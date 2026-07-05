set shell := ["powershell", "-Command"]

# botdocs — Telegram bot

# Запуск бота
run:
    uv run python src/bot.py

# Линтинг
lint:
    uv run ruff check .

# Автоисправление линтера
lintf:
    uv run ruff check --fix .

# Форматирование
fmt:
    uv run ruff format .

# Проверка форматирования
fmtch:
    uv run ruff format --check .

# Проверка типов
tch:
    uv run mypy .

# Тесты
test:
    uv run pytest -v

# Тесты с покрытием
test-cov:
    uv run pytest --cov=src --cov-report=term-missing -v

# Все проверки
check: lint fmtch tch test

# Pre-commit на всех файлах
pcom:
    uv run pre-commit run --all-files

# Установка pre-commit хуков
pcomin:
    uv run pre-commit install

# Установка зависимостей
install:
    uv sync
