from repositories.customer_repository import CustomerRepository
from models.customer import CustomerDB
from fastapi import HTTPException


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
    def get_customer(self, db, customer_id: int, user_id: int):
        if not self.is_owner(db, customer_id, user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this customer"
            )

        return self.repo.get_by_id(db, customer_id)

    # GET ALL
    def get_customers(self, db, user: dict, skip: int = 0, limit: int = 10):
        return self.repo.get_all(
            db,
            user_id=user["user_id"],
            is_admin=user["role"] == "admin",
            skip=skip,
            limit=limit,
        )

    # UPDATE
    def update_customer(self, db, customer_id: int, data, user_id: int):
        customer = self.repo.get_by_id(db, customer_id)

        if not customer:
            return None

        if not self.is_owner(db, customer_id, user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this customer"
            )

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
    def delete_customer(self, db, customer_id: int, user_id: int):
        customer = self.repo.get_by_id(db, customer_id)

        if not customer:
            return None

        if not self.is_owner(db, customer_id, user_id):
            raise HTTPException(
                status_code=403, detail="Not authorized to access this customer"
            )

        self.repo.delete(db, customer)
        return True

    #   Owner check function
    def is_owner(self, db, customer_id: int, user_id: int):
        customer = self.repo.get_by_id(db, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer.created_by == user_id
