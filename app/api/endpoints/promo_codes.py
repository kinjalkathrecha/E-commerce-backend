from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import PromoCodeCreate, PromoCodeResponse
from app import crud
from app.core.dependencies import get_db, get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[PromoCodeResponse])
def read_promo_codes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """Retrieve promo codes."""
    promo_codes = crud.promo_code.get_multi(db, skip=skip, limit=limit)
    if current_user.role.role_name == "Admin":
        return promo_codes
    elif current_user.role.role_name == "Seller":
        # Seller sees their own, plus any active general ones
        return [p for p in promo_codes if p.seller_id == current_user.id or p.is_active]
    else:
        # Customers only see active ones
        return [p for p in promo_codes if p.is_active]

@router.post("/", response_model=PromoCodeResponse, status_code=status.HTTP_201_CREATED)
def create_promo_code(
    *,
    db: Session = Depends(get_db),
    promo_code_in: PromoCodeCreate,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """Create new promo code (Admin or Seller)."""
    if current_user.role.role_name not in ["Admin", "Seller"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    promo_code = crud.promo_code.get_by_code(db, code=promo_code_in.code)
    if promo_code:
        raise HTTPException(
            status_code=400,
            detail="The promo code already exists in the system.",
        )
    
    if current_user.role.role_name == "Seller":
        promo_code_in.seller_id = current_user.id
        
    promo_code = crud.promo_code.create(db, obj_in=promo_code_in)
    return promo_code

@router.get("/validate/{code}", response_model=PromoCodeResponse)
def validate_promo_code(
    code: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """Validate a promo code by code."""
    promo_code = crud.promo_code.get_by_code(db, code=code)
    if not promo_code:
        raise HTTPException(status_code=404, detail="Promo code not found")
    if not promo_code.is_active:
        raise HTTPException(status_code=400, detail="Promo code is inactive")
    return promo_code

@router.delete("/{id}", response_model=PromoCodeResponse)
def delete_promo_code(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    """Delete a promo code (Admin or Seller for their own)."""
    if current_user.role.role_name not in ["Admin", "Seller"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    promo_code = crud.promo_code.get(db, id=id)
    if not promo_code:
        raise HTTPException(status_code=404, detail="Promo code not found")
        
    if current_user.role.role_name == "Seller" and promo_code.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this promo code")
        
    promo_code = crud.promo_code.remove(db=db, id=id)
    return promo_code
