from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

def create_project(data: ProjectCreate, session: Session, owner_id: int) -> ProjectRead:
    # Initialize new project with owner ID
    project = Project(**data.model_dump(), owner_id=owner_id)
    try:
        session.add(project)
        session.commit()
        session.refresh(project)
    except IntegrityError:
        session.rollback()
        # Handle unique constraint (e.g., duplicate project name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project with the same name already exists."
        )
    return ProjectRead.model_validate(project)

def get_projects(session: Session, owner_id: int) -> List[ProjectRead]:
    # Retrieve all projects for the given owner
    statement = select(Project).where(Project.owner_id == owner_id)
    projects = session.exec(statement).all()
    return [ProjectRead.model_validate(p) for p in projects]

def update_project(project_id: int, data: ProjectUpdate, session: Session, owner_id: int) -> ProjectRead:
    # Fetch project by ID and owner
    statement = select(Project).where(Project.id == project_id, Project.owner_id == owner_id)
    project = session.exec(statement).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied."
        )

    # Apply only the fields that were provided
    for key, value in data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    try:
        session.commit()
        session.refresh(project)
    except IntegrityError:
        session.rollback()
        # Handle update constraint violations (e.g., duplicate name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not update project due to constraint violation."
        )

    return ProjectRead.model_validate(project)

def delete_project(project_id: int, session: Session, owner_id: int) -> dict:
    # Fetch project to ensure it exists and belongs to the owner
    statement = select(Project).where(Project.id == project_id, Project.owner_id == owner_id)
    project = session.exec(statement).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied."
        )

    session.delete(project)
    session.commit()

    return {"detail": "Project deleted successfully"}
