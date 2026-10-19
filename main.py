from fastapi import FastAPI
from Services.database import engine, base
from models.models import User
from routers.home import router as home_router
from routers.router import router as work_router

app = FastAPI(title="Authentication API")

# Create database tables
base.metadata.create_all(bind=engine)

app.include_router(home_router)
app.include_router(work_router)

