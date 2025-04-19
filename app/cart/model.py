from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.utils.base import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Связи для удобства
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product")
