from fastapi import APIRouter,Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.database import SessionLocal
from app.core.security import hash_password,verify_password,create_access_token
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user:UserCreate,db:Session=Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_user=User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user:UserCreate,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="User not found")
    if not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400,detail="Invalid password")
    token=create_access_token({"sub":db_user.email})
    return {"access_token":token,"token_type":"bearer"}

