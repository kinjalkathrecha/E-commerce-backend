from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.product import router as pro_router
from app.db.database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(user_router, prefix="/auth", tags=["Auth"])
app.include_router(pro_router,prefix="/products",tags=["Products"])