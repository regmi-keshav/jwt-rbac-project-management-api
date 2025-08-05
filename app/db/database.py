from sqlmodel import create_engine
from sqlalchemy.exc import OperationalError
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=True)

def test_connection():
    try:
        with engine.connect() as connection:
            print("Database connection successful.")
    except OperationalError as e:
        print("Database connection failed:")
        print(e)

