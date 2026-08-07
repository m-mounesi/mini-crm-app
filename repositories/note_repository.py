from datetime import datetime, timezone

from models.note import NoteDB


class NoteRepository:
    def create(self, db, note: NoteDB):
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    def get_by_id(self, db, note_id: int):
        return (
            db.query(NoteDB)
            .filter(NoteDB.id == note_id, NoteDB.deleted_at.is_(None))
            .first()
        )

    def get_all(self, db, user_id: int, is_admin: bool, skip: int = 0, limit: int = 10):
        query = db.query(NoteDB).filter(NoteDB.deleted_at.is_(None))

        if not is_admin:
            query = query.filter(NoteDB.created_by == user_id)

        return query.offset(skip).limit(limit).all()

    def update(self, db, note: NoteDB):
        db.commit()
        db.refresh(note)
        return note

    def delete(self, db, note: NoteDB):
        note.deleted_at = datetime.now(timezone.utc)
        db.commit()
