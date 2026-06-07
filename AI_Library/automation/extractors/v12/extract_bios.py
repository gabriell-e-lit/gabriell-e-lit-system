"""
extract_bios.py (v12 — extended skeleton)

Екстрактор за биографии.

Архитектурни цели:

- Извличане на КРАТКА биография (short_bio) за:
  - тагове
  - кратки авторски блокове
  - SEO описания

- Извличане на ДЪЛГА биография (long_bio) за:
  - статични авторски страници
  - рубрики от типа „ВЪВ ФОКУСА НИ“

Източници (по приоритет за short_bio):

1) Страници „Автори в брой X“
2) Публикации с H3 „ЗА АВТОРА“ / „ЗА ХУДОЖНИКА“ / „ЗА ТВОРЕЦА“ / „ЗА ИМЕ ФАМИЛИЯ“
3) Тагове (по-късно)
4) Външни източници (по-късно, напр. Уикипедия)

Източници за long_bio:

- специални биографични публикации (напр. „ВЪВ ФОКУСА НИ“)
- други дълги материали за автора

Тази версия е архитектурен скелет — без реална логика.
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger


class ExtractBios:
    """
    Екстрактор за биографии (skeleton, extended).
    """

    def __init__(self, input_dir: str, output_dir: str, logger: Optional[Logger] = None):
        """
        :param input_dir: директория с HTML файлове или други входни данни
        :param output_dir: директория за JSON резултати
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.logger = logger or Logger("ExtractBios")

    # ---------------------------------------------------------
    # 1) Зареждане на източници (skeleton)
    # ---------------------------------------------------------
    def load_issue_pages(self) -> List[str]:
        """
        Зарежда HTML файловете за страници „Автори в брой X“.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Зареждане на страници 'Автори в брой X'.")
        return []

    def load_publications(self) -> List[str]:
        """
        Зарежда HTML файловете за публикации.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Зареждане на публикации.")
        return []

    def load_focus_publications(self) -> List[str]:
        """
        Зарежда HTML файловете за специални биографични публикации
        (напр. рубрика 'ВЪВ ФОКУСА НИ').
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Зареждане на 'фокус' публикации.")
        return []

    # ---------------------------------------------------------
    # 2) Извличане на КРАТКА биография (short_bio) (skeleton)
    # ---------------------------------------------------------
    def extract_short_bio_from_issue_page(self, file_path: str) -> Dict[str, Any]:
        """
        Извлича кратка биография от страница 'Автори в брой X'.
        Очаква се по-късно да връща структура с:
        - author_slug
        - short_bio
        - source
        """
        self.logger.info(f"(skeleton) Извличане на short_bio от issue страница: {file_path}")
        return {}

    def extract_short_bio_from_publication(self, file_path: str) -> Dict[str, Any]:
        """
        Извлича кратка биография от публикация, базирана на H3:
        - 'ЗА АВТОРА'
        - 'ЗА ХУДОЖНИКА'
        - 'ЗА ТВОРЕЦА'
        - 'ЗА ИМЕ ФАМИЛИЯ'

        Очаква се по-късно да връща структура с:
        - author_slug (или временно author_name)
        - short_bio
        - source
        """
        self.logger.info(f"(skeleton) Извличане на short_bio от публикация: {file_path}")
        return {}

    # ---------------------------------------------------------
    # 3) Извличане на ДЪЛГА биография (long_bio) (skeleton)
    # ---------------------------------------------------------
    def extract_long_bio_from_focus_publication(self, file_path: str) -> Dict[str, Any]:
        """
        Извлича дълга биография от специална биографична публикация
        (напр. 'ВЪВ ФОКУСА НИ').

        Очаква се по-късно да връща структура с:
        - author_slug (или временно author_name)
        - long_bio
        - source
        """
        self.logger.info(f"(skeleton) Извличане на long_bio от 'фокус' публикация: {file_path}")
        return {}

    # ---------------------------------------------------------
    # 4) Нормализация и избор на най-подходяща кратка биография (skeleton)
    # ---------------------------------------------------------
    def clean_bio_text(self, raw_text: str) -> str:
        """
        Нормализира биографичен текст:
        - премахва HTML
        - премахва излишни интервали
        - премахва празни редове

        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Нормализация на биографичен текст.")
        return raw_text

    def select_best_short_bio(self, candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Избира най-подходящата КРАТКА биография за автор.

        Приоритет (архитектурно решение):
        1) Биография от 'Автори в брой X'
        2) Биография от публикация (H3 'ЗА АВТОРА' и др.)
        3) Други източници (по-късно)

        НЕ избира най-дългата, а най-редакционно подходящата.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Избор на най-подходяща short_bio.")
        return candidates[0] if candidates else None

    def merge_long_bio_sources(self, candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Комбинира/избира дълга биография (long_bio) от различни източници.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Комбиниране/избор на long_bio.")
        return candidates[0] if candidates else None

    # ---------------------------------------------------------
    # 5) Записване на JSON резултат (skeleton)
    # ---------------------------------------------------------
    def save_bio_json(self, author_slug: str, bio_data: Dict[str, Any]):
        """
        Записва JSON файл за биография на автор.

        Очаквана структура (примерно):
        {
            "author_slug": "...",
            "canonical_name": "...",
            "short_bio": "...",
            "long_bio": "...",
            "sources": {...}
        }

        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info(f"(skeleton) Записване на JSON за биография: {author_slug}")

    # ---------------------------------------------------------
    # 6) Главен метод — orchestration (skeleton)
    # ---------------------------------------------------------
    def run(self):
        """
        Главен метод — orchestration на извличането на биографии.

        Стъпки (концептуално, за бъдещи версии):
        1) Зареждане на issue страници
        2) Зареждане на публикации
        3) Зареждане на 'фокус' публикации
        4) Извличане на short_bio кандидати
        5) Извличане на long_bio кандидати
        6) Нормализация
        7) Избор на best short_bio
        8) Комбиниране на long_bio
        9) Записване на JSON
        """
        self.logger.info("ExtractBios (skeleton, extended) — стартиране.")

        issue_pages = self.load_issue_pages()
        publications = self.load_publications()
        focus_publications = self.load_focus_publications()

        # Тук по-късно ще има реална логика за:
        # - събиране на кандидати за short_bio и long_bio
        # - групиране по author_slug
        # - избор и запис

        self.logger.info("ExtractBios (skeleton, extended) — завършено.")
