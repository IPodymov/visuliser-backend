import re
from django.db.models import QuerySet
from .models import ProgramDiscipline


class CompetencyAnalyzer:
    # Descriptions for each competency area
    DESCRIPTIONS = {
        "CE": "Computer Engineering (Компьютерная инженерия) - Аппаратное обеспечение, электроника, микропроцессоры.",
        "CS": "Computer Science (Компьютерные науки) - Алгоритмы, математика, искусственный интеллект, теория.",
        "SE": "Software Engineering (Программная инженерия) - Разработка ПО, тестирование, управление проектами.",
        "IT": "Information Technology (Информационные технологии) - Администрирование, сети, инфраструктура.",
        "IS": "Information Systems (Информационные системы) - Бизнес-процессы, управление предприятием, ERP/CRM.",
        "CSEC": "Cybersecurity (Кибербезопасность) - Защита информации, криптография, безопасность сетей.",
        "DS": "Data Science (Наука о данных) - Анализ данных, статистика, машинное обучение.",
    }

    # Keywords for each competency area (Russian)
    KEYWORDS = {
        "CE": [
            r"схемотехник",
            r"электроник",
            r"физик",
            r"робототехник",
            r"микропроцессор",
            r"архитектура эвм",
            r"аппаратн",
            r"железо",
            r"интернет вещей",
            r"iot",
            r"сигналов",
        ],
        "CS": [
            r"алгоритм",
            r"структур.*данных",
            r"математик",
            r"логик",
            r"теори",
            r"искусствен.*интеллект",
            r"машинн.*обучени",
            r"нейронн.*сет",
            r"computer science",
            r"дискретн",
            r"вычислительн",
        ],
        "SE": [
            r"разработк",
            r"тестирован",
            r"архитектура по",
            r"управлени.*проект",
            r"требовани",
            r"devops",
            r"quality",
            r"качеств",
            r"инженерия по",
            r"software",
        ],
        "IT": [
            r"сет",
            r"администрирован",
            r"операционн.*систем",
            r"облачн",
            r"инфраструктур",
            r"linux",
            r"windows",
            r"сервер",
            r"виртуализац",
        ],
        "IS": [
            r"бизнес",
            r"процесс",
            r"управлени.*предприяти",
            r"erp",
            r"crm",
            r"1с",
            r"экономик",
            r"менеджмент",
            r"маркетинг",
            r"электронн.*коммерц",
        ],
        "CSEC": [
            r"безопасн",
            r"защит",
            r"криптограф",
            r"уязвимост",
            r"атак",
            r"security",
            r"правовы.*аспект",
        ],
        "DS": [
            r"данн",
            r"анализ",
            r"статистик",
            r"big data",
            r"аналитик",
            r"визуализац",
            r"data science",
            r"интеллектуальн.*анализ",
        ],
    }

    def analyze(self, disciplines: QuerySet[ProgramDiscipline]) -> dict:
        scores = {key: 0.0 for key in self.KEYWORDS.keys()}
        total_zet = 0.0

        for pd_obj in disciplines:
            zet_val = self._parse_zet(pd_obj.zet)
            if zet_val <= 0:
                continue

            name_lower = pd_obj.discipline.name.lower()
            matched = False

            for category, patterns in self.KEYWORDS.items():
                for pattern in patterns:
                    if re.search(pattern, name_lower):
                        scores[category] += zet_val
                        matched = True
                        break  # Count discipline only once per category (or remove break to allow multi-category)

            if matched:
                total_zet += zet_val

        # Normalize scores to percentage (0-100) relative to the total analyzed ZET
        # Or relative to the max possible score?
        # Let's return raw ZET sums for now, or percentages of the "categorized" load.

        normalized_scores = {}
        if total_zet > 0:
            for k, v in scores.items():
                normalized_scores[k] = round((v / total_zet) * 100, 2)
        else:
            normalized_scores = scores

        return {
            "scores": normalized_scores,
            "raw_scores": scores,
            "total_analyzed_zet": total_zet,
        }

    def _parse_zet(self, zet_str):
        if not zet_str:
            return 0.0
        try:
            # Replace comma with dot and handle non-numeric chars if necessary
            clean_str = str(zet_str).replace(",", ".").strip()
            return float(clean_str)
        except ValueError:
            return 0.0
