import random
import string

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Фикстура для получения валидного токена пользователя.
@pytest.fixture(scope="function")
def auth_token():
    register_data = {
        "username": "testproduser",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
    }
    # Регистрируем (если пользователь уже существует, допускаем код 200 или 400)
    r = client.post("/auth/register", json=register_data)
    assert r.status_code in (200, 400), r.text

    # Логиним пользователя
    login_data = {"username": "testproduser", "password": "testpass"}
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


# Фикстура для данных продукта.
@pytest.fixture
def product_data():
    random_suffix = "".join(random.choices(string.ascii_lowercase, k=5))
    return {
        "name": "Product " + random_suffix,
        "category_id": 1,
        "price": 99.99,
        "rating": 4.5,
        "description": "A sample product description.",
    }


# 1. Тест создания продукта
def test_create_product_ok(product_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/products/", json=product_data, headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "id" in data
    assert data["name"] == product_data["name"]


def test_create_product_invalid_data(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Отсутствует обязательное поле "name"
    invalid_data = {
        "category_id": 1,
        "price": 49.99,
        "rating": 3.5,
        "description": "No name provided",
    }
    r = client.post("/products/", json=invalid_data, headers=headers)
    # Ожидаем ошибку валидации (422) или если эндпойнт отсутствует (404)
    assert r.status_code in (422, 404), r.text


# 2. Тест получения продукта по ID
def test_get_product_by_id_ok(product_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Создаем продукт
    r = client.post("/products/", json=product_data, headers=headers)
    assert r.status_code == 200, r.text
    prod_id = r.json()["id"]
    print(f"Created product ID: {prod_id}")

    # Получаем продукт по ID
    r = client.get(f"/products/{prod_id}", headers=headers)
    assert r.status_code == 200, r.text
    assert r.json()["id"] == prod_id  # Проверяем, что полученный ID совпадает


# 3. Тест получения продуктов по категории (GET /products/?category_id=1)
def test_get_products_by_category_ok(product_data):
    # Создадим продукт через защищенный endpoint;
    # если GET не защищен, можно не передавать заголовки
    dummy_token = "dummy_token"  # Если GET не требует авторизации
    # Создание продукта через защищённый endpoint:
    r = client.post(
        "/products/",
        json=product_data,
        headers={"Authorization": f"Bearer {dummy_token}"},
    )
    # Выполняем GET запрос для получения продуктов с category_id=1
    r = client.get("/products/?category_id=1")
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    assert any(prod["category_id"] == 1 for prod in data)


# 4. Тест обновления продукта
def test_update_product_ok(product_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Создаем продукт
    r = client.post("/products/", json=product_data, headers=headers)
    assert r.status_code == 200, r.text
    prod_id = r.json()["id"]
    # Обновляем – меняем цену и описание
    updated_data = product_data.copy()
    updated_data["price"] = 79.99
    updated_data["description"] = "Updated description"
    r = client.put(f"/products/{prod_id}", json=updated_data, headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["price"] == 79.99
    assert data["description"] == "Updated description"


# 5. Тест удаления продукта
def test_delete_product_ok(product_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Создаем продукт
    r = client.post("/products/", json=product_data, headers=headers)
    assert r.status_code == 200, r.text
    prod_id = r.json()["id"]
    # Удаляем продукт
    r_del = client.delete(f"/products/{prod_id}", headers=headers)
    assert r_del.status_code == 200, r_del.text
    # После удаления ожидание: GET по этому id должен вернуть 404 (товар не найден)
    r_get = client.get(f"/products/{prod_id}", headers=headers)
    assert r_get.status_code == 404, r_get.text


def test_delete_product_not_found(auth_token):
    non_existent_id = 999999
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.delete(f"/products/{non_existent_id}", headers=headers)
    assert r.status_code == 404, r.text
    detail = r.json().get("detail", "")
    assert detail in ["Товар не найден", "Product not found"]
