from models.customer import CustomerDB


class CustomerRepository:
    def create(self, db, customer: CustomerDB):
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def get_by_id(self, db, customer_id: int):
        return db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()

    def get_all(self, db, user_id: int, is_admin: bool, skip: int = 0, limit: int = 10):
        query = db.query(CustomerDB)

        if not is_admin:
            query = query.filter(CustomerDB.created_by == user_id)

        return query.offset(skip).limit(limit).all()

    def update(self, db, customer: CustomerDB):
        db.commit()
        db.refresh(customer)
        return customer

    def delete(self, db, customer: CustomerDB):
        db.delete(customer)
        db.commit()
