from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text

from app.models.base import Base


class Promotional(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    promotion_name = Column(String(255), nullable=False)
    discount_type = Column(String(50), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
