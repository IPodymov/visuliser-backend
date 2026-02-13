import pandas as pd
from django.db import transaction
from .models import (
    EducationalProgram,
    Discipline,
    Faculty,
    Direction,
    EducationLevel,
    EducationType,
    Qualification,
    StandardType,
    Semester,
    DisciplineBlock,
    DisciplinePart,
    DisciplineModule,
    LoadType,
)
from .constants import (
    PROGRAM_SHEET_INDEX,
    DISCIPLINES_SHEET_INDEX,
    COL_AUP_NUMBER,
    COL_EDUCATION_TYPE,
    COL_EDUCATION_LEVEL,
    COL_DIRECTION,
    COL_DIRECTION_CODE,
    COL_QUALIFICATION,
    COL_PROFILE,
    COL_STANDARD_TYPE,
    COL_FACULTY,
    COL_BLOCK,
    COL_CODE,
    COL_PART,
    COL_MODULE,
    COL_RECORD_TYPE,
    COL_DISCIPLINE_NAME,
    COL_PERIOD,
    COL_LOAD_TYPE,
    COL_AMOUNT,
    COL_MEASUREMENT_UNIT,
    COL_ZET,
)


class InvalidProgramError(Exception):
    """Raised when program data is invalid (e.g., profile is 'nan')"""

    pass


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

    def parse_program_data_from_file(self, file_obj):
        """Parse program data from an uploaded file object"""
        try:
            df = pd.read_excel(file_obj, sheet_name=PROGRAM_SHEET_INDEX, header=None)
            return dict(zip(df[0], df[1]))
        except Exception as e:
            raise ValueError(f"Failed to parse program data: {e}")

    def parse_disciplines_data_from_file(self, file_obj):
        """Parse disciplines data from an uploaded file object"""
        try:
            df = pd.read_excel(file_obj, sheet_name=DISCIPLINES_SHEET_INDEX)
            return df
        except Exception as e:
            raise ValueError(f"Failed to parse disciplines data: {e}")


