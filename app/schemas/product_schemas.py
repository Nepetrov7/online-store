from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    category_id: int
    price: float
    rating: float
    description: str

class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True
