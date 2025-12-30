import os
import pandas as pd
from django.core.management.base import BaseCommand
from programs.models import EducationalProgram, Discipline
from django.conf import settings


class Command(BaseCommand):
    help = "Parses Excel files from the data directory and populates the database"

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, "data")

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f"Data directory not found: {data_dir}"))
            return

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".xlsx") and not file.startswith("~$"):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path, root)

    def process_file(self, file_path, root):
        try:
            # Extract year from folder name (e.g., Fit_2023 -> 2023)
            folder_name = os.path.basename(root)
            year = None
            if "Fit_" in folder_name:
                try:
                    year = int(folder_name.split("_")[1])
                except (IndexError, ValueError):
                    pass

            # Read Sheet 1 (Program Info)
            df1 = pd.read_excel(file_path, sheet_name=0, header=None)
            program_data = dict(zip(df1[0], df1[1]))

            aup_number = program_data.get("Номер АУП")

            if not aup_number:
                self.stdout.write(
                    self.style.WARNING(f"Skipping {file_path}: No AUP number found")
                )
                return

            program, created = EducationalProgram.objects.update_or_create(
                aup_number=aup_number,
                defaults={
                    "education_type": program_data.get("Вид образования"),
                    "education_level": program_data.get("Уровень образования"),
                    "direction": program_data.get("Направление (специальность)"),
                    "direction_code": program_data.get("Код специальности"),
                    "qualification": program_data.get("Квалификация"),
                    "profile": program_data.get("Профиль (специализация)"),
                    "standard_type": program_data.get("Тип стандарта"),
                    "faculty": program_data.get("Факультет"),
                    "year": year,
                },
            )

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} program: {program}"))

            # Read Sheet 2 (Disciplines)
            df2 = pd.read_excel(file_path, sheet_name=1)

            # Clear existing disciplines for this program to avoid duplicates on re-run
            Discipline.objects.filter(program=program).delete()

            disciplines_to_create = []
            for _, row in df2.iterrows():
                # Handle NaN values
                row = row.where(pd.notnull(row), None)

                discipline = Discipline(
                    program=program,
                    block=row.get("Блок"),
                    code=row.get("Шифр"),
                    part=row.get("Часть"),
                    module=row.get("Модуль"),
                    record_type=row.get("Тип записи"),
                    name=row.get("Дисциплина"),
                    period=row.get("Период контроля"),
                    load_type=row.get("Нагрузка"),
                    amount=row.get("Количество"),
                    measurement_unit=row.get("Ед. изм."),
                    zet=row.get("ЗЕТ"),
                )
                disciplines_to_create.append(discipline)

            Discipline.objects.bulk_create(disciplines_to_create)
            self.stdout.write(
                self.style.SUCCESS(f"  Added {len(disciplines_to_create)} disciplines")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing {file_path}: {e}"))
