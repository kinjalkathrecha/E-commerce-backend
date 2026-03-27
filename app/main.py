from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)