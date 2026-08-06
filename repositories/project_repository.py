from datetime import datetime, timezone

from models.project import ProjectDB


class ProjectRepository:
    def create(self, db, project: ProjectDB):
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def get_by_id(self, db, project_id: int):
        return (
            db.query(ProjectDB)
            .filter(ProjectDB.id == project_id, ProjectDB.deleted_at.is_(None))
            .first()
        )

    def get_all(self, db, user_id: int, is_admin: bool):
        query = db.query(ProjectDB).filter(ProjectDB.deleted_at.is_(None))

        if not is_admin:
            query = query.filter(ProjectDB.created_by == user_id)

        return query.all()

    def update(self, db, project: ProjectDB):
        db.commit()
        db.refresh(project)
        return project

    def delete(self, db, project: ProjectDB):
        project.deleted_at = datetime.now(timezone.utc)
        db.commit()
