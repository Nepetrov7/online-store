# 🚀 Запуск проекта

Чтобы запустить проект на локальной машине, выполните следующие шаги:

1. **Клонируйте репозиторий:**

    ```bash
    git clone git@github.com:Nepetrov7/online-store.git
    ```

2. **Перейдите в директорию проекта:**

    ```bash
    cd online-store
    ```

3. **Создаём файл .env, переменные берём из .env.sample**

	```bash
	cp .env.sample .env
	```

4. **Переключиться на ветку:**

    ```bash
    git checkout -b minor/вашНикGithub
    ```

5. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

6. **Запустите проект:**

    ```bash
    python -m app.main
    ```

7. **Запустите тесты:**

    ```bash
    pytest
    ```

8. **Проверьте работу приложения:**

    Откройте в браузере http://127.0.0.1:8000 или перейдите по адресу документации http://127.0.0.1:8000/docs. Документы хранятся по пути ./app/storage

# вариант со сборкой образа и поднятием приложения в контейнере

1. собираем образ

```bash
docker built online-store .
```

2.1. поднимаем контейнер - вариант для тестов

```
docker-compose up
```

2.2. поднимаем контейнер - вариант для сервера

```
docker-compose up -d
```

## 👤 Авторы

Команда "Слизерин"

[GitHub](https://github.com/Nepetrov7/online-store) репа

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT.
