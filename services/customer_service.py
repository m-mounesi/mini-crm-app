from repositories.customer_repository import CustomerRepository
from models.customer import CustomerDB


class CustomerService:
    def __init__(self):
        self.repo = CustomerRepository()

    # CREATE
    def create_customer(self, db, data, user_id: int):
        customer = CustomerDB(
            name=data.name,
            email=data.email,
            phone=data.phone,
            description=data.description,
            created_by=user_id,
        )

        return self.repo.create(db, customer)

    # GET ONE
    def get_customer(self, db, customer_id: int):
        return self.repo.get_by_id(db, customer_id)

    # GET ALL
    def get_customers(self, db, skip: int = 0, limit: int = 10):
        return self.repo.get_all(db, skip, limit)

    # UPDATE
    def update_customer(self, db, customer_id: int, data):
        customer = self.repo.get_by_id(db, customer_id)

        if not customer:
            return None

        if data.name is not None:
            customer.name = data.name

        if data.email is not None:
            customer.email = data.email

        if data.phone is not None:
            customer.phone = data.phone

        if data.description is not None:
            customer.description = data.description

        return self.repo.update(db, customer)

    # DELETE
    def delete_customer(self, db, customer_id: int):
        customer = self.repo.get_by_id(db, customer_id)

        if not customer:
            return None

        self.repo.delete(db, customer)
        return True
