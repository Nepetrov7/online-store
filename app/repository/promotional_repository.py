from sqlalchemy.orm import Session
from app.models.promotional_models import Promotional
from typing import Optional
from datetime import date


class PromotionalRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_promotional(self, promotion_name: str, discount_type: str, discount_value: float,
                           start_date: date, end_date: date, applicable_product_ids: str) -> Promotional:
        promotional = Promotional(
            promotion_name=promotion_name,
            discount_type=discount_type,
            discount_value=discount_value,
            start_date=start_date,
            end_date=end_date,
            applicable_product_ids=applicable_product_ids
        )

        self.session.add(promotional)
        self.session.commit()
        self.session.refresh(promotional)
        return promotional

    def get_all_promotional(self) -> Optional[Promotional]:
        return (
            self.session.query(Promotional)
            .all()
        )

    def get_promotional_by_id(
            self, promotional_id: int) -> Optional[Promotional]:
        return self.session.query(Promotional).filter(
            Promotional.id == promotional_id).first()

    def delete_promotional(self, promotional_id: int) -> bool:
        promotional = self.session.query(Promotional).filter(
            Promotional.id == promotional_id).first()
        if not promotional:
            return False
        self.session.delete(promotional)
        self.session.commit()
        return True
