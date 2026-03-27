from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.category import Category, Section
from app.schemas.category import CategoryCreate, CategoryUpdate, SectionCreate, SectionUpdate

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Category]:
        return db.query(Category).filter(Category.slug == slug).first()

class CRUDSection(CRUDBase[Section, SectionCreate, SectionUpdate]):
    def get_by_category(self, db: Session, *, category_id: int) -> List[Section]:
        return db.query(Section).filter(Section.category_id == category_id).all()

category = CRUDCategory(Category)
section = CRUDSection(Section)
