import uvicorn
from fastapi import FastAPI

from app.models.user_models import Base as UserBase
from app.routers import auth, cart, products, promotional
from app.utils.db import engine


def create_app() -> FastAPI:
    app = FastAPI(title="Online store", version="0.1.0")

    # Создаём таблицы
    UserBase.metadata.create_all(bind=engine)

    # Подключаем роутеры
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(products.router, prefix="/products", tags=["Products"])
    app.include_router(promotional.router, prefix="/promotional", tags=["Promotional"])
    app.include_router(cart.router, prefix="/cart", tags=["Cart"])

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
