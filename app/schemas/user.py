from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    role: RoleEnum

    model_config = {
        "from_attributes": True
    }
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
