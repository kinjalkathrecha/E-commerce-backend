from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()

class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, OrderItemCreate]):
    def get_by_order(self, db: Session, *, order_id: int) -> List[OrderItem]:
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

order = CRUDOrder(Order)
order_item = CRUDOrderItem(OrderItem)
