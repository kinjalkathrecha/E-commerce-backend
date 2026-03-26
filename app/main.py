from fastapi import FastAPI
from app.api.user import router as user_router
from app.db.database import engine, Base
from app.models import user

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(user_router, prefix="/auth", tags=["Auth"])