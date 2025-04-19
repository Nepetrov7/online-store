from typing import List, Optional

from sqlalchemy.orm import Session

from app.promotional.model import Promotional


class PromotionalRepository:
    def __init__(self, db: Session):
        self.session = db

    def get_all(self) -> List[Promotional]:
        return self.session.query(Promotional).all()

    def get_by_id(self, promo_id: int) -> Optional[Promotional]:
        return (
            self.session.query(Promotional).filter(Promotional.id == promo_id).first()
        )

    def create(self, promo: Promotional) -> Promotional:
        self.session.add(promo)
        self.session.commit()
        self.session.refresh(promo)
        return promo

    def update(self, promo: Promotional) -> Promotional:
        self.session.add(promo)
        self.session.commit()
        self.session.refresh(promo)
        return promo

    def delete(self, promo: Promotional) -> None:
        self.session.delete(promo)
        self.session.commit()
