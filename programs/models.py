from django.db import models


class EducationalProgram(models.Model):
    id = models.AutoField(primary_key=True)
    aup_number = models.CharField(max_length=50, verbose_name="Номер АУП")
    education_type = models.CharField(max_length=100, verbose_name="Вид образования")
    education_level = models.CharField(
        max_length=100, verbose_name="Уровень образования"
    )
    direction = models.CharField(
        max_length=255, verbose_name="Направление (специальность)"
    )
    direction_code = models.CharField(max_length=50, verbose_name="Код специальности")
    qualification = models.CharField(max_length=100, verbose_name="Квалификация")
    profile = models.CharField(max_length=255, verbose_name="Профиль (специализация)")
    standard_type = models.CharField(max_length=100, verbose_name="Тип стандарта")
    faculty = models.CharField(max_length=255, verbose_name="Факультет")
    year = models.IntegerField(verbose_name="Год набора", null=True, blank=True)

    # Type hint for reverse relation
    disciplines: models.Manager["Discipline"]

    def __str__(self):
        return f"{self.aup_number} - {self.profile} ({self.year})"


class Discipline(models.Model):
    program = models.ForeignKey(
        EducationalProgram, on_delete=models.CASCADE, related_name="disciplines"
    )
    block = models.CharField(max_length=100, verbose_name="Блок", null=True, blank=True)
    code = models.CharField(max_length=50, verbose_name="Шифр", null=True, blank=True)
    part = models.CharField(max_length=100, verbose_name="Часть", null=True, blank=True)
    module = models.CharField(
        max_length=255, verbose_name="Модуль", null=True, blank=True
    )
    record_type = models.CharField(
        max_length=100, verbose_name="Тип записи", null=True, blank=True
    )
    name = models.CharField(max_length=255, verbose_name="Дисциплина")
    period = models.CharField(
        max_length=100, verbose_name="Период контроля", null=True, blank=True
    )
    load_type = models.CharField(
        max_length=100, verbose_name="Нагрузка", null=True, blank=True
    )
    amount = models.CharField(
        max_length=50, verbose_name="Количество", null=True, blank=True
    )  # CharField because it might be empty or formatted
    measurement_unit = models.CharField(
        max_length=50, verbose_name="Ед. изм.", null=True, blank=True
    )
    zet = models.CharField(max_length=50, verbose_name="ЗЕТ", null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
