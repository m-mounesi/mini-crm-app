from fastapi import HTTPException

from repositories.task_repository import TaskRepository
from models.task import TaskDB
from core.dependencies import get_project_service


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo
        self.project_service = get_project_service

    def create_task(self, db, data, user_id: int):
        task = TaskDB(
            title=data.title,
            description=data.description,
            project_id=data.project_id,
            assigned_to=data.assigned_to,
            created_by=user_id,
        )

        return self.repo.create(db, task)

    def get_tasks(self, db, project_id: int, user_id: int):
        if not self.project_service.is_owner(db, project_id, user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this task"
            )
        return self.repo.get_all(db, project_id)

    def get_task(self, db, task_id: int, user_id: int):
        if not self.is_owner(db, task_id, user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this task"
            )
        return self.repo.get_by_id(db, task_id)

    def toggle_task(self, db, task_id: int, user_id: int):
        if not self.is_owner(db, task_id, user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this task"
            )

        task = self.repo.get_by_id(db, task_id)

        if not task:
            return None

        task.completed = not task.completed
        return self.repo.update(db, task)
        #   Owner check function

    def is_owner(self, db, customer_id: int, user_id: int):
        customer = self.repo.get_by_id(db, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer.created_by == user_id
