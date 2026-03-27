from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product
from app import crud
from app.core.dependencies import get_db, get_current_active_admin

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    section_id: Optional[int] = Query(None, description="Filter by section ID"),
    search: Optional[str] = Query(None, description="Search by title or description"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if section_id:
        query = query.filter(Product.section_id == section_id)
    if search:
        query = query.filter(
            or_(
                Product.title.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )
    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)
        
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    new_product = crud.product.create(db=db, obj_in=product)
    return new_product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    db_product = crud.product.get(db=db, id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = crud.product.update(db=db, db_obj=db_product, obj_in=product)
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    db_product = crud.product.get(db=db, id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.product.remove(db=db, id=product_id)
    return None
