from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import create_db_and_tables
from app.routes.auth_router import router as auth_router
from app.routes.project_router import router as project_router

# Lifespan context to handle startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database and tables before app starts
    create_db_and_tables()
    yield  # Allow app to run

# Initialize FastAPI app with lifespan for startup tasks
app = FastAPI(
    title="FastAPI RBAC - Project Management App",
    lifespan=lifespan
)

# Include auth and project routes
app.include_router(auth_router)
app.include_router(project_router)

# Simple root endpoint for health check or welcome message
@app.get("/")
def root():
    return {"message": "Welcome to the Project Management API"}
