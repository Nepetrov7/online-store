from pydantic import BaseModel, Field
from datetime import datetime


class PromotionalCreate(BaseModel):
    promotion_name: str = Field(..., example="SuperSale")
    discount_type: str = Field(..., example="percent")
    discount_value: float = Field(..., example=10.75)
    start_date: datetime = Field(..., example="2023-01-01T00:00:00")
    end_date: datetime = Field(..., example="2023-02-01T00:00:00")
    applicable_product_ids: str = Field(..., example="{1,2,3}")


class PromotionalOut(PromotionalCreate):
    id: int


class PromotionalDelete(BaseModel):
    id: int

    class ConfigDict:
        from_attributes = True
