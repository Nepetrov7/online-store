import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.cart import router as cart
from app.product import router as product
from app.promotional import router as promotional
from app.user import router as user
from app.user.model import Base as UserBase
from app.utils.db import engine


def create_app() -> FastAPI:
    app = FastAPI(title="Online store", version="0.1.0")

    # CORS
    # список разрешённых origin — подставьте URL вашего фронтенда
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        # "https://online",добавить реальный адрес frontend в продакшене
        # можно указать "*" для разрешения всех, но это не рекомендуется в продакшене
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Создаём таблицы
    UserBase.metadata.create_all(bind=engine)

    # Подключаем роутеры
    app.include_router(user.router, prefix="/auth", tags=["Auth"])
    app.include_router(product.router, prefix="/products", tags=["Products"])
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
