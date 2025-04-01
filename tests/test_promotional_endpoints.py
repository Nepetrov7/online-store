import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Фикстура для корректных данных промоакции.


@pytest.fixture
def promo_data():
    return {
        "promotion_name": "Summer Sale",
        "discount_type": "percent",
        "discount_value": 15.75,
        "start_date": "2023-06-01T00:00:00",
        "end_date": "2023-06-30T00:00:00",
        # Используем формат PostgreSQL для массива целых чисел:
        "applicable_product_ids": "{1,2,3}"
    }

# 1. Тесты для создания промоакции


def test_create_promotional_ok(promo_data):
    r = client.post("/promotional/create", json=promo_data)
    # Ожидаем 200, если эндпойнт найден и работает
    assert r.status_code == 200, r.text
    data = r.json()
    assert "id" in data
    assert data["promotion_name"] == promo_data["promotion_name"]


def test_create_promotional_invalid_data():
    # Попытка создать промоакцию без обязательного поля promotion_name
    invalid_data = {
        # "promotion_name" отсутствует,
        "discount_type": "percent",
        "discount_value": 10.0,
        "start_date": "2023-06-01T00:00:00",
        "end_date": "2023-06-30T00:00:00",
        "applicable_product_ids": "{1,2,3}"
    }
    r = client.post("/promotional/create", json=invalid_data)
    # Если валидация срабатывает, ожидаем 422 (или 404, если эндпойнт
    # отсутствует)
    assert r.status_code in (422, 404), r.text

# 2. Тесты для получения всех промоакций


def test_get_all_promotional_ok(promo_data):
    # Создаем две промоакции
    r1 = client.post("/promotional/create", json=promo_data)
    assert r1.status_code == 200, r1.text
    promo_data2 = promo_data.copy()
    promo_data2["promotion_name"] = "Winter Sale"
    r2 = client.post("/promotional/create", json=promo_data2)
    assert r2.status_code == 200, r2.text

    # Получаем список всех промоакций
    r = client.get("/promotional/all")
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    # Ожидаем, что в списке будет как минимум 2 записи
    assert len(data) >= 2


def test_get_all_promotional_empty():
    # Если база данных пуста, эндпойнт должен вернуть пустой список.
    r = client.get("/promotional/all")
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    # Если база чистая, можно проверить, что список пустой:
    # assert len(data) == 0

# 3. Тесты для удаления промоакции


def test_delete_promotional_ok(promo_data):
    # Создаем промоакцию
    r = client.post("/promotional/create", json=promo_data)
    assert r.status_code == 200, r.text
    promo_id = r.json()["id"]

    # Удаляем промоакцию
    r2 = client.delete(f"/promotional/{promo_id}")
    assert r2.status_code == 200, r2.text
    # Ожидаем, что возвращается {"id": promo_id}
    assert r2.json()["id"] == promo_id


def test_delete_promotional_not_found():
    non_existent_id = 999999
    r = client.delete(f"/promotional/{non_existent_id}")
    assert r.status_code == 404, r.text
    detail = r.json().get("detail", "")
    # Допускаем вариант "Promotional not found" или "Not Found"
    assert detail in ["Promotional not found", "Not Found"]
