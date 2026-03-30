from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User, UserRole, Address
from app.schemas.user import UserCreate, UserUpdate, UserRoleCreate, AddressCreate, AddressUpdate

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
