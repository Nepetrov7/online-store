from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Table

from app.utils.base import Base

promotion_products = Table(
    "promotion_products",
    Base.metadata,
    Column(
        "promotion_id",
        Integer,
        ForeignKey("promotions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Promotional(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    promotion_name = Column(String(255), nullable=False)
    discount_type = Column(String(50), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
