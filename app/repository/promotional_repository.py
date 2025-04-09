from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.promotional_models import Promotional


class PromotionalRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_promotional(
        self,
        promotion_name: str,
        discount_type: str,
        discount_value: float,
        start_date: datetime,
        end_date: datetime,
        applicable_product_ids: str,
    ) -> Promotional:
        promotional = Promotional(
            promotion_name=promotion_name,
            discount_type=discount_type,
            discount_value=discount_value,
            start_date=start_date,
            end_date=end_date,
            applicable_product_ids=applicable_product_ids,
        )
        self.session.add(promotional)
        self.session.commit()
        self.session.refresh(promotional)
        return promotional

    def get_active_promotions_for_product(self, product_id: int) -> List[Promotional]:
        """
        Пример: выбираем все промоакции, для которых product_id
        встречается в строковом поле applicable_product_ids.
        Здесь можно добавить фильтрацию по дате, если нужно
        (т.е. акции должны быть активны)
        """
        all_promos = self.session.query(Promotional).all()
        active_promos = []
        for promo in all_promos:
            # Преобразуем строку в список целых чисел
            try:
                # Убираем фигурные скобки и разделяем по запятым
                ids = [
                    int(x.strip())
                    for x in promo.applicable_product_ids.strip("{}").split(",")
                    if x.strip().isdigit()
                ]
            except Exception:
                ids = []
            # Если продукт есть среди указанных, добавляем акцию
            if product_id in ids:
                # Если требуется проверить активность акции по дате:
                now = datetime.now(timezone.utc)
                if promo.start_date <= now <= promo.end_date:
                    active_promos.append(promo)
        return active_promos

    def get_all_promotional(self) -> Optional[Promotional]:
        return self.session.query(Promotional).all()

    def get_promotional_by_id(self, promotional_id: int) -> Optional[Promotional]:
        return (
            self.session.query(Promotional)
            .filter(Promotional.id == promotional_id)
            .first()
        )

    def delete_promotional(self, promotional_id: int) -> bool:
        promotional = (
            self.session.query(Promotional)
            .filter(Promotional.id == promotional_id)
            .first()
        )
        if not promotional:
            return False
        self.session.delete(promotional)
        self.session.commit()
        return True
