from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import BulkInquiryCreate, BulkInquiryResponse
from app import crud
from app.core.dependencies import get_db, get_current_active_admin

router = APIRouter()

@router.post("/", response_model=BulkInquiryResponse, status_code=status.HTTP_201_CREATED)
def create_bulk_inquiry(
    *,
    db: Session = Depends(get_db),
    inquiry_in: BulkInquiryCreate,
) -> Any:
    """Submit a new bulk inquiry (Public)."""
    inquiry = crud.bulk_inquiry.create(db, obj_in=inquiry_in)
    return inquiry

@router.get("/", response_model=List[BulkInquiryResponse])
def read_bulk_inquiries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Any = Depends(get_current_active_admin)
) -> Any:
    """Retrieve all bulk inquiries (Admin only)."""
    return crud.bulk_inquiry.get_multi(db, skip=skip, limit=limit)
