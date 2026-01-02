# Visualizer Backend

Веб-приложение для визуализации и сравнения основных профессиональных образовательных программ (ОПОП).
Серверная часть реализована на Django + Django REST Framework.

## Функциональность

- **Авторизация и регистрация**: Session-based аутентификация с поддержкой CORS
- **Парсинг данных**: Импорт учебных планов и дисциплин из Excel-файлов
- **Загрузка через API**: Эндпоинт для загрузки программ (для сотрудников и администраторов)
- **Группировка дисциплин**: Дисциплины группируются по названию с информацией о семестрах и видах контроля
- **Анализ компетенций**: Оценка направленности программы по 7 областям (CE, CS, SE, IT, IS, CSEC, DS)
- **Сравнение программ**: Сравнительный анализ нескольких программ
- **Валидация данных**: Автоматическая проверка корректности загружаемых данных

## Установка и запуск

### Предварительные требования

- Python 3.10+
- PostgreSQL (или SQLite для разработки)
- Redis (для кэширования)

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

4.  **Настройте переменные окружения:**
    Создайте файл `.env` в корне проекта:

    ```env
    DATABASE_URL=postgresql://user:password@host:port/dbname
    REDIS_URL=redis://localhost:6379/0
    ```

5.  **Примените миграции:**

    ```bash
    python manage.py migrate
    ```

6.  **Создайте суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Загрузите данные из Excel:**
    Поместите папки с данными (например, `Fit_2023`) в директорию `data/` и запустите парсер:

    ```bash
    python manage.py parse_excel
    ```

8.  **Запустите сервер разработки:**
    ```bash
    python manage.py runserver
    ```

## API Endpoints

| Метод | URL                                  | Описание           | Доступ             |
| ----- | ------------------------------------ | ------------------ | ------------------ |
| POST  | `/api/auth/register/`                | Регистрация        | Все                |
| POST  | `/api/auth/login/`                   | Вход               | Все                |
| POST  | `/api/auth/logout/`                  | Выход              | Авторизованные     |
| GET   | `/api/programs/`                     | Список программ    | Авторизованные     |
| GET   | `/api/programs/<id>/`                | Детали программы   | Авторизованные     |
| GET   | `/api/programs/<id>/analysis/`       | Анализ компетенций | Авторизованные     |
| GET   | `/api/programs/compare/?ids=1&ids=2` | Сравнение программ | Авторизованные     |
| POST  | `/api/programs/upload/`              | Загрузка из Excel  | Сотрудники, Админы |

## Структура проекта

```
visualizer-back/
├── data/                   # Excel файлы с учебными планами
│   ├── Fit_2023/
│   ├── Fit_2024/
│   └── Fit_2025/
├── docs/                   # Документация
├── programs/               # Приложение для работы с программами
│   ├── management/commands/  # Management команды (parse_excel)
│   ├── models.py           # Модели EducationalProgram, Discipline
│   ├── serializers.py      # Сериализаторы с группировкой дисциплин
│   ├── services.py         # ExcelParser, ProgramImporter
│   ├── analysis.py         # CompetencyAnalyzer
│   └── views.py            # API views
├── users/                  # Приложение для пользователей
│   ├── permissions.py      # Права доступа
│   └── views.py            # Auth views
└── visualizer/             # Настройки проекта
    └── settings.py
```

## Документация

Подробная документация по проекту доступна в папке [docs/](docs/):

- [Обзор проекта](docs/project_overview.md) — Архитектура, цели и ключевые возможности
- [API Documentation](docs/api.md) — Описание эндпоинтов API
- [Структура Базы Данных](docs/database.md) — Описание моделей данных
- [Парсер данных](docs/parser.md) — Инструкция по импорту данных из Excel

## Технологии

- **Backend**: Django 6.0, Django REST Framework 3.16
- **База данных**: PostgreSQL (dj-database-url)
- **Кэширование**: Redis (django-redis)
- **CORS**: django-cors-headers
- **Парсинг Excel**: pandas, openpyxl
- **Деплой**: Gunicorn, WhiteNoise
