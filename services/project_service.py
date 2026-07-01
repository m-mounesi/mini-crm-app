from repositories.project_repository import ProjectRepository
from models.project import ProjectDB


class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()

    def create_project(self, db, data, user_id: int):
        project = ProjectDB(
            title=data.title, customer_id=data.customer_id, created_by=user_id
        )

        return self.repo.create(db, project)

    def get_projects(self, db, user):
        return self.repo.get_all(
            db, user_id=user["user_id"], is_admin=user["role"] == "admin"
        )

    def get_project(self, db, project_id: int):
        return self.repo.get_by_id(db, project_id)
