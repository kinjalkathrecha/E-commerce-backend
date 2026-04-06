from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserRoleBase(BaseModel):
    role_name: str

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleResponse(UserRoleBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None
    password: Optional[str] = Field(None, min_length=6, max_length=72)

class UserResponse(UserBase):
    id: int
    role: Optional[UserRoleResponse] = None

    class Config:
        from_attributes = True

class BulkInquiryBase(BaseModel):
    company_individual_name: str
    contact_person_name: str
    preferred_contact_method: Optional[str] = None
    email: EmailStr
    whatsapp_number: str
    require_customization: bool = False
    budget_range: str
    delivery_timeframe_value: Optional[int] = None
    delivery_timeframe_unit: Optional[str] = None
    additional_requirements: Optional[str] = None
    preferred_contact_datetime: datetime
    product_id: Optional[int] = None
    inquiry_type: str = "General"

class BulkInquiryCreate(BulkInquiryBase):
    pass

class BulkInquiryResponse(BulkInquiryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AddressBase(BaseModel):
    address_line: str
    city: str
    state: str
    postal_code: str
    phone_number: str
    address_type: Optional[str] = None

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None
    address_type: Optional[str] = None

class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class PromoCodeBase(BaseModel):
    code: str
    discount_percentage: float
    is_active: bool = True
    expiry_date: Optional[datetime] = None
    seller_id: Optional[int] = None

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeResponse(PromoCodeBase):
    id: int

    class Config:
        from_attributes = True

class BecomeSellerBase(BaseModel):
    business_name: str
    gst_number: str
    pan_card: str
    store_description: Optional[str] = None

class BecomeSellerCreate(BecomeSellerBase):
    pass

class BecomeSellerUpdate(BaseModel):
    is_reviewed: Optional[bool] = None
    admin_status: Optional[str] = None

class BecomeSellerResponse(BecomeSellerBase):
    id: int
    user_id: int
    is_reviewed: bool
    admin_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class CustomerSupportBase(BaseModel):
    order_id: Optional[int] = None
    subject: str
    message: str
    priority: str = "Medium"

class CustomerSupportCreate(CustomerSupportBase):
    pass

class CustomerSupportUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class CustomerSupportResponse(CustomerSupportBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None