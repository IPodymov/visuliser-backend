# API Documentation

## Аутентификация (Auth)

Базовый URL: `/api/auth/`

### Регистрация

- **URL**: `/register/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "user1",
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: Данные созданного пользователя.

### Вход (Login)

- **URL**: `/login/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "user1",
    "password": "securepassword"
  }
  ```
- **Response**: Данные пользователя.

### Выход (Logout)

- **URL**: `/logout/`
- **Method**: `POST`
- **Response**: 204 No Content.

---

## Образовательные программы (Programs)

Базовый URL: `/api/`

### Список программ

- **URL**: `/programs/`
- **Method**: `GET`
- **Параметры запроса (Query Parameters)**:
  - `education_level`: Фильтр по уровню образования (например, `bachelor`, `master`).
  - `year`: Фильтр по году набора (точное совпадение, например, `2023`).
  - `year__gte`: Фильтр по году набора (больше или равно, например, `2022`).
  - `year__lte`: Фильтр по году набора (меньше или равно, например, `2024`).
  - `faculty`: Фильтр по факультету (например, `Fit`).
  - `search`: Поиск по названию профиля, направлению или коду АУП.
- **Response**: Список всех доступных образовательных программ.
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

- **URL**: `/programs/<id>/`
- **Method**: `GET`
- **Response**: Детальная информация о программе, включая **сгруппированный** список дисциплин с информацией о семестрах и видах сдачи.
  ```json
  {
      "id": 1,
      "aup_number": "000019337",
      "profile": "Корпоративные информационные системы",
      "disciplines": [
          {
              "name": "История России",
              "code": "Б1.1.1",
              "block": "Блок 1",
              "part": "Обязательная часть",
              "module": null,
              "total_zet": 3.98,
              "semesters": [
                  {
                      "semester": "Шестой семестр",
                      "control_types": ["Зачет"]
                  },
                  {
                      "semester": "Седьмой семестр",
                      "control_types": ["Экзамен"]
                  }
              ]
          },
          ...
      ]
  }
  ```

> **Примечание**: Дисциплины группируются по названию. Для каждой дисциплины показаны:
>
> - `total_zet` — суммарные зачётные единицы
> - `semesters` — список семестров с видами контроля (Экзамен, Зачет, Курсовой проект и т.д.)

### Анализ программы

- **URL**: `/programs/<id>/analysis/`
- **Method**: `GET`
- **Response**: Результаты анализа компетенций программы.
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
      },
      "legend": {
          "CE": "Computer Engineering (Компьютерная инженерия) - ...",
          "CS": "Computer Science (Компьютерные науки) - ...",
          ...
      }
  }
  ```

### Сравнение программ

- **URL**: `/programs/compare/`
- **Method**: `GET`
- **Params**: `ids` (список ID программ, например: `?ids=1&ids=2`)
- **Response**: Список результатов анализа для выбранных программ.
  ```json
  {
      "results": [
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
      ],
      "legend": {
          "CE": "Computer Engineering...",
          ...
      }
  }
  ```

### Загрузка программы из Excel

- **URL**: `/programs/upload/`
- **Method**: `POST`
- **Доступ**: Только для сотрудников и администраторов
- **Content-Type**: `multipart/form-data`
- **Body**:
  - `file` (required): Excel файл (.xlsx) с учебным планом
  - `year` (optional): Год набора (целое число)
- **Response (успех)**:
  ```json
  {
    "message": "Program successfully created",
    "program": {
      "id": 42,
      "aup_number": "000021234",
      "profile": "Название профиля",
      "year": 2025
    }
  }
  ```
- **Response (ошибка валидации)**:
  ```json
  {
    "error": "Invalid profile value: 'nan'. Profile cannot be 'nan' or empty."
  }
  ```
- **Коды ответа**:
  - `201 Created` — программа успешно создана
  - `200 OK` — программа обновлена
  - `400 Bad Request` — ошибка валидации (неверный формат файла, пустой профиль, "nan" в профиле)
  - `403 Forbidden` — недостаточно прав
  - `500 Internal Server Error` — ошибка обработки файла

**Пример cURL запроса:**

```bash
curl -X POST http://localhost:8000/api/programs/upload/ \
  -H "Cookie: sessionid=<session_id>" \
  -F "file=@/path/to/program.xlsx" \
  -F "year=2025"
```
