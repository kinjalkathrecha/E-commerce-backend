from sqlalchemy import Column,Numeric, Integer, String, Float, ForeignKey,DateTime,Text,CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    base_price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=True)
    stock_quantity = Column(Integer, default=0) 
    image_url = Column(String(500)) 
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id")) # <--- New link
    
    brand = relationship("Brand", back_populates="products")
    section = relationship("Section", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete")
    reviews = relationship("Review", back_populates="product")

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    variant_name = Column(String(100))
    color = Column(String(50), nullable=True)
    size = Column(String(50), nullable=True) 
    material = Column(String(50), nullable=True) 
    additional_price = Column(Numeric(10, 2), default=0.00) # Added to base price
    stock_quantity = Column(Integer, default=0) 

    product = relationship("Product", back_populates="variants")

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=True)
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cart_items")
    __table_args__ = (CheckConstraint('quantity > 0', name='min_quantity_1'),)

