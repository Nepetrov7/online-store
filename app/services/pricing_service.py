from typing import List

from app.models.promotional_models import Promotional
from app.product.model import Product


def calculate_final_price(product: Product, promotions: List[Promotional]) -> float:
    """
    Вычисляет финальную цену товара на основе базовой цены и всех применимых промоакций.
    Для процентной скидки итоговая цена = цена * (1 - discount/100).
    Для фиксированной скидки итоговая цена = цена - discount.
    """
    final_price = product.price
    for promo in promotions:
        if promo.discount_type.lower() == "percent":
            final_price *= 1 - promo.discount_value / 100
        elif promo.discount_type.lower() == "fixed":
            final_price -= promo.discount_value

    return max(final_price, 0)
