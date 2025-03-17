import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app

client = TestClient(app)

# ---------------------------------------------------------
# 1. Вспомогательная фикстура для регистрации + логина
# ---------------------------------------------------------
@pytest.fixture
def auth_token():
    """
    Регистрирует и логинит тестового пользователя.
    Возвращает access_token (Bearer).
    """
    # 1. Регистрируем
    register_data = {
        "first_name": "Test",
		"last_name": "User",
        "username": "testuser",
        "password": "testpass",
        "role": "user"
    }
    r = client.post("/auth/register", json=register_data)
    assert r.status_code in (200, 400), r.text
    # Если пользователь уже существует, вернётся 400, тогда продолжаем

    # 2. Логиним
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    r = client.post("/auth/login", json=login_data)
    assert r.status_code == 200, r.text

    token = r.json()["access_token"]
    return token


# ---------------------------------------------------------
# 2. Тестируем эндпойнты /auth
# ---------------------------------------------------------

def test_register_new_user():
    """
    Проверяем успешную регистрацию нового пользователя.
    """
    data = {
		"first_name": "Test",
		"last_name": "User",
        "username": "unique_user",
        "password": "pass123",
        "role": "user"
    }
    r = client.post("/auth/register", json=data)
    # Могут быть 200 (успешно) или 400 (если такой user уже есть)
    assert r.status_code in (200, 400)

def test_login_wrong_password():
    """
    Проверяем, что при неверном пароле вернётся 401.
    """
    data = {
        "username": "testuser",   # фиктивный или существующий
        "password": "wrongpass"
    }
    r = client.post("/auth/login", json=data)
    assert r.status_code == 401, r.text

def test_logout(auth_token):
    """
    Проверяем, что logout работает (200).
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/auth/logout", headers=headers)
    assert r.status_code == 200, r.text
