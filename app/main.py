import uvicorn
from fastapi import FastAPI
from app.models.user_models import Base as UserBase
from app.models.product_models import Product
from app.utils.db import engine
from app.routers import auth, products, cart

def create_app() -> FastAPI:
    app = FastAPI(title="Online store", version="0.1.0")

    # Создаём таблицы
    UserBase.metadata.create_all(bind=engine)

    # Подключаем роутеры
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(products.router, prefix="/products", tags=["Products"])  
    

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
