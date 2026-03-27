from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderResponse
from app.models.order import Order, OrderItem
from app.models.user import User
from app import crud
from app.core.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Pre-validation for stock
    for item in order_data.items:
        product = crud.product.get(db=db, id=item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.title}")
            
    # Calculate prices
    subtotal = 0.0
    for item in order_data.items:
        product = crud.product.get(db=db, id=item.product_id)
        price = product.discounted_price if product.discounted_price else product.base_price
        subtotal += price * item.quantity
        
    gst_charge = subtotal * 0.18 # Example 18% GST
    platform_fee = 20.00
    total_amount = subtotal + gst_charge + platform_fee
    
    # Create the Order
    order_data_dict = order_data.model_dump()
    order_data_dict.update({
        "user_id": current_user.id,
        "subtotal": subtotal,
        "gst_charge": gst_charge,
        "platform_fee": platform_fee,
        "total_amount": total_amount,
        "payment_status": "Pending"
    })
    
    # We remove items from dict to prevent model fields mismatch during Model instantiation
    order_data_dict.pop("items", None)
    
    new_order = Order(**order_data_dict)
    db.add(new_order)
    db.flush()  # To get new_order.id
    
    # Process Order Items
    for item in order_data.items:
        product = crud.product.get(db=db, id=item.product_id)
        
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            price_at_purchase=product.discounted_price if product.discounted_price else product.base_price
        )
        db.add(order_item)
        
        # Deduct stock
        product.stock_quantity -= item.quantity
        
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = crud.order.get_by_user(db=db, user_id=current_user.id)
    return orders
