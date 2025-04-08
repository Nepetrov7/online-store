from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    description = Column(String(1000), nullable=False)
