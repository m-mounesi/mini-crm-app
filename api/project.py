from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import UserDB
from schemas.project import ProjectCreate, ProjectResponse
from security.dependencies import require_permission
from services.project_service import ProjectService
from security.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


# CREATE
@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
    service: ProjectService = Depends(ProjectService),
    dependencies=Depends(require_permission("project.create")),
):
    return service.create_project(db, data, user.user_id)


# GET ALL
@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
    service: ProjectService = Depends(ProjectService),
    dependencies=Depends(require_permission("project.read")),
):
    return service.get_projects(db, user)


# GET BY ID
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: UserDB = Depends(get_current_user),
    service: ProjectService = Depends(ProjectService),
    dependencies=Depends(require_permission("project.read")),
):
    return service.get_project(db, project_id, user)
