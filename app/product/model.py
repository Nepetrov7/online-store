from sqlalchemy import Column, Float, Integer, String

from app.utils.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    description = Column(String(1000), nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
