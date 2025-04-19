import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def auth_token():
    register_data = {
        "username": "promo_user",
        "password": "promopass",
        "first_name": "Promo",
        "last_name": "Tester",
        "role": "user",
    }
    # Регистрация и логин (если пользователь уже существует, допускаем 400)
    r = client.post("/auth/register", json=register_data)
    assert r.status_code in (200, 400), r.text
    r = client.post(
        "/auth/login",
        json={
            "username": register_data["username"],
            "password": register_data["password"],
        },
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.fixture(scope="function")
def promo_data():
    return {
        "promotion_name": "Spring Sale",
        "discount_type": "percentage",
        "discount_value": 15.0,
        "start_date": "2025-05-01T00:00:00",
        "end_date": "2025-05-10T23:59:59",
    }


# Изменено: теперь просто проверяем, что возвращается список
def test_list_promotional_returns_list():
    r = client.get("/promotional/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_promotional_ok(auth_token, promo_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/promotional/", json=promo_data, headers=headers)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data.get("promotion_name") == promo_data["promotion_name"]
    assert data.get("discount_type") == promo_data["discount_type"]
    assert float(data.get("discount_value", 0)) == promo_data["discount_value"]


def test_create_promotional_invalid_data(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Пропустим обязательное discount_type
    invalid = {
        "promotion_name": "Bad Promo",
        "discount_value": 1.0,
        "start_date": "2025-05-01T00:00:00",
        "end_date": "2025-05-10T23:59:59",
    }
    r = client.post("/promotional/", json=invalid, headers=headers)
    assert r.status_code == 422


def test_get_all_promotional_ok(auth_token, promo_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Создаём одну акцию
    client.post("/promotional/", json=promo_data, headers=headers)
    r = client.get("/promotional/")
    assert r.status_code == 200
    items = r.json()
    # Должен присутствовать хотя бы один элемент с нашими данными
    assert any(
        item.get("promotion_name") == promo_data["promotion_name"] for item in items
    )


def test_delete_promotional_ok(auth_token, promo_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r1 = client.post("/promotional/", json=promo_data, headers=headers)
    pid = r1.json()["id"]
    r2 = client.delete(f"/promotional/{pid}", headers=headers)
    assert r2.status_code == 204
    # далее GET по тому же id — 404
    r3 = client.get(f"/promotional/{pid}")
    assert r3.status_code == 404


def test_delete_promotional_not_found(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.delete("/promotional/999999", headers=headers)
    assert r.status_code == 404
