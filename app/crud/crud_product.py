from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product, ProductVariant, Wishlist, Review, CartItem
from app.schemas.product import ProductCreate, ProductUpdate, ProductVariantCreate, ProductVariantUpdate, WishlistCreate, ReviewCreate, ReviewUpdate, CartItemCreate, CartItemUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_section(self, db: Session, *, section_id: int) -> List[Product]:
        return db.query(Product).filter(Product.section_id == section_id).all()

class CRUDProductVariant(CRUDBase[ProductVariant, ProductVariantCreate, ProductVariantUpdate]):
    def get_by_product(self, db: Session, *, product_id: int) -> List[ProductVariant]:
        return db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()

class CRUDWishlist(CRUDBase[Wishlist, WishlistCreate, WishlistCreate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[Wishlist]:
        return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    def get_by_user_and_product(self, db: Session, *, user_id: int, product_id: int) -> Optional[Wishlist]:
        return db.query(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id).first()

class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def get_by_product(self, db: Session, *, product_id: int) -> List[Review]:
        return db.query(Review).filter(Review.product_id == product_id).all()
    def get_by_user_and_product(self, db: Session, *, user_id: int, product_id: int) -> Optional[Review]:
        return db.query(Review).filter(Review.user_id == user_id, Review.product_id == product_id).first()

class CRUDCartItem(CRUDBase[CartItem, CartItemCreate, CartItemUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[CartItem]:
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()
    def get_by_user_and_product(self, db: Session, *, user_id: int, product_id: int, variant_id: Optional[int] = None) -> Optional[CartItem]:
        query = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        if variant_id:
            query = query.filter(CartItem.variant_id == variant_id)
        return query.first()

product = CRUDProduct(Product)
product_variant = CRUDProductVariant(ProductVariant)
wishlist = CRUDWishlist(Wishlist)
review = CRUDReview(Review)
cart_item = CRUDCartItem(CartItem)
