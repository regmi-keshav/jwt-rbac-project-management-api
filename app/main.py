from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db.database import create_db_and_tables
from .auth.auth_router import router as auth_router
from .api.project_router import router as project_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="FastAPI RBAC - Project Management App",
    lifespan=lifespan
)
app.include_router(auth_router)
app.include_router(project_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Project Management API"}