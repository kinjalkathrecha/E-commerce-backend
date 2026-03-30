from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import AddressCreate, AddressUpdate, AddressResponse
from app import crud
from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[AddressResponse])
def get_addresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.address.get_by_user(db=db, user_id=current_user.id)

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(address: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    addr_dict = address.model_dump()
    addr_dict["user_id"] = current_user.id
    new_address = crud.address.create(db=db, obj_in=addr_dict)
    return new_address

@router.patch("/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_address = crud.address.get(db=db, id=address_id)
    if not db_address or db_address.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Address not found")
    
    updated_address = crud.address.update(db=db, db_obj=db_address, obj_in=address)
    return updated_address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_address = crud.address.get(db=db, id=address_id)
    if not db_address or db_address.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Address not found")
    crud.address.remove(db=db, id=address_id)
    return None
