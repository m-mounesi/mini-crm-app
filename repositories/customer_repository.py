from models.customer import CustomerDB

class CustomerRepository:
    
    def create(self, db, customer: CustomerDB):
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    
    def get_by_id(self, db, customer_id: int):
        return db.query(CustomerDB).filter(CustomerDB.id== customer_id).first()
    
    def get_all(self, db, skip:int = 0, limit: int= 10):
        return db.query(CustomerDB).offset(skip).limit(limit).all()
    
    def update(self, db, customer: CustomerDB):
        db.commit()
        db.refresh(customer)
        return customer
    
    def delete(self, db, customer: CustomerDB):
        db.delete(customer)
        db.commit()