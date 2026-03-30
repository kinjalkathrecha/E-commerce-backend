from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import CartItemCreate, CartItemUpdate, CartItemResponse
from app import crud
from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CartItemResponse])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.cart_item.get_by_user(db=db, user_id=current_user.id)

@router.post("/", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if item already in cart
    existing_item = crud.cart_item.get_by_user_and_product(
        db=db, user_id=current_user.id, product_id=item.product_id, variant_id=item.variant_id
    )
    if existing_item:
        # Update quantity
        item_update = CartItemUpdate(quantity=existing_item.quantity + item.quantity)
        return crud.cart_item.update(db=db, db_obj=existing_item, obj_in=item_update)
    
    # Create new item
    item_dict = item.model_dump()
    item_dict["user_id"] = current_user.id
    new_item = crud.cart_item.create(db=db, obj_in=item_dict)
    return new_item

@router.patch("/{item_id}", response_model=CartItemResponse)
def update_cart_item(item_id: int, item: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = crud.cart_item.get(db=db, id=item_id)
    if not db_item or db_item.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    updated_item = crud.cart_item.update(db=db, db_obj=db_item, obj_in=item)
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = crud.cart_item.get(db=db, id=item_id)
    if not db_item or db_item.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    crud.cart_item.remove(db=db, id=item_id)
    return None
