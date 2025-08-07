from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.database import get_session
from app.schemas.user import UserCreate, UserLogin, Token, UserRead
from app.api.auth_service import register_user, login_user

# Auth-related routes grouped under /auth
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Create a new user account
    user_obj = register_user(user, session)
    return UserRead.model_validate(user_obj)

@router.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    # Authenticate user and return JWT access token
    access_token = login_user(user.username, user.password, session)
    return {"access_token": access_token, "token_type": "bearer"}
