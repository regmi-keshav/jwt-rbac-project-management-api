from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import test_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Test DB connection
    test_connection()
    yield

app = FastAPI(
    title="FastAPI RBAC - Project Management App",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Welcome to the Project Management API"}
