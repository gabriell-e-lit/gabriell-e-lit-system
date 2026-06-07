"""
extract_authors.py (v12 — skeleton)

Екстрактор за автори.
Той ще извлича:
- имена
- биографични данни
- линкове
- снимки
- списък с произведения
- метаданни за нормализация

Тази версия е архитектурен скелет — без реална логика.
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger


class ExtractAuthors:
    """
    Екстрактор за автори (skeleton).
    """

    def __init__(self, input_dir: str, output_dir: str, logger: Optional[Logger] = None):
        """
        :param input_dir: директория с HTML файлове или други входни данни
        :param output_dir: директория за JSON резултати
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.logger = logger or Logger("ExtractAuthors")

    # ---------------------------------------------------------
    # 1) Зареждане на HTML/текстови файлове (skeleton)
    # ---------------------------------------------------------
    def load_source_files(self) -> List[str]:
        """
        Зарежда HTML файловете за автори.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Зареждане на HTML файлове за автори.")
        return []

    # ---------------------------------------------------------
    # 2) Извличане на данни от един файл (skeleton)
    # ---------------------------------------------------------
    def extract_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Извлича данни за автор от един HTML файл.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info(f"(skeleton) Извличане на данни от файл: {file_path}")
        return None

    # ---------------------------------------------------------
    # 3) Записване на JSON резултат (skeleton)
    # ---------------------------------------------------------
    def save_author_json(self, author_data: Dict[str, Any]):
        """
        Записва JSON файл за автор.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Записване на JSON за автор.")

    # ---------------------------------------------------------
    # 4) Главен метод — обхожда всички файлове (skeleton)
    # ---------------------------------------------------------
    def run(self):
        """
        Главен метод — обхожда всички HTML файлове и извлича автори.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("ExtractAuthors (skeleton) — стартиране.")

        files = self.load_source_files()

        for file_path in files:
            author_data = self.extract_from_file(file_path)
            if author_data:
                self.save_author_json(author_data)

        self.logger.info("ExtractAuthors (skeleton) — завършено.")
