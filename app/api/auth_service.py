from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.hashing import Hasher
from app.auth.jwt_handler import create_access_token

def register_user(user_data: UserCreate, session: Session) -> User:
    # Check if the username is already taken
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )

    # Hash the user's password before storing
    hashed_password = Hasher.get_password_hash(user_data.password)

    # Create new user instance with hashed password
    user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        role=user_data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def login_user(username: str, password: str, session: Session) -> str:
    # Look up user by username
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    # Validate user existence and password
    if not user or not Hasher.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    # Generate and return JWT access token
    return create_access_token(data={"sub": str(user.id), "role": user.role})
