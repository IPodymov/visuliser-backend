import pandas as pd
from django.db import transaction
from .models import EducationalProgram, Discipline
from .constants import *


class ExcelParser:
    """
    Responsible for reading Excel files and extracting raw data.
    Follows SRP: Only knows how to read the file format.
    """

    def parse_program_data(self, file_path):
        try:
            df = pd.read_excel(file_path, sheet_name=PROGRAM_SHEET_INDEX, header=None)
            return dict(zip(df[0], df[1]))
        except Exception as e:
            raise ValueError(f"Failed to parse program data from {file_path}: {e}")

    def parse_disciplines_data(self, file_path):
        try:
            df = pd.read_excel(file_path, sheet_name=DISCIPLINES_SHEET_INDEX)
            return df
        except Exception as e:
            raise ValueError(f"Failed to parse disciplines data from {file_path}: {e}")


class ProgramImporter:
    """
    Responsible for business logic of importing programs and disciplines into the database.
    Follows SRP: Only knows how to save data to models.
    """

    def __init__(self, parser: ExcelParser):
        self.parser = parser

    @transaction.atomic
    def import_from_file(self, file_path, year=None):
        program_data = self.parser.parse_program_data(file_path)
        aup_number = program_data.get(COL_AUP_NUMBER)

        if not aup_number:
            return None, False, "No AUP number found"

        program, created = EducationalProgram.objects.update_or_create(
            aup_number=aup_number,
            defaults={
                "education_type": program_data.get(COL_EDUCATION_TYPE),
                "education_level": program_data.get(COL_EDUCATION_LEVEL),
                "direction": program_data.get(COL_DIRECTION),
                "direction_code": program_data.get(COL_DIRECTION_CODE),
                "qualification": program_data.get(COL_QUALIFICATION),
                "profile": program_data.get(COL_PROFILE),
                "standard_type": program_data.get(COL_STANDARD_TYPE),
                "faculty": program_data.get(COL_FACULTY),
                "year": year,
            },
        )

        self._import_disciplines(file_path, program)

        return program, created, None

    def _import_disciplines(self, file_path, program):
        df = self.parser.parse_disciplines_data(file_path)

        # Clear existing disciplines to ensure idempotency
        Discipline.objects.filter(program=program).delete()

        disciplines_to_create = []
        for _, row in df.iterrows():
            # Handle NaN values by converting to dict and replacing NaNs with None
            row_data = {k: (v if pd.notnull(v) else None) for k, v in row.items()}

            discipline = Discipline(
                program=program,
                block=row_data.get(COL_BLOCK),
                code=row_data.get(COL_CODE),
                part=row_data.get(COL_PART),
                module=row_data.get(COL_MODULE),
                record_type=row_data.get(COL_RECORD_TYPE),
                name=row_data.get(COL_DISCIPLINE_NAME),
                period=row_data.get(COL_PERIOD),
                load_type=row_data.get(COL_LOAD_TYPE),
                amount=row_data.get(COL_AMOUNT),
                measurement_unit=row_data.get(COL_MEASUREMENT_UNIT),
                zet=row_data.get(COL_ZET),
            )
            disciplines_to_create.append(discipline)

        Discipline.objects.bulk_create(disciplines_to_create)
        return len(disciplines_to_create)
