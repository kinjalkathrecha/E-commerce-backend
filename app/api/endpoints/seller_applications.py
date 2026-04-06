from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import BecomeSellerCreate, BecomeSellerUpdate, BecomeSellerResponse
from app import crud
from app.core.dependencies import get_db, get_current_active_admin, get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[BecomeSellerResponse])
def read_seller_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Any = Depends(get_current_active_admin),
) -> Any:
    """Retrieve all seller applications (Admin only)."""
    return crud.become_seller.get_multi(db, skip=skip, limit=limit)

@router.get("/my-application", response_model=BecomeSellerResponse)
def read_my_application(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """Retrieve current user's seller application."""
    application = crud.become_seller.get_by_user(db, user_id=current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.post("/", response_model=BecomeSellerResponse, status_code=status.HTTP_201_CREATED)
def create_seller_application(
    *,
    db: Session = Depends(get_db),
    application_in: BecomeSellerCreate,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """Submit a seller application."""
    application = crud.become_seller.get_by_user(db, user_id=current_user.id)
    if application:
        raise HTTPException(status_code=400, detail="You have already applied.")
    application = crud.become_seller.create_with_user(db, obj_in=application_in, user_id=current_user.id)
    return application

@router.patch("/{id}", response_model=BecomeSellerResponse)
def update_seller_application(
    *,
    db: Session = Depends(get_db),
    id: int,
    application_in: BecomeSellerUpdate,
    current_admin: Any = Depends(get_current_active_admin)
) -> Any:
    """Review and update a seller application (Admin only)."""
    application = crud.become_seller.get(db, id=id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application = crud.become_seller.update(db, db_obj=application, obj_in=application_in)
    return application
