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
