import enum
from sqlalchemy import Column, Integer, Float,String, ForeignKey, DateTime, Enum,Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class OrderStatus(str, enum.Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    varient_id = Column(Integer,ForeignKey("product_variants.id"))
    subtotal = Column(Numeric(10, 2), nullable=False) 
    gst_charge = Column(Numeric(10, 2), nullable=False) 
    platform_fee = Column(Numeric(10, 2), default=20.00) 
    total_amount = Column(Numeric(10, 2), nullable=False)

    payment_method = Column(String(50)) # "Online Payment" or "Cash on Delivery"
    payment_status = Column(String(50), default="Pending")
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order")
    user = relationship("User")
    address = relationship("Address")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=True)
    
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")