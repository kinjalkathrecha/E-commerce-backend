from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import ReviewCreate, ReviewUpdate, ReviewResponse
from app import crud
from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    return crud.review.get_by_product(db=db, product_id=product_id)

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Optional logic: ensure user bought the product via checking orders (skipping for now)
    existing_review = crud.review.get_by_user_and_product(db=db, user_id=current_user.id, product_id=review.product_id)
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
        
    review_dict = review.model_dump()
    review_dict["user_id"] = current_user.id
    new_review = crud.review.create(db=db, obj_in=review_dict)
    return new_review

@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_review = crud.review.get(db=db, id=review_id)
    if not db_review or db_review.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Review not found")
    
    updated_review = crud.review.update(db=db, db_obj=db_review, obj_in=review)
    return updated_review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_review = crud.review.get(db=db, id=review_id)
    if not db_review or db_review.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Review not found")
    crud.review.remove(db=db, id=review_id)
    return None
