from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.task import TaskCreate, TaskResponse
from services.task_service import TaskService
from security.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

service = TaskService()


# CREATE Task
@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.create_task(db, data, user["user_id"])


# GET ALL
@router.get("/", response_model=list[TaskResponse])
def get_tasks(project_id: int, db: Session = Depends(get_db)):
    return service.get_tasks(db, project_id)


# TOGGLE STATUS
@router.patch("/{task_id}/toggle")
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = service.toggle_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
