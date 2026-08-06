from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import UserDB
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from security.dependencies import require_permission
from services.project_service import ProjectService
from core.dependencies import get_project_service

router = APIRouter(prefix="/projects", tags=["projects"])


# CREATE
@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service),
    user: UserDB = Depends(require_permission("project.create")),
):
    return service.create_project(db, data, user.user_id)


# GET ALL
@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service),
    user: UserDB = Depends(require_permission("project.read")),
):
    return service.get_projects(db, user)


# GET BY ID
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service),
    user: UserDB = Depends(require_permission("project.read")),
):
    return service.get_project(db, project_id, user)


# UPDATE
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service),
    user: UserDB = Depends(require_permission("project.update")),
):
    project = service.update_project(db, project_id, data, user.user_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


# DELETE
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service),
    user: UserDB = Depends(require_permission("project.delete")),
):
    result = service.delete_project(db, project_id, user.user_id)

    if not result:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted successfully"}
