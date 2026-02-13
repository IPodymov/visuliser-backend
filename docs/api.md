# API Documentation

## Основные сведения

В API включена **глобальная пагинация** для списковых методов.

- **Размер страницы по умолчанию**: 20 элементов.
- **Параметры пагинации**: `?page=2` (номер страницы).
- **Формат ответа**:
  ```json
  {
      "count": 102,
      "next": "http://api/programs/?page=3",
      "previous": "http://api/programs/?page=1",
      "results": [ ... ]
  }
  ```

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
- **Response**: Список программ с пагинацией.
  ```json
  {
      "count": 50,
      "next": "...",
      "previous": null,
      "results": [
          {
              "id": 1,
              "direction": "09.03.03 Прикладная информатика",
              "profile": "Корпоративные информационные системы",
              "faculty": "Факультет информационных технологий",
              "year": 2023,
              ...
          },
          ...
      ]
  }
  ```

### Детальная информация о программе

- **URL**: `/programs/<id>/`
- **Method**: `GET`
- **Response**: Детальная информация о программе, включая **несгруппированный** список дисциплин (оптимизированный для быстрой загрузки).
  ```json
  {
      "id": 1,
      "direction": "09.03.03 Прикладная информатика",
      "profile": "Корпоративные информационные системы",
      "disciplines": [
          {
              "id": 101,
              "name": "История России",
              "code": "Б1.1.1",
              "block": "Блок 1",
              "part": "Обязательная часть",
              "semester": "Шестой семестр",
              "load_type": "Экзамен",
              "amount": "144",
              "zet": "4"
          },
          ...
      ]
  }
  ```

### Дисциплины программы

- **URL**: `/programs/<id>/disciplines/`
- **Method**: `GET`
- **Params**: `?semester=Первый семестр`
- **Response**: Список дисциплин отдельным запросом.

### Анализ программы

- **URL**: `/programs/<id>/analysis/`
- **Method**: `GET`
- **Response**: Результаты анализа компетенций программы.
  ```json
  {
      "program": "09.03.03 Прикладная информатика - Корпоративные информационные системы (2023)",
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
- **Доступ**: Только для сотрудников и администраторов.
- **Body**: Multipart-Form Data.
  - `file`: .xlsx файл.
  - `year`: Год набора (integer).
