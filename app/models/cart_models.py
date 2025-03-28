from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
