from repositories.task_repository import TaskRepository
from models.task import TaskDB


class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, db, data, user_id: int):
        task = TaskDB(
            title=data.title,
            description=data.description,
            project_id=data.project_id,
            assigned_to=data.assigned_to,
            created_by=user_id,
        )

        return self.repo.create(db, task)

    def get_tasks(self, db, project_id: int):
        return self.repo.get_all(db, project_id)

    def get_task(self, db, task_id: int):
        return self.repo.get_by_id(db, task_id)

    def toggle_task(self, db, task_id: int):
        task = self.repo.get_by_id(db, task_id)

        if not task:
            return None

        task.completed = not task.completed
        return self.repo.update(db, task)
