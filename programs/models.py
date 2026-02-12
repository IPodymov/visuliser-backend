from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=255, verbose_name="Факультет", unique=True)

    def __str__(self):
        return self.name


class Direction(models.Model):
    code = models.CharField(max_length=50, verbose_name="Код направления")
    name = models.CharField(max_length=255, verbose_name="Название направления")

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        unique_together = ("code", "name")

    def __str__(self):
        return f"{self.code} {self.name}"


class EducationLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Уровень образования", unique=True)

    def __str__(self):
        return self.name


class EducationType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Вид образования", unique=True)

    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=100, verbose_name="Квалификация", unique=True)

    def __str__(self):
        return self.name


class StandardType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип стандарта", unique=True)

    def __str__(self):
        return self.name


class EducationalProgram(models.Model):
    education_type = models.ForeignKey(
        EducationType, on_delete=models.CASCADE, verbose_name="Вид образования"
    )
    education_level = models.ForeignKey(
        EducationLevel, on_delete=models.CASCADE, verbose_name="Уровень образования"
    )
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Направление")
    qualification = models.ForeignKey(
        Qualification, on_delete=models.CASCADE, verbose_name="Квалификация"
    )
    standard_type = models.ForeignKey(
        StandardType,
        on_delete=models.CASCADE,
        verbose_name="Тип стандарта",
        null=True,
        blank=True,
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Факультет")
    profile = models.CharField(max_length=255, verbose_name="Профиль (специализация)")
    year = models.IntegerField(verbose_name="Год набора", null=True, blank=True)

    # Type hint for reverse relation
    disciplines: models.Manager["Discipline"]

    def __str__(self):
        return f"{self.direction.code} - {self.profile} ({self.year})"


class Semester(models.Model):
    name = models.CharField(max_length=100, verbose_name="Семестр/Период", unique=True)

    def __str__(self):
        return self.name


class DisciplineBlock(models.Model):
    name = models.CharField(max_length=100, verbose_name="Блок", unique=True)

    def __str__(self):
        return self.name


class DisciplinePart(models.Model):
    name = models.CharField(max_length=100, verbose_name="Часть", unique=True)

    def __str__(self):
        return self.name


class DisciplineModule(models.Model):
    name = models.CharField(max_length=255, verbose_name="Модуль", unique=True)

    def __str__(self):
        return self.name


class LoadType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Вид нагрузки", unique=True)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    program = models.ForeignKey(
        EducationalProgram, on_delete=models.CASCADE, related_name="disciplines"
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        verbose_name="Семестр",
        null=True,
        blank=True,
        related_name="disciplines",
    )
    block = models.ForeignKey(
        DisciplineBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Блок",
    )
    part = models.ForeignKey(
        DisciplinePart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Часть",
    )
    module = models.ForeignKey(
        DisciplineModule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Модуль",
    )
    load_type = models.ForeignKey(
        LoadType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Вид нагрузки",
    )

    code = models.CharField(max_length=50, verbose_name="Шифр", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Дисциплина")

    amount = models.CharField(max_length=50, verbose_name="Количество", null=True, blank=True)
    measurement_unit = models.CharField(
        max_length=50, verbose_name="Ед. изм.", null=True, blank=True
    )
    zet = models.CharField(max_length=50, verbose_name="ЗЕТ", null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class DisciplineMarking(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="markings")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return f"Marking for {self.discipline}"


class SemesterControl(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="controls")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Семестр")
    control_type = models.CharField(
        max_length=100, verbose_name="Вид контроля"
    )  # e.g. Экзамен, Зачет

    def __str__(self):
        return f"{self.control_type} ({self.semester})"
