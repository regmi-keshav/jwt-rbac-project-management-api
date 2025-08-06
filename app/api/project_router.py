from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db.database import get_session
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectRead
from ..auth.dependencies import get_current_user, require_admin
from ..models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=list[ProjectRead])
def get_projects(session: Session = Depends(get_session), _: User = Depends(get_current_user)):
    return session.exec(select(Project)).all()

@router.post("/", response_model=ProjectRead)
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
    user: User = Depends(require_admin),
):
    existing = session.exec(select(Project).where(Project.name == project.name)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with this name already exists.",
        )

    db_project = Project(**project.dict())
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    updated_data: ProjectCreate,
    session: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in updated_data.dict().items():
        setattr(project, key, value)
    session.commit()
    return project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"detail": "Deleted successfully"}
