from models.project import ProjectDB


class ProjectRepository:
    def create(self, db, project: ProjectDB):
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def get_by_id(self, db, project_id: int):
        return db.query(ProjectDB).filter(ProjectDB.id == project_id).first()

    def get_all(self, db, user_id: int, is_admin: bool):
        query = db.query(ProjectDB)

        if not is_admin:
            query = query.filter(ProjectDB.created_by == user_id)

        return query.all()

    def delete(self, db, project: ProjectDB):
        db.delete(project)
        db.commit()
