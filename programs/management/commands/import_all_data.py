import os
import re
from django.core.management.base import BaseCommand
from programs.services import ExcelParser, ProgramImporter

class Command(BaseCommand):
    help = 'Import all data from data/ directory'

    def handle(self, *args, **options):
        self.stdout.write("Starting import...")
        base_dir = os.path.join(os.getcwd(), 'data')
        self.stdout.write(f"Base dir: {base_dir}")
        
        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR(f"Directory {base_dir} does not exist."))
            return

        parser = ExcelParser()
        importer = ProgramImporter(parser)

        # Regex to match year folders like Fit_2023, Fit_2024
        year_folder_pattern = re.compile(r'Fit_(\d{4})')

        count_success = 0
        count_fail = 0

        for root, dirs, files in os.walk(base_dir):
            self.stdout.write(f"Visiting {root}")
            # Skip _OLD directories and any hidden directories
            if '_OLD' in root or '.git' in root or '.DS_Store' in root:
                self.stdout.write(f"Skipping {root} (filtered)")
                continue
            
            # Remove _OLD from dirs so we don't traverse into them
            if '_OLD' in dirs:
                dirs.remove('_OLD')
                
            # Try to determine year from path
            match = year_folder_pattern.search(root)
            year = int(match.group(1)) if match else None
            self.stdout.write(f"  Year detected: {year}")
            
            for file in files:
                self.stdout.write(f"  Checking file: {file}")
                if (file.endswith('.xlsx') or file.endswith('.xls')) and not file.startswith('~'):
                    
                    file_path = os.path.join(root, file)
                    self.stdout.write(f"  Processing {file_path} (Year: {year})...")
                    
                    try:
                        program, created, error = importer.import_from_file(file_path, year=year)
                        if error:
                            self.stdout.write(self.style.ERROR(f"Error importing {file}: {error}"))
                            count_fail += 1
                        else:
                            action = "Created" if created else "Updated"
                            self.stdout.write(self.style.SUCCESS(f"{action}: {program}"))
                            count_success += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Exception importing {file}: {e}"))
                        count_fail += 1

        self.stdout.write(self.style.SUCCESS(f"\nImport finished. Success: {count_success}, Failed: {count_fail}"))
