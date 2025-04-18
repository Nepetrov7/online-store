import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Фикстура для регистрации и получения токена
@pytest.fixture(scope="function")
def auth_token():
    register_data = {
        "username": "testcartuser",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "Cart",
        "role": "user",
    }
    r = client.post("/auth/register", json=register_data)
    assert r.status_code in (200, 400), r.text

    login_data = {"username": "testcartuser", "password": "testpass"}
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


# Фикстура для создания двух продуктов через API
@pytest.fixture(scope="function")
def products(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Обязательно указать rating, как требуют схемы
    prod1 = {
        "name": "CartProd1",
        "price": 10.0,
        "rating": 4.0,
        "description": "Desc1",
        "category_id": 1,
    }
    prod2 = {
        "name": "CartProd2",
        "price": 20.0,
        "rating": 3.5,
        "description": "Desc2",
        "category_id": 1,
    }
    r1 = client.post("/products/", json=prod1, headers=headers)
    assert r1.status_code == 200, r1.text
    id1 = r1.json()["id"]

    r2 = client.post("/products/", json=prod2, headers=headers)
    assert r2.status_code == 200, r2.text
    id2 = r2.json()["id"]

    return id1, id2


@pytest.mark.parametrize(
    "quantity,expected_qty",
    [
        (2, 2),
        (3, 3),
    ],
)
def test_add_new_item(auth_token, products, quantity, expected_qty):
    headers = {"Authorization": f"Bearer {auth_token}"}
    product_id, _ = products
    r = client.post(
        "/cart/", json={"product_id": product_id, "quantity": quantity}, headers=headers
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["product_id"] == product_id
    assert data["quantity"] == expected_qty


def test_add_existing_item(auth_token, products):
    headers = {"Authorization": f"Bearer {auth_token}"}
    product_id, _ = products
    client.post(
        "/cart/", json={"product_id": product_id, "quantity": 1}, headers=headers
    )
    r = client.post(
        "/cart/", json={"product_id": product_id, "quantity": 2}, headers=headers
    )
    assert r.status_code == 201, r.text
    assert r.json()["quantity"] == 3


@pytest.mark.parametrize(
    "init_qty,update_qty,expected_qty",
    [
        (1, 5, 5),
        (4, 2, 2),
    ],
)
def test_update_item_quantity(auth_token, products, init_qty, update_qty, expected_qty):
    headers = {"Authorization": f"Bearer {auth_token}"}
    _, product_id = products
    r = client.post(
        "/cart/", json={"product_id": product_id, "quantity": init_qty}, headers=headers
    )
    item_id = r.json()["id"]
    r2 = client.put(f"/cart/{item_id}", json={"quantity": update_qty}, headers=headers)
    assert r2.status_code == 200, r2.text
    assert r2.json()["quantity"] == expected_qty


def test_delete_item(auth_token, products):
    headers = {"Authorization": f"Bearer {auth_token}"}
    product_id, _ = products
    r = client.post(
        "/cart/", json={"product_id": product_id, "quantity": 1}, headers=headers
    )
    item_id = r.json()["id"]
    r2 = client.delete(f"/cart/{item_id}", headers=headers)
    assert r2.status_code == 204, r2.text
    items = client.get("/cart/", headers=headers).json()["items"]
    assert all(i["id"] != item_id for i in items)


def test_clear_cart(auth_token, products):
    headers = {"Authorization": f"Bearer {auth_token}"}
    pid1, pid2 = products
    client.post("/cart/", json={"product_id": pid1, "quantity": 1}, headers=headers)
    client.post("/cart/", json={"product_id": pid2, "quantity": 1}, headers=headers)
    r = client.delete("/cart/", headers=headers)
    assert r.status_code == 204, r.text
    assert client.get("/cart/", headers=headers).json()["items"] == []
