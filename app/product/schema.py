from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Sample Product"})
    category_id: int = Field(..., json_schema_extra={"example": 1})
    price: float = Field(..., json_schema_extra={"example": 99.99})
    rating: float = Field(..., json_schema_extra={"example": 4.5})
    description: Optional[str] = Field(
        ..., json_schema_extra={"example": "A sample product description."}
    )

    @field_validator("name")
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value

    @field_validator("category_id")
    def category_id_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Category ID must be positive")
        return value

    @field_validator("price")
    def price_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @field_validator("rating")
    def rating_in_range(cls, value: float) -> float:
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5")
        return value

    @field_validator("description")
    def description_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Description must not be empty")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    description: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    final_price: Optional[float] = None  # Итоговая цена с учетом скидок

    model_config = {"from_attributes": True}


class ProductsList(BaseModel):
    items: List[ProductResponse]
