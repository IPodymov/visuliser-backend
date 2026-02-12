# Структура Базы Данных

Проект использует реляционную базу данных (PostgreSQL).

## Модели

### EducationalProgram (Образовательная программа)

Хранит общую информацию об учебном плане.

| Поле              | Тип        | Описание                                                            |
| ----------------- | ---------- | ------------------------------------------------------------------- |
| `id`              | Integer    | Первичный ключ                                                      |
| `education_type`  | ForeignKey | Вид образования (ссылка на справочник `EducationType`)              |
| `education_level` | ForeignKey | Уровень образования (ссылка на справочник `EducationLevel`)         |
| `direction`       | ForeignKey | Направление подготовки (ссылка на справочник `Direction`)           |
| `qualification`   | ForeignKey | Квалификация (ссылка на справочник `Qualification`)                 |
| `standard_type`   | ForeignKey | Тип стандарта (ссылка на справочник `StandardType`, необязательно)  |
| `faculty`         | ForeignKey | Факультет (ссылка на справочник `Faculty`)                          |
| `profile`         | CharField  | Профиль (специализация)                                             |
| `year`            | Integer    | Год набора (извлекается из имени папки)                             |

### Discipline (Дисциплина)

Хранит информацию о конкретной дисциплине в рамках учебного плана.

| Поле        | Тип        | Описание                                              |
| ----------- | ---------- | ----------------------------------------------------- |
| `id`        | Integer    | Первичный ключ                                        |
| `program`   | ForeignKey | Ссылка на `EducationalProgram` (One-to-Many)          |
| `block`     | ForeignKey | Блок дисциплин (ссылка на `DisciplineBlock`)          |
| `part`      | ForeignKey | Часть (ссылка на `DisciplinePart`)                    |
| `module`    | ForeignKey | Модуль (ссылка на `DisciplineModule`, может быть null)|
| `load_type` | ForeignKey | Тип нагрузки (ссылка на `LoadType`)                   |
| `code`      | CharField  | Шифр дисциплины                                       |
| `name`      | CharField  | Название дисциплины                                   |
| `zet`       | CharField  | Зачетные единицы (ЗЕТ)                                |
| `period`    | ForeignKey | Период контроля (ссылка на `Semester`)                |

## Справочники (Dictionaries)

Для нормализации данных используются следующие справочные модели:

- **Faculty**: Название факультета.
- **Direction**: Код и название направления (Unique together).
- **EducationLevel**: Уровень образования (бакалавриат, магистратура и т.д.).
- **EducationType**: Вид образования.
- **Qualification**: Квалификация выпускника.
- **StandardType**: Тип образовательного стандарта.
- **Semester**: Семестр или период обучения.
- **DisciplineBlock**: Блок дисциплин (Б1, Б2 и т.д.).
- **DisciplinePart**: Часть образовательной программы (Базовая, Вариативная).
- **DisciplineModule**: Модуль дисциплины.
- **LoadType**: Тип учебной нагрузки (Лекция, Практика, Экзамен и т.д.).

## Общие компоненты (Mixins)

### TimeStampedMixin

Расположение: `common/mixins.py`

Абстрактная модель-миксин, добавляющая метки времени создания и обновления.

| Поле         | Тип          | Описание                  |
| ------------ | ------------ | ------------------------- |
| `created_at` | DateTimeField| Дата и время создания     |
| `updated_at` | DateTimeField| Дата и время обновления   |

## Связи

- **EducationalProgram** `1` <---> `N` **Discipline**
  - При удалении программы удаляются все связанные с ней дисциплины (`on_delete=models.CASCADE`).
