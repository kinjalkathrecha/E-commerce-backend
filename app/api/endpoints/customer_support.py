from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import CustomerSupportCreate, CustomerSupportUpdate, CustomerSupportResponse
from app import crud
from app.core.dependencies import get_db, get_current_active_admin, get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[CustomerSupportResponse])
def read_customer_supports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """Retrieve customer support tickets."""
    if current_user.role.role_name == "Admin":
        supports = crud.customer_support.get_multi(db, skip=skip, limit=limit)
    else:
        supports = crud.customer_support.get_by_user(db, user_id=current_user.id)
    return supports

@router.post("/", response_model=CustomerSupportResponse, status_code=status.HTTP_201_CREATED)
def create_customer_support(
    *,
    db: Session = Depends(get_db),
    support_in: CustomerSupportCreate,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """Create new support ticket."""
    support = crud.customer_support.create_with_user(db, obj_in=support_in, user_id=current_user.id)
    return support

@router.patch("/{id}", response_model=CustomerSupportResponse)
def update_customer_support(
    *,
    db: Session = Depends(get_db),
    id: int,
    support_in: CustomerSupportUpdate,
    current_admin: Any = Depends(get_current_active_admin)
) -> Any:
    """Update support ticket status or priority (Admin only)."""
    support = crud.customer_support.get(db, id=id)
    if not support:
        raise HTTPException(status_code=404, detail="Ticket not found")
    support = crud.customer_support.update(db, db_obj=support, obj_in=support_in)
    return support
