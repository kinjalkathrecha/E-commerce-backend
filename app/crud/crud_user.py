from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User, UserRole, Address, PromoCode, CustomerSupport, BecomeSeller, BulkInquiry
from app.schemas.user import (
    UserCreate, UserUpdate, UserRoleCreate, AddressCreate, AddressUpdate,
    PromoCodeCreate, PromoCodeBase, CustomerSupportCreate, CustomerSupportUpdate,
    BecomeSellerCreate, BecomeSellerUpdate, BulkInquiryCreate, BulkInquiryBase
)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleCreate]):
    def get_by_name(self, db: Session, *, role_name: str) -> Optional[UserRole]:
        return db.query(UserRole).filter(UserRole.role_name == role_name).first()

class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[Address]:
        return db.query(Address).filter(Address.user_id == user_id).all()

user = CRUDUser(User)
user_role = CRUDUserRole(UserRole)
address = CRUDAddress(Address)

class CRUDPromoCode(CRUDBase[PromoCode, PromoCodeCreate, PromoCodeBase]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[PromoCode]:
        return db.query(PromoCode).filter(PromoCode.code == code).first()

class CRUDCustomerSupport(CRUDBase[CustomerSupport, CustomerSupportCreate, CustomerSupportUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[CustomerSupport]:
        return db.query(CustomerSupport).filter(CustomerSupport.user_id == user_id).all()

    def create_with_user(self, db: Session, *, obj_in: CustomerSupportCreate, user_id: int) -> CustomerSupport:
        from fastapi.encoders import jsonable_encoder
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDBecomeSeller(CRUDBase[BecomeSeller, BecomeSellerCreate, BecomeSellerUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> Optional[BecomeSeller]:
        return db.query(BecomeSeller).filter(BecomeSeller.user_id == user_id).first()

    def create_with_user(self, db: Session, *, obj_in: BecomeSellerCreate, user_id: int) -> BecomeSeller:
        from fastapi.encoders import jsonable_encoder
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDBulkInquiry(CRUDBase[BulkInquiry, BulkInquiryCreate, BulkInquiryBase]):
    pass

promo_code = CRUDPromoCode(PromoCode)
customer_support = CRUDCustomerSupport(CustomerSupport)
become_seller = CRUDBecomeSeller(BecomeSeller)
bulk_inquiry = CRUDBulkInquiry(BulkInquiry)
