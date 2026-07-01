from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from services.customer_service import CustomerService
from schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

from security.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

service = CustomerService()


# CREATE Customer
@router.post("/", response_model=CustomerResponse)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return service.create_customer(db, data, current_user["user_id"])


# GET ALL
@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return service.get_customers(db, current_user, skip, limit)


# GET BY ID
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = service.get_customer(db, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


# UPDATE
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)
):
    customer = service.update_customer(db, customer_id, data)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


# Delete
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    result = service.delete_customer(db, customer_id)

    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"message": "Customer deleted successfully"}
