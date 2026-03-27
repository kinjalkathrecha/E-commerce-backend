from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class ProductVariantBase(BaseModel):
    variant_name: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    additional_price: float = 0.00
    stock_quantity: int = 0

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantUpdate(BaseModel):
    variant_name: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    additional_price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    base_price: float
    discounted_price: Optional[float] = None
    stock_quantity: int = 0
    image_url: Optional[str] = None
    section_id: int
    brand_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    discounted_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None
    section_id: Optional[int] = None
    brand_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    variants: List[ProductVariantResponse] = []

    class Config:
        from_attributes = True

class WishlistBase(BaseModel):
    product_id: int

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    id: int
    user_id: int
    added_at: datetime
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(default=1, gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)

class CartItemResponse(CartItemBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True