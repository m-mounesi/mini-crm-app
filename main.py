from fastapi import FastAPI
from api.customer import router as customer_router
from api.project import router as project_router

app = FastAPI()

app.include_router(customer_router)
app.include_router(project_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
