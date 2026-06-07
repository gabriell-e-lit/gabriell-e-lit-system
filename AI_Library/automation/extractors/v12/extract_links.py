"""
extract_links.py (v12 — final architecture skeleton)

Екстрактор за връзки в платформата gabriell-e-lit.

Работи върху:
- HTML публикации (по избор)
- HTML WordPress страници (по избор)
- статични HTML страници (генерирани от системата)
- JSON файлове (authors, bios, issues)
- медийни файлове (по избор)

НЕ работи върху публични URL на JSON файловете (те не съществуват).
Извлича линкове само от съдържанието на JSON/HTML.
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger
import os
import json
import re
import requests


class ExtractLinks:
    """
    Екстрактор за връзки (final skeleton).
    """

    DOMAIN = "gabriell-e-lit.com"

    def __init__(
        self,
        input_dirs: Dict[str, str],
        output_dir: str,
        logger: Optional[Logger] = None
    ):
        """
        :param input_dirs: директории с HTML, JSON и други входни данни
        :param output_dir: директория за JSON резултати (links/)
        """
        self.input_dirs = input_dirs
        self.output_dir = output_dir
        self.logger = logger or Logger("ExtractLinks")

    # ---------------------------------------------------------
    # 1) Зареждане на HTML файлове (skeleton)
    # ---------------------------------------------------------
    def load_html_files(self, directory: str) -> List[str]:
        self.logger.info(f"(skeleton) Зареждане на HTML файлове от {directory}.")
        return []

    # ---------------------------------------------------------
    # 2) Зареждане на JSON файлове (skeleton)
    # ---------------------------------------------------------
    def load_json_files(self, directory: str) -> List[Dict[str, Any]]:
        self.logger.info(f"(skeleton) Зареждане на JSON файлове от {directory}.")
        return []

    # ---------------------------------------------------------
    # 3) Извличане на линкове от HTML (skeleton)
    # ---------------------------------------------------------
    def extract_links_from_html(self, html: str) -> List[str]:
        self.logger.info("(skeleton) Извличане на линкове от HTML.")
        return []

    # ---------------------------------------------------------
    # 4) Извличане на линкове от JSON (skeleton)
    # ---------------------------------------------------------
    def extract_links_from_json(self, data: Dict[str, Any]) -> List[str]:
        self.logger.info("(skeleton) Извличане на линкове от JSON.")
        return []

    # ---------------------------------------------------------
    # 5) Класификация на линкове (skeleton)
    # ---------------------------------------------------------
    def classify_link(self, url: str) -> str:
        self.logger.info(f"(skeleton) Класификация на линк: {url}")
        return "internal"

    # ---------------------------------------------------------
    # 6) Нормализация на вътрешни линкове (skeleton)
    # ---------------------------------------------------------
    def normalize_internal_link(self, url: str) -> str:
        self.logger.info(f"(skeleton) Нормализация на вътрешен линк: {url}")
        return url

    # ---------------------------------------------------------
    # 7) Проверка на валидност (skeleton)
    # ---------------------------------------------------------
    def check_link_status(self, url: str) -> Dict[str, Any]:
        self.logger.info(f"(skeleton) Проверка на линк: {url}")
        return {
            "url": url,
            "status": None,
            "redirect": None
        }

    # ---------------------------------------------------------
    # 8) Записване на резултати (skeleton)
    # ---------------------------------------------------------
    def save_links_json(self, filename: str, data: Any):
        self.logger.info(f"(skeleton) Записване на {filename}.")
        output_path = os.path.join(self.output_dir, filename)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            self.logger.error(f"(skeleton) Грешка при запис на {filename}")

    # ---------------------------------------------------------
    # 9) Главен метод — orchestration (skeleton)
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("ExtractLinks (final skeleton) — стартиране.")

        all_links = []
        internal_links = []
        external_links = []
        media_links = []
        broken_links = []
        redirects = []

        # 1) HTML файлове
        for key, directory in self.input_dirs.items():
            if key.endswith("_html") or key == "static_pages":
                html_files = self.load_html_files(directory)
                for html in html_files:
                    links = self.extract_links_from_html(html)
                    all_links.extend(links)

        # 2) JSON файлове
        for key, directory in self.input_dirs.items():
            if key.endswith("_json"):
                json_files = self.load_json_files(directory)
                for data in json_files:
                    links = self.extract_links_from_json(data)
                    all_links.extend(links)

        # 3) Класификация и нормализация
        for url in all_links:
            category = self.classify_link(url)

            if category == "internal":
                normalized = self.normalize_internal_link(url)
                internal_links.append(normalized)

            elif category == "external":
                external_links.append(url)

            elif category in ("media", "wp_media"):
                media_links.append(url)

        # 4) Проверка на валидност
        for url in internal_links + external_links:
            status = self.check_link_status(url)

            if status["status"] == 404:
                broken_links.append(status)

            if status["redirect"]:
                redirects.append(status)

        # 5) Записване на резултати
        self.save_links_json("internal_links.json", internal_links)
        self.save_links_json("external_links.json", external_links)
        self.save_links_json("media_links.json", media_links)
        self.save_links_json("broken_links.json", broken_links)
        self.save_links_json("redirects.json", redirects)

        self.logger.info("ExtractLinks (final skeleton) — завършено.")
