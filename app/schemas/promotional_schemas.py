from datetime import datetime

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PromotionalCreate(BaseModel):
    promotion_name: str = Field(..., json_schema_extra={"example": "SuperSale"})
    discount_type: str = Field(..., json_schema_extra={"example": "percent"})
    discount_value: float = Field(..., json_schema_extra={"example": 10.75})
    start_date: datetime = Field(
        ..., json_schema_extra={"example": "2023-01-01T00:00:00"}
    )
    end_date: datetime = Field(
        ..., json_schema_extra={"example": "2023-02-01T00:00:00"}
    )
    applicable_product_ids: str = Field(..., json_schema_extra={"example": "{1,2,3}"})

    @field_validator("promotion_name")
    def validate_promotion_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Promotion name must not be empty")
        return value

    @field_validator("discount_value")
    def validate_discount_value(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Discount value must be positive")
        return value

    @field_validator("end_date")
    def validate_dates(cls, end_date: datetime, info: ValidationInfo) -> datetime:
        start_date = info.data.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("End date must be greater than start date")
        return end_date


class PromotionalOut(PromotionalCreate):
    id: int


class PromotionalDelete(BaseModel):
    id: int

    class ConfigDict:
        from_attributes = True