class ProgramImporter:
    """
    Responsible for business logic of importing programs and disciplines into the database.
    Follows SRP: Only knows how to save data to models.
    """

    def __init__(self, parser: ExcelParser):
        self.parser = parser

    def _validate_profile(self, profile):
        """Validate that profile is not 'nan' or empty"""
        if profile is None:
            raise InvalidProgramError("Profile cannot be empty")

        profile_str = str(profile).strip().lower()
        if profile_str == "nan" or profile_str == "":
            raise InvalidProgramError(
                f"Invalid profile value: '{profile}'. Profile cannot be 'nan' or empty."
            )

    @transaction.atomic
    def import_from_file(self, file_path, year=None):
        program_data = self.parser.parse_program_data(file_path)
        # Assuming AUP is still used to identify the file/program locally, but not stored on the model as primary key
        # Wait, prompt said "Remove aup_number from EducationalProgram".
        # But we might still use it to uniquely identify during import? Or identifying by profile/direction/year?
        # The prompt says: "Exclude use of aup_number when searching and creating programs."
        # So we should use something else. Direction + Profile + Year is a good candidate for uniqueness.

        # Validate profile
        profile = program_data.get(COL_PROFILE)
        self._validate_profile(profile)

        # Get or create related models
        faculty_name = program_data.get(COL_FACULTY)
        faculty, _ = Faculty.objects.get_or_create(name=faculty_name)

        direction_code = program_data.get(COL_DIRECTION_CODE)
        direction_name = program_data.get(COL_DIRECTION)
        direction, _ = Direction.objects.get_or_create(
            code=direction_code, defaults={"name": direction_name}
        )

        edu_level_name = program_data.get(COL_EDUCATION_LEVEL)
        edu_level, _ = EducationLevel.objects.get_or_create(name=edu_level_name)

        edu_type_name = program_data.get(COL_EDUCATION_TYPE)
        edu_type, _ = EducationType.objects.get_or_create(name=edu_type_name)

        qualification_name = program_data.get(COL_QUALIFICATION)
        qualification, _ = Qualification.objects.get_or_create(name=qualification_name)

        standard_type_name = program_data.get(COL_STANDARD_TYPE)
        standard_type, _ = StandardType.objects.get_or_create(name=standard_type_name)

        # Update or Create Program based on Direction, Profile, Year
        program, created = EducationalProgram.objects.update_or_create(
            direction=direction,
            profile=profile,
            year=year,
            defaults={
                "education_type": edu_type,
                "education_level": edu_level,
                "qualification": qualification,
                "standard_type": standard_type,
                "faculty": faculty,
            },
        )

        self._import_disciplines(file_path, program)

        return program, created, None

    @transaction.atomic
    def import_from_uploaded_file(self, file_obj, year=None):
        """Import program from an uploaded file object"""
        program_data = self.parser.parse_program_data_from_file(file_obj)

        # Validate profile
        profile = program_data.get(COL_PROFILE)
        self._validate_profile(profile)

        # Get or create related models
        faculty_name = program_data.get(COL_FACULTY)
        faculty, _ = Faculty.objects.get_or_create(name=faculty_name)

        direction_code = program_data.get(COL_DIRECTION_CODE)
        direction_name = program_data.get(COL_DIRECTION)
        direction, _ = Direction.objects.get_or_create(
            code=direction_code, defaults={"name": direction_name}
        )

        edu_level_name = program_data.get(COL_EDUCATION_LEVEL)
        edu_level, _ = EducationLevel.objects.get_or_create(name=edu_level_name)

        edu_type_name = program_data.get(COL_EDUCATION_TYPE)
        edu_type, _ = EducationType.objects.get_or_create(name=edu_type_name)

        qualification_name = program_data.get(COL_QUALIFICATION)
        qualification, _ = Qualification.objects.get_or_create(name=qualification_name)

        standard_type_name = program_data.get(COL_STANDARD_TYPE)
        standard_type, _ = StandardType.objects.get_or_create(name=standard_type_name)

        program, created = EducationalProgram.objects.update_or_create(
            direction=direction,
            profile=profile,
            year=year,
            defaults={
                "education_type": edu_type,
                "education_level": edu_level,
                "qualification": qualification,
                "standard_type": standard_type,
                "faculty": faculty,
            },
        )

        # Reset file position for reading disciplines
        file_obj.seek(0)
        self._import_disciplines_from_file(file_obj, program)

        return program, created, None

    def _import_disciplines(self, file_path, program):
        df = self.parser.parse_disciplines_data(file_path)
        return self._save_disciplines(df, program)

    def _import_disciplines_from_file(self, file_obj, program):
        """Import disciplines from an uploaded file object"""
        df = self.parser.parse_disciplines_data_from_file(file_obj)
        return self._save_disciplines(df, program)

    def _save_disciplines(self, df, program):
        """Save disciplines from DataFrame to database"""
        # Optimized implementation to reduce DB queries

        created_count = 0
        new_disciplines = []

        # Pre-fetch existing disciplines to avoid N+1 queries
        existing_disciplines = set(
            Discipline.objects.filter(program=program).values_list("semester__name", "name", "code")
        )

        # Local caches for dictionary lookups
        semesters_cache = {}
        blocks_cache = {}
        parts_cache = {}
        modules_cache = {}
        load_types_cache = {}

        def get_cached_obj(model, name, cache):
            if not name:
                return None
            if name not in cache:
                obj, _ = model.objects.get_or_create(name=name)
                cache[name] = obj
            return cache[name]

        for _, row in df.iterrows():
            # Handle NaN values
            row_data = {k: (v if pd.notnull(v) else None) for k, v in row.items()}

            discipline_name = row_data.get(COL_DISCIPLINE_NAME)
            if not discipline_name:
                continue

            code = row_data.get(COL_CODE)
            semester_name = row_data.get(COL_PERIOD)

            # Check duplication tuple (semester_name, discipline_name, code)
            # Note: code or semester might be None, so we handle that in the tuple
            if (semester_name, discipline_name, code) in existing_disciplines:
                continue

            # Resolve related objects using cache
            semester = get_cached_obj(Semester, semester_name, semesters_cache)
            block = get_cached_obj(DisciplineBlock, row_data.get(COL_BLOCK), blocks_cache)
            part = get_cached_obj(DisciplinePart, row_data.get(COL_PART), parts_cache)
            module = get_cached_obj(DisciplineModule, row_data.get(COL_MODULE), modules_cache)
            load_type = get_cached_obj(LoadType, row_data.get(COL_LOAD_TYPE), load_types_cache)

            # Create Discipline instance (but don't save yet)
            discipline = Discipline(
                program=program,
                semester=semester,
                block=block,
                part=part,
                module=module,
                load_type=load_type,
                code=code,
                name=discipline_name,
                amount=row_data.get(COL_AMOUNT),
                measurement_unit=row_data.get(COL_MEASUREMENT_UNIT),
                zet=row_data.get(COL_ZET),
            )
            new_disciplines.append(discipline)

            # Add to existing set to prevent duplicates within the same file import
            existing_disciplines.add((semester_name, discipline_name, code))

        if new_disciplines:
            Discipline.objects.bulk_create(new_disciplines)
            created_count = len(new_disciplines)

        return created_count
