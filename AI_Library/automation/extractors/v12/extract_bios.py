"""
extract_bios.py (v12 — skeleton)

Екстрактор за биографии.
Той ще извлича:
- биографични текстове
- метаданни
- външни линкове (ако има)
- структурирани полета за JSON

Тази версия е архитектурен скелет — без реална логика.
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger


class ExtractBios:
    """
    Екстрактор за биографии (skeleton).
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
    # 1) Зареждане на HTML файлове (skeleton)
    # ---------------------------------------------------------
    def load_source_files(self) -> List[str]:
        """
        Зарежда HTML файловете за биографии.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Зареждане на HTML файлове за биографии.")
        return []

    # ---------------------------------------------------------
    # 2) Извличане на биография от един файл (skeleton)
    # ---------------------------------------------------------
    def extract_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Извлича биографичен текст от един HTML файл.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info(f"(skeleton) Извличане на биография от файл: {file_path}")
        return None

    # ---------------------------------------------------------
    # 3) Записване на JSON резултат (skeleton)
    # ---------------------------------------------------------
    def save_bio_json(self, bio_data: Dict[str, Any]):
        """
        Записва JSON файл за биография.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("(skeleton) Записване на JSON за биография.")

    # ---------------------------------------------------------
    # 4) Главен метод — обхожда всички файлове (skeleton)
    # ---------------------------------------------------------
    def run(self):
        """
        Главен метод — обхожда всички HTML файлове и извлича биографии.
        Реалната логика ще бъде добавена във v12.1.
        """
        self.logger.info("ExtractBios (skeleton) — стартиране.")

        files = self.load_source_files()

        for file_path in files:
            bio_data = self.extract_from_file(file_path)
            if bio_data:
                self.save_bio_json(bio_data)

        self.logger.info("ExtractBios (skeleton) — завършено.")
