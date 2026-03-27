from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserRoleCreate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleCreate]):
    def get_by_name(self, db: Session, *, role_name: str) -> Optional[UserRole]:
        return db.query(UserRole).filter(UserRole.role_name == role_name).first()

user = CRUDUser(User)
user_role = CRUDUserRole(UserRole)
