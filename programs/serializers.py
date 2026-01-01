from rest_framework import serializers
from collections import defaultdict
from .models import EducationalProgram, Discipline


# Виды контроля (сдачи), которые нас интересуют
CONTROL_TYPES = {
    "Экзамен",
    "Зачет",
    "Зачет с оценкой",
    "Курсовой проект",
    "Курсовая работа",
}


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = [
            "id",
            "block",
            "code",
            "part",
            "module",
            "record_type",
            "name",
            "period",
            "load_type",
            "amount",
            "measurement_unit",
            "zet",
        ]


class SemesterInfoSerializer(serializers.Serializer):
    """Информация о дисциплине в конкретном семестре"""

    semester = serializers.CharField()
    control_types = serializers.ListField(child=serializers.CharField())


class GroupedDisciplineSerializer(serializers.Serializer):
    """Сериализатор для сгруппированной дисциплины"""

    name = serializers.CharField()
    code = serializers.CharField(allow_null=True)
    block = serializers.CharField(allow_null=True)
    part = serializers.CharField(allow_null=True)
    module = serializers.CharField(allow_null=True)
    total_zet = serializers.CharField(allow_null=True)
    semesters = SemesterInfoSerializer(many=True)


class EducationalProgramSerializer(serializers.ModelSerializer):
    disciplines = serializers.SerializerMethodField()

    class Meta:
        model = EducationalProgram
        fields = [
            "id",
            "aup_number",
            "education_type",
            "education_level",
            "direction",
            "direction_code",
            "qualification",
            "profile",
            "standard_type",
            "faculty",
            "year",
            "disciplines",
        ]

    def get_disciplines(self, obj):
        """Группирует дисциплины по названию и собирает информацию о семестрах и видах сдачи"""
        disciplines = obj.disciplines.all()

        # Группируем по названию дисциплины
        grouped: dict[str, dict] = {}
        
        def get_group(name: str) -> dict:
            if name not in grouped:
                grouped[name] = {
                    "name": None,
                    "code": None,
                    "block": None,
                    "part": None,
                    "module": None,
                    "total_zet": 0.0,
                    "semesters": defaultdict(set),  # {семестр: {виды контроля}}
                }
            return grouped[name]

        for disc in disciplines:
            key = disc.name
            if not key:
                continue

            group = get_group(key)
            group["name"] = disc.name

            # Берём первые непустые значения для общих полей
            if disc.code and not group["code"]:
                group["code"] = disc.code
            if disc.block and not group["block"]:
                group["block"] = disc.block
            if disc.part and not group["part"]:
                group["part"] = disc.part
            if disc.module and not group["module"]:
                group["module"] = disc.module

            # Суммируем ЗЕТ из всех записей (кроме контрольных видов)
            if disc.zet and disc.load_type not in CONTROL_TYPES:
                try:
                    # ZET может быть в формате "0,44" (с запятой)
                    zet_value = float(str(disc.zet).replace(",", "."))
                    group["total_zet"] += zet_value
                except (ValueError, TypeError):
                    pass

            # Добавляем вид контроля для семестра
            if disc.period and disc.load_type in CONTROL_TYPES:
                group["semesters"][disc.period].add(disc.load_type)

        # Преобразуем в список для сериализации
        result = []
        for name, data in grouped.items():
            semesters_list = [
                {"semester": semester, "control_types": sorted(list(control_types))}
                for semester, control_types in sorted(
                    data["semesters"].items(), key=lambda x: _semester_order(x[0])
                )
            ]

            result.append(
                {
                    "name": data["name"],
                    "code": data["code"],
                    "block": data["block"],
                    "part": data["part"],
                    "module": data["module"],
                    "total_zet": (
                        round(data["total_zet"], 2) if data["total_zet"] > 0 else None
                    ),
                    "semesters": semesters_list,
                }
            )

        # Сортируем по коду дисциплины
        result.sort(key=lambda x: x["code"] or "")

        return result


def _semester_order(semester_name: str) -> int:
    """Возвращает числовой порядок семестра для сортировки"""
    order_map = {
        "Первый семестр": 1,
        "Второй семестр": 2,
        "Третий семестр": 3,
        "Четвертый семестр": 4,
        "Пятый семестр": 5,
        "Шестой семестр": 6,
        "Седьмой семестр": 7,
        "Восьмой семестр": 8,
        "Девятый семестр": 9,
        "Десятый семестр": 10,
        "Одиннадцатый семестр": 11,
        "Двенадцатый семестр": 12,
    }
    return order_map.get(semester_name, 99)
