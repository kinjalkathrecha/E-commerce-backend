from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.order import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    price_at_purchase: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    address_id: Optional[int] = None
    varient_id: Optional[int] = None
    promo_code_id: Optional[int] = None
    subtotal: float
    gst_charge: float
    platform_fee: float = 20.00
    total_amount: float
    payment_method: Optional[str] = None
    payment_status: str = "Pending"
    status: OrderStatus = OrderStatus.pending

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    address_id: Optional[int] = None
    varient_id: Optional[int] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    status: Optional[OrderStatus] = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
