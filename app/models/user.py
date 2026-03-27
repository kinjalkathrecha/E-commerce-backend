import enum
from sqlalchemy import Column,Enum, Integer, String, Boolean,Text,DateTime,ForeignKey,Numeric
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    role = relationship("UserRole", back_populates="users")

    reviews = relationship("Review", back_populates="user")
    wishlist_items = relationship("Wishlist", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False) # e.g., "Admin", "Customer", "Artist"

    users = relationship("User", back_populates="role")

class BulkInquiry(Base):
    __tablename__ = "bulk_inquiries"

    id = Column(Integer, primary_key=True, index=True)
    Company_Individual_Name = Column(String(255), nullable=False)
    contact_person_name = Column(String(255), nullable=False)
    preferred_contact_method = Column(String(50))
    email = Column(String(255), nullable=False)
    whatsapp_number = Column(String(20), nullable=False)
    require_customization = Column(Boolean, default=False)
    budget_range = Column(String(100), nullable=False) # e.g., "5000-10000"
    delivery_timeframe_value = Column(Integer) # e.g., 10
    delivery_timeframe_unit = Column(String(20))  # e.g., "Days" or "Months"
    additional_requirements = Column(Text, nullable=True)
    preferred_contact_datetime = Column(DateTime, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    inquiry_type = Column(String(50), nullable=False, default="General")
    created_at = Column(DateTime, default=datetime.utcnow)
    selected_categories = relationship("Category", backref="bulk_inquiries")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    address_line = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    phone_number = Column(String(20), nullable=False)
    address_type = Column(String(50)) 
    
    user = relationship("User")

class PromoCode(Base):
    __tablename__ = "promo_codes"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percentage = Column(Numeric(5, 2))
    is_active = Column(Boolean, default=True)
    expiry_date = Column(DateTime)

class TicketStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class BecomeSeller(Base):
    __tablename__ = "become_seller_applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    business_name = Column(String(255), nullable=False)
    gst_number = Column(String(50), nullable=False)
    pan_card = Column(String(50), nullable=False)
    store_description = Column(Text)
    
    # Status tracking
    is_reviewed = Column(Boolean, default=False)
    admin_status = Column(String(50), default="Pending") # "Pending", "Approved", "Rejected"
    
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class CustomerSupport(Base):
    __tablename__ = "customer_support"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True) # Optional link to order
    
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="Open") # Open, In Progress, Resolved
    priority = Column(String(50), default="Medium") # Low, Medium, High
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    user = relationship("User")
    order = relationship("Order")