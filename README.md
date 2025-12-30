# Visualizer Backend

Веб-приложение для визуализации и сравнения основных профессиональных образовательных программ.
Серверная часть реализована на Django + Django REST Framework.

## Функциональность

*   **Авторизация и регистрация**: JWT/Session based (в текущей реализации Session/Basic, но подготовлена для расширения).
*   **Парсинг данных**: Импорт учебных планов и дисциплин из Excel-файлов.
*   **API**: Предоставление данных об образовательных программах и дисциплинах.

## Установка и запуск

### Предварительные требования

*   Python 3.10+
*   PostgreSQL (или SQLite для разработки)

### Шаги установки

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <repository_url>
    cd visualizer-back
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для macOS/Linux
    # venv\Scripts\activate  # Для Windows
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Примечание: если файла requirements.txt нет, создайте его командой `pip freeze > requirements.txt`)*

4.  **Настройте переменные окружения:**
    Создайте файл `.env` в корне проекта и добавьте строку подключения к БД:
    ```env
    DATABASE_URL=postgresql://user:password@host:port/dbname
    ```

5.  **Примените миграции:**
    ```bash
    python manage.py migrate
    ```

6.  **Загрузите данные из Excel:**
    Поместите папки с данными (например, `Fit_2023`) в директорию `data/` и запустите парсер:
    ```bash
    python manage.py parse_excel
    ```

7.  **Запустите сервер разработки:**
    ```bash
    python manage.py runserver
    ```

## Документация

Подробная документация по проекту доступна в папке [docs/](docs/):

*   [Обзор проекта](docs/project_overview.md) — Архитектура, цели и ключевые возможности.
*   [API Documentation](docs/api.md) — Описание эндпоинтов API.
*   [Структура Базы Данных](docs/database.md) — Описание моделей данных.
*   [Парсер данных](docs/parser.md) — Инструкция по импорту данных из Excel.
