from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.utils.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    # например: "user", "read_only", "admin"
    role = Column(String(50), default="user")
    cart_items = relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan",
    )
