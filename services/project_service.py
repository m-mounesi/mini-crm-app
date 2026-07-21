from fastapi import HTTPException

from models.user import UserDB
from repositories.project_repository import ProjectRepository
from models.project import ProjectDB
from repositories.user_repository import UserRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def create_project(self, db, data, user_id: int):
        project = ProjectDB(
            title=data.title, customer_id=data.customer_id, created_by=user_id
        )

        return self.repo.create(db, project)

    def get_projects(self, db, user: UserDB):
        return self.repo.get_all(
            db,
            user_id=user.user_id,
            is_admin=any(role.name == "admin" for role in user.roles),
        )

    def get_project(self, db, project_id: int, current_user: UserDB):
        if not self.is_owner(db, project_id, current_user.user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this project"
            )

        return self.repo.get_by_id(db, project_id)

    #   Owner check function
    def is_owner(self, db, project_id: int, user_id: int):
        project = self.repo.get_by_id(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project.created_by == user_id
