from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product, ProductVariant
from app.schemas.product import ProductCreate, ProductUpdate, ProductVariantCreate, ProductVariantUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_section(self, db: Session, *, section_id: int) -> List[Product]:
        return db.query(Product).filter(Product.section_id == section_id).all()

class CRUDProductVariant(CRUDBase[ProductVariant, ProductVariantCreate, ProductVariantUpdate]):
    def get_by_product(self, db: Session, *, product_id: int) -> List[ProductVariant]:
        return db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()

product = CRUDProduct(Product)
product_variant = CRUDProductVariant(ProductVariant)
