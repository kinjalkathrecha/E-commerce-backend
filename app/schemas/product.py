from pydantic import BaseModel

class ProductCreate(BaseModel):
    name:str
    description:str
    price:float

class ProductResponse(ProductCreate):
    id:int

    class config:
        from_attributes=True