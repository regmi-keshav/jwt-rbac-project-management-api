from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List
from app.db.database import get_session
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.api.project_service import create_project, get_projects, update_project, delete_project
from app.auth.dependencies import get_current_user
from app.models.user import User

# Group project-related endpoints under /projects
router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/create", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create(
    data: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Create a new project for the current user
    return create_project(data, session, current_user.id)

@router.get("", response_model=List[ProjectRead], status_code=status.HTTP_200_OK)
def list_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Retrieve all projects belonging to the current user
    return get_projects(session, current_user.id)

@router.put("/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def update(
    project_id: int,
    data: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Update a project owned by the current user
    return update_project(project_id, data, session, current_user.id)

@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def delete(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Delete a project owned by the current user
    return delete_project(project_id, session, current_user.id)
