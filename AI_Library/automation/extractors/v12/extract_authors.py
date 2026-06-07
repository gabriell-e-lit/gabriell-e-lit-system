"""
extract_authors.py (v12 — extended skeleton)

Екстрактор за автори.

Архитектурни цели:

- Извличане на основни авторски данни (име, slug, роли, произведения)
- Зареждане на short_bio и long_bio от ExtractBios
- Комбиниране на данните в един author JSON
- Подготовка за статични страници и WordPress генератори

Тази версия е архитектурен скелет — без реална логика.
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger
import os
import json


class ExtractAuthors:
    """
    Екстрактор за автори (skeleton, extended).
    """

    def __init__(self, input_dir: str, output_dir: str, bios_dir: str, logger: Optional[Logger] = None):
        """
        :param input_dir: директория с HTML файлове или други входни данни
        :param output_dir: директория за JSON резултати (authors/)
        :param bios_dir: директория с JSON файлове от ExtractBios
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.bios_dir = bios_dir
        self.logger = logger or Logger("ExtractAuthors")

    # ---------------------------------------------------------
    # 1) Зареждане на HTML файлове (skeleton)
    # ---------------------------------------------------------
    def load_source_files(self) -> List[str]:
        self.logger.info("(skeleton) Зареждане на HTML файлове за автори.")
        return []

    # ---------------------------------------------------------
    # 2) Извличане на основни авторски данни (skeleton)
    # ---------------------------------------------------------
    def extract_author_core(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Извлича основни данни за автора:
        - canonical_name
        - author_slug
        - roles
        - works (ако има)
        """
        self.logger.info(f"(skeleton) Извличане на основни данни от файл: {file_path}")
        return None

    # ---------------------------------------------------------
    # 3) Зареждане на биографии от ExtractBios (skeleton)
    # ---------------------------------------------------------
    def load_bio_json(self, author_slug: str) -> Dict[str, Any]:
        """
        Зарежда JSON файл за биография на автора, ако съществува.
        Очаква структура:
        {
            "short_bio": "...",
            "long_bio": "...",
            "sources": {...}
        }
        """
        bio_path = os.path.join(self.bios_dir, f"{author_slug}.json")

        if not os.path.exists(bio_path):
            self.logger.info(f"(skeleton) Няма биография за {author_slug}.")
            return {}

        self.logger.info(f"(skeleton) Зареждане на биография за {author_slug}.")
        try:
            with open(bio_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    # ---------------------------------------------------------
    # 4) Комбиниране на данните (skeleton)
    # ---------------------------------------------------------
    def merge_author_data(self, core_data: Dict[str, Any], bio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Комбинира основните авторски данни с биографичните данни.
        """
        self.logger.info("(skeleton) Комбиниране на авторски данни с биография.")

        merged = core_data.copy()

        merged["short_bio"] = bio_data.get("short_bio")
        merged["long_bio"] = bio_data.get("long_bio")
        merged["bio_sources"] = bio_data.get("sources")

        return merged

    # ---------------------------------------------------------
    # 5) Записване на author JSON (skeleton)
    # ---------------------------------------------------------
    def save_author_json(self, author_slug: str, author_data: Dict[str, Any]):
        """
        Записва финалния JSON файл за автора.
        """
        self.logger.info(f"(skeleton) Записване на JSON за автор: {author_slug}")

        output_path = os.path.join(self.output_dir, f"{author_slug}.json")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(author_data, f, ensure_ascii=False, indent=2)
        except Exception:
            self.logger.error(f"(skeleton) Грешка при запис на JSON за {author_slug}")

    # ---------------------------------------------------------
    # 6) Главен метод — orchestration (skeleton)
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("ExtractAuthors (skeleton, extended) — стартиране.")

        files = self.load_source_files()

        for file_path in files:
            core_data = self.extract_author_core(file_path)
            if not core_data:
                continue

            slug = core_data.get("author_slug")
            bio_data = self.load_bio_json(slug)

            merged = self.merge_author_data(core_data, bio_data)
            self.save_author_json(slug, merged)

        self.logger.info("ExtractAuthors (skeleton, extended) — завършено.")
