from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.promotional_models import Promotional
from app.repository.promotional_repository import PromotionalRepository
from app.schemas.promotional_schemas import PromotionalCreate, PromotionalUpdate


class PromotionalService:
    def __init__(self, db: Session):
        self.repo = PromotionalRepository(db)

    def list_promos(self) -> List[Promotional]:
        now = datetime.now(timezone.utc).date()
        return [p for p in self.repo.get_all() if p.end_date >= now]

    def get_promo(self, promo_id: int) -> Optional[Promotional]:
        return self.repo.get_by_id(promo_id)

    def create_promo(self, data: PromotionalCreate) -> Promotional:
        promo = Promotional(**data.model_dump())
        return self.repo.create(promo)

    def update_promo(
        self, promo_id: int, data: PromotionalUpdate
    ) -> Optional[Promotional]:
        promo = self.repo.get_by_id(promo_id)
        if not promo:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(promo, field, value)
        return self.repo.update(promo)

    def delete_promo(self, promo_id: int) -> bool:
        promo = self.repo.get_by_id(promo_id)
        if not promo:
            return False
        self.repo.delete(promo)
        return True
