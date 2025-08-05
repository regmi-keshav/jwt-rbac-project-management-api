from sqlmodel import SQLModel, Field
from typing import Optional
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: RoleEnum = Field(default=RoleEnum.user)
