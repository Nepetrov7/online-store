from typing import List

from app.product.model import Product
from app.promotional.model import Promotional


def calculate_final_price(product: Product, promotions: List[Promotional]) -> float:
    """
    Вычисляет финальную цену товара на основе базовой цены и всех применимых промоакций.
    Для процентной скидки итоговая цена = цена * (1 - discount/100).
    Для фиксированной скидки итоговая цена = цена - discount.
    """
    final_price = float(product.price)
    for promo in promotions:
        dtype = promo.discount_type.lower()
        discount = float(promo.discount_value)
        if dtype in ("percent", "percentage"):
            final_price *= 1 - discount / 100
        elif dtype == "fixed":
            final_price -= discount
    return max(final_price, 0.0)
