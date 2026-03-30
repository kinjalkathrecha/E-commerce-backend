from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import WishlistCreate, WishlistResponse
from app import crud
from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[WishlistResponse])
def get_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.wishlist.get_by_user(db=db, user_id=current_user.id)

@router.post("/", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(item: WishlistCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_item = crud.wishlist.get_by_user_and_product(db=db, user_id=current_user.id, product_id=item.product_id)
    if existing_item:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
    
    item_dict = item.model_dump()
    item_dict["user_id"] = current_user.id
    new_item = crud.wishlist.create(db=db, obj_in=item_dict)
    return new_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = crud.wishlist.get(db=db, id=item_id)
    if not db_item or db_item.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    crud.wishlist.remove(db=db, id=item_id)
    return None
