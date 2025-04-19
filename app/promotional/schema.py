# app/schemas/promotional_schemas.py

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PromotionalBase(BaseModel):
    promotion_name: str
    discount_type: str
    discount_value: Decimal
    start_date: datetime
    end_date: datetime


class PromotionalCreate(PromotionalBase):
    pass


class PromotionalUpdate(BaseModel):
    promotion_name: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PromotionalResponse(PromotionalBase):
    id: int

    # Pydantic v2: берем атрибуты из ORM
    model_config = ConfigDict(from_attributes=True)


# не обязательно, если вы отдаете прямо List[PromotionalResponse]
class PromotionalList(BaseModel):
    items: List[PromotionalResponse]
