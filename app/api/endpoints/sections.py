from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.category import SectionCreate, SectionUpdate, SectionResponse
from app import crud
from app.core.dependencies import get_db, get_current_active_admin

router = APIRouter()

@router.get("/", response_model=List[SectionResponse])
def get_sections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sections = crud.section.get_multi(db, skip=skip, limit=limit)
    return sections

@router.get("/{section_id}", response_model=SectionResponse)
def get_section(section_id: int, db: Session = Depends(get_db)):
    section = crud.section.get(db=db, id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.post("/", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(
    section: SectionCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_admin)
):
    category = crud.category.get(db=db, id=section.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    new_section = crud.section.create(db=db, obj_in=section)
    return new_section

@router.patch("/{section_id}", response_model=SectionResponse)
def update_section(
    section_id: int, 
    section: SectionUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_admin)
):
    db_section = crud.section.get(db=db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    if section.category_id is not None:
        category = crud.category.get(db=db, id=section.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    updated_section = crud.section.update(db=db, db_obj=db_section, obj_in=section)
    return updated_section

@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_section(
    section_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_admin)
):
    db_section = crud.section.get(db=db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    crud.section.remove(db=db, id=section_id)
    return None

@router.get("/category/{category_id}", response_model=List[SectionResponse])
def get_sections_by_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    sections = crud.section.get_by_category(db=db, category_id=category_id)
    return sections
