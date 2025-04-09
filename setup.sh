#!/bin/bash

# Название виртуального окружения
VENV_DIR="venv"

# Проверка, установлен ли Python
if ! command -v python &> /dev/null; then
    echo "❌ Python не установлен. Установи его"
    exit 1
fi

# Создание виртуального окружения, если его ещё нет
if [ ! -d "$VENV_DIR" ]; then
    echo "🌀 Создаю виртуальное окружение в ./$VENV_DIR"
    python -m venv "$VENV_DIR"
fi

# Активация виртуального окружения
echo "🚀 Активирую виртуальное окружение"
source "$VENV_DIR/bin/activate"

# Установка зависимостей из requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Устанавливаю зависимости из requirements.txt"
    "$VENV_DIR/bin/pip" install -r requirements.txt
else
    echo "⚠️ Файл requirements.txt не найден — продолжаю без него"
fi

# Установка инструментов
echo "🧰 Устанавливаю pre-commit, black и flake8..."
pip install --upgrade pip
pip install pre-commit black flake8

# Создание .pre-commit-config.yaml, если его нет
if [ ! -f ".pre-commit-config.yaml" ]; then
    echo "📝 Создаю .pre-commit-config.yaml"
    cat << EOF > .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://gitlab.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8]
EOF
else
    echo "✅ .pre-commit-config.yaml уже существует — пропускаю создание"
fi

# Проверка наличия .git
if [ ! -d ".git" ]; then
    echo "❗ Не найден .git — инициализирую git-репозиторий"
    git init
fi

# Установка и обновление хуков
echo "🔗 Устанавливаю и обновляю хуки..."
pre-commit install
pre-commit autoupdate

# Прогон хуков по всем файлам
echo "🧪 Запускаю хуки на всех файлах проекта..."
pre-commit run --all-files

echo "🎉 Всё готово! Форматирование и линтинг будет запускаться автоматически при каждом коммите."
