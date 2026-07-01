from models.task import TaskDB


class TaskRepository:
    def create(self, db, task: TaskDB):
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def get_by_id(self, db, task_id: int):
        return db.query(TaskDB).filter(TaskDB.id == task_id).first()

    def get_all(self, db, project_id: int = None):
        query = db.query(TaskDB)

        if project_id:
            query = query.filter(TaskDB.project_id == project_id)

        return query.all()

    def update(self, db, task: TaskDB):
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db, task: TaskDB):
        db.delete(task)
        db.commit()
