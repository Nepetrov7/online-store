import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Фикстура для регистрации и логина тестового пользователя.
@pytest.fixture
def auth_token():
    register_data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "password": "testpass",
        "role": "user",
    }
    r = client.post("/auth/register", json=register_data)
    # Если пользователь уже существует — допускаем 200 или 400
    assert r.status_code in (200, 400), r.text

    login_data = {"username": "testuser", "password": "testpass"}
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.mark.parametrize(
    "register_data,expected_status",
    [
        # Корректные данные: регистрация проходит (200) или уже существует (400)
        (
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "unique_user1",
                "password": "pass123",
                "role": "user",
            },
            (200, 400),
        ),
        # Отсутствует обязательное поле first_name – ожидаем ошибку (422)
        (
            {
                "last_name": "User",
                "username": "unique_user2",
                "password": "pass123",
                "role": "user",
            },
            422,
        ),
        # Пустой пароль – ожидаем ошибку (422)
        (
            {
                "first_name": "Test",
                "last_name": "User",
                "username": "unique_user3",
                "password": "",
                "role": "user",
            },
            422,
        ),
    ],
)
def test_register_user(register_data, expected_status):
    r = client.post("/auth/register", json=register_data)
    if isinstance(expected_status, tuple):
        assert r.status_code in expected_status, r.text
    else:
        assert r.status_code == expected_status, r.text


# Параметризованный тест для логина с неверными данными.
@pytest.mark.parametrize(
    "login_data,expected_status",
    [
        ({"username": "testuser", "password": "wrongpass"}, 401),
        ({"username": "nonexistent", "password": "pass"}, 422),
        ({"username": "testuser", "password": ""}, 422),
    ],
)
def test_login_wrong(login_data, expected_status):
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == expected_status, r.text


# Тест для корректного логаута с валидным токеном.
def test_logout(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/auth/logout", headers=headers)
    assert r.status_code == 204, r.text


# Параметризованный тест для логаута с некорректными токенами.
@pytest.mark.parametrize(
    "invalid_token,expected_status",
    [
        ("", 401),
        ("invalidtoken", 401),
        ("Bearer", 401),
    ],
)
def test_logout_invalid(invalid_token, expected_status):
    # Передаем токен из параметра, даже если он некорректен.
    headers = {"Authorization": f"Bearer {invalid_token}"}
    r = client.post("/auth/logout", headers=headers)
    assert r.status_code == expected_status, r.text
