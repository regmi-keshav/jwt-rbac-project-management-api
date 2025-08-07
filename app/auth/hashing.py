from passlib.context import CryptContext

# Configure password hashing context with bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Generate a secure hash for the given plain-text password
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Verify that the plain-text password matches the hashed version
        return pwd_context.verify(plain_password, hashed_password)
