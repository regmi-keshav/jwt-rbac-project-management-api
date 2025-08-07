from sqlmodel import SQLModel, Field
from typing import Optional

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")
