import os
from django.core.management.base import BaseCommand
from django.conf import settings
from programs.services import ExcelParser, ProgramImporter


class Command(BaseCommand):
    help = "Parses Excel files from the data directory and populates the database"

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, "data")

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f"Data directory not found: {data_dir}"))
            return

        parser = ExcelParser()
        importer = ProgramImporter(parser)

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".xlsx") and not file.startswith("~$"):
                    file_path = os.path.join(root, file)
                    self.process_file(importer, file_path, root)

    def process_file(self, importer, file_path, root):
        try:
            # Extract year from folder name (e.g., Fit_2023 -> 2023)
            folder_name = os.path.basename(root)
            year = None
            if "Fit_" in folder_name:
                try:
                    year = int(folder_name.split("_")[1])
                except (IndexError, ValueError):
                    pass

            program, created, error = importer.import_from_file(file_path, year)

            if error:
                self.stdout.write(self.style.WARNING(f"Skipping {file_path}: {error}"))
                return

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} program: {program}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing {file_path}: {e}"))
