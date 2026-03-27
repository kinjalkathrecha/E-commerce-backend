from typing import Optional, List
from pydantic import BaseModel

class SectionBase(BaseModel):
    name: str
    category_id: int

class SectionCreate(SectionBase):
    pass

class SectionUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None

class SectionResponse(SectionBase):
    id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    sections: List[SectionResponse] = []

    class Config:
        from_attributes = True
