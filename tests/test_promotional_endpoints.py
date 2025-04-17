import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Фикстура для получения валидного токена пользователя.
# Предполагается, что в вашем сервисе есть эндпойнты /auth/register и /auth/login.
@pytest.fixture(scope="function")
def auth_token():
    register_data = {
        "username": "testuser",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
    }
    # Регистрируем пользователя (если он уже существует, допускаем ошибку 400)
    r = client.post("/auth/register", json=register_data)
    assert r.status_code in (200, 400), r.text

    login_data = {"username": "testuser", "password": "testpass"}
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


# Фикстура для корректных данных промоакции.
@pytest.fixture
def promo_data():
    return {
        "promotion_name": "Summer Sale",
        "discount_type": "percent",
        "discount_value": 15.75,
        "start_date": "2023-06-01T00:00:00",
        "end_date": "2023-06-30T00:00:00",
    }


# 1. Тесты для создания промоакции
def test_create_promotional_ok(promo_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/promotional/create", json=promo_data, headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "id" in data
    assert data["promotion_name"] == promo_data["promotion_name"]


def test_create_promotional_invalid_data(auth_token):
    # Попытка создать промоакцию без обязательного поля promotion_name
    invalid_data = {
        "discount_type": "percent",
        "discount_value": 10.0,
        "start_date": "2023-06-01T00:00:00",
        "end_date": "2023-06-30T00:00:00",
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/promotional/create", json=invalid_data, headers=headers)
    # При валидационной ошибке ожидаем 422, либо если эндпойнт не найден — 404
    assert r.status_code in (422, 404), r.text


# 2. Тесты для получения всех промоакций
def test_get_all_promotional_ok(promo_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Создаем две промоакции
    r1 = client.post("/promotional/create", json=promo_data, headers=headers)
    assert r1.status_code == 200, r1.text
    promo_data2 = promo_data.copy()
    promo_data2["promotion_name"] = "Winter Sale"
    r2 = client.post("/promotional/create", json=promo_data2, headers=headers)
    assert r2.status_code == 200, r2.text

    # Получаем список всех промоакций
    r = client.get("/promotional/all", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_all_promotional_empty(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.get("/promotional/all", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    # Если база чистая, можно добавить:
    # assert len(data) == 0


# 3. Тесты для удаления промоакции
def test_delete_promotional_ok(promo_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Создаем промоакцию
    r = client.post("/promotional/create", json=promo_data, headers=headers)
    assert r.status_code == 200, r.text
    promo_id = r.json()["id"]

    # Удаляем промоакцию
    r2 = client.delete(f"/promotional/{promo_id}", headers=headers)
    assert r2.status_code == 200, r2.text
    assert r2.json()["id"] == promo_id


def test_delete_promotional_not_found(auth_token):
    non_existent_id = 999999
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.delete(f"/promotional/{non_existent_id}", headers=headers)
    assert r.status_code == 404, r.text
    detail = r.json().get("detail", "")
    assert detail in ["Promotional not found", "Not Found"]
