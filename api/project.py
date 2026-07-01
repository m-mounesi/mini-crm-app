from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.project import ProjectCreate, ProjectResponse
from services.project_service import ProjectService
from security.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

service = ProjectService()


# CREATE
@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.create_project(db, data, user["user_id"])


# GET ALL
