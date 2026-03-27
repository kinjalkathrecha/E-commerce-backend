from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app import crud
from app.core.dependencies import get_db, get_current_active_admin

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.category.get_multi(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    db_category = crud.category.get_by_slug(db, slug=category.slug)
    if db_category:
        raise HTTPException(status_code=400, detail="Slug already exists")
    new_category = crud.category.create(db=db, obj_in=category)
    return new_category

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    db_category = crud.category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    updated_category = crud.category.update(db=db, db_obj=db_category, obj_in=category)
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    db_category = crud.category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.category.remove(db=db, id=category_id)
    return None
