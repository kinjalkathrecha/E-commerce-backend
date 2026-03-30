from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, Token
from app import crud
from app.core.dependencies import get_db, get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import UserRole,User
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    customer_role = db.query(UserRole).filter(
        UserRole.role_name == "Customer"
    ).first()
    if not customer_role:
        raise HTTPException(
            status_code=500,
            detail="Customer role not found"
        )
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        role_id=customer_role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.user.get_by_email(db, email=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/create-admin", response_model=UserResponse)
def create_admin(user: UserCreate, db: Session = Depends(get_db)):
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Find admin role
    admin_role = db.query(UserRole).filter(
        UserRole.role_name == "Admin"
    ).first()

    if not admin_role:
        raise HTTPException(
            status_code=404,
            detail="Admin role not found"
        )
    
    # Create admin user
    new_admin = User(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
        role_id=admin_role.id
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin