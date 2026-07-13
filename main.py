from fastapi import FastAPI
from api.customer import router as customer_router
from api.project import router as project_router
from api.auth import router as auth_router
from api.task import router as task_router
from contextlib import asynccontextmanager
from core.database import SessionLocal

from seeders.rbac_seed import seed_roles, seed_permissions, assign_admin_permissions
from seeders.admin_seed import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = SessionLocal()

    try:
        seed_roles(db)
        seed_permissions(db)
        assign_admin_permissions(db)
        create_admin(db)

    finally:
        db.close()

    yield


app = FastAPI(title="Mini CRM", lifespan=lifespan)

app.include_router(customer_router)
app.include_router(project_router)
app.include_router(auth_router)
app.include_router(task_router)
