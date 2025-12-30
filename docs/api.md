# API Documentation

## Аутентификация (Auth)

Базовый URL: `/api/auth/`

### Регистрация
*   **URL**: `/register/`
*   **Method**: `POST`
*   **Body**:
    ```json
    {
        "username": "user1",
        "email": "user@example.com",
        "password": "securepassword"
    }
    ```
*   **Response**: Данные созданного пользователя.

### Вход (Login)
*   **URL**: `/login/`
*   **Method**: `POST`
*   **Body**:
    ```json
    {
        "username": "user1",
        "password": "securepassword"
    }
    ```
*   **Response**: Данные пользователя.

### Выход (Logout)
*   **URL**: `/logout/`
*   **Method**: `POST`
*   **Response**: 204 No Content.

---

## Образовательные программы (Programs)

Базовый URL: `/api/`

### Список программ
*   **URL**: `/programs/`
*   **Method**: `GET`
*   **Response**: Список всех доступных образовательных программ.
    ```json
    [
        {
            "id": 1,
            "aup_number": "000019337",
            "profile": "Корпоративные информационные системы",
            "year": 2023,
            ...
        },
        ...
    ]
    ```

### Детальная информация о программе
*   **URL**: `/programs/<id>/`
*   **Method**: `GET`
*   **Response**: Детальная информация о программе, включая список всех дисциплин.
    ```json
    {
        "id": 1,
        "aup_number": "000019337",
        "profile": "Корпоративные информационные системы",
        "disciplines": [
            {
                "id": 101,
                "name": "История России",
                "code": "Б1.1.1",
                "zet": "0.94",
                ...
            },
            ...
        ]
    }
    ```

### Анализ программы
*   **URL**: `/programs/<id>/analysis/`
*   **Method**: `GET`
*   **Response**: Результаты анализа компетенций программы.
    ```json
    {
        "program": "000019337 - Корпоративные информационные системы",
        "analysis": {
            "scores": {
                "CE": 10.5,
                "CS": 25.0,
                "SE": 30.0,
                "IT": 15.0,
                "IS": 15.0,
                "CSEC": 2.5,
                "DS": 2.0
            },
            "raw_scores": { ... },
            "total_analyzed_zet": 120.0
        }
    }
    ```

### Сравнение программ
*   **URL**: `/programs/compare/`
*   **Method**: `GET`
*   **Params**: `ids` (список ID программ, например: `?ids=1&ids=2`)
*   **Response**: Список результатов анализа для выбранных программ.
    ```json
    [
        {
            "id": 1,
            "name": "...",
            "analysis": { ... }
        },
        {
            "id": 2,
            "name": "...",
            "analysis": { ... }
        }
    ]
    ```
