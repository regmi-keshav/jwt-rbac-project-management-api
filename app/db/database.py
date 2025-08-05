from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings
from app.models import user

settings = get_settings()

engine = create_engine(settings.database_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session