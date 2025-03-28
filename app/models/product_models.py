from sqlalchemy import Column, Integer, String, Float
from app.models.user_models import Base 

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
