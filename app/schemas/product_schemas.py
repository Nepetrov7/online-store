from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float

class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True
