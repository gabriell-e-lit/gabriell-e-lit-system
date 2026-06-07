"""
extract_issues.py (v12 — final architecture skeleton)

Екстрактор за броевете на списанието „Картини с думи и багри“.

Работи чрез WordPress REST API и извлича:

1) Йерархия на категориите:
   - root категория: spisanie-kartini-s-dumi-i-bagri
   - годишни категории (2024, 2023, ...)
   - брой категории (4-2024, 3-2024, ..., 0-2018)

2) Метаданни за брой:
   - issue_id (slug)
   - title (име на категорията)
   - description (описание на броя)
   - cover_image (featured image на категорията)

3) Публикации в броя:
   - title
   - url
   - author_slug
   - roles (ако има)
   - type (поезия, проза, есе...)

ВАЖНО:
- НЕ извлича биографии (това е работа на ExtractBios)
- НЕ анализира HTML
- Работи само чрез WordPress REST API
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger
import requests
import json
import os


class ExtractIssues:
    """
    Екстрактор за броеве (WordPress REST API, final skeleton).
    """

    WP_API_BASE = "https://gabriell-e-lit.com/wp-json/wp/v2"

    ROOT_CATEGORY_SLUG = "spisanie-kartini-s-dumi-i-bagri"

    def __init__(self, output_dir: str, logger: Optional[Logger] = None):
        """
        :param output_dir: директория за JSON резултати (issues/)
        """
        self.output_dir = output_dir
        self.logger = logger or Logger("ExtractIssues")

    # ---------------------------------------------------------
    # 1) Помощни методи за REST API (skeleton)
    # ---------------------------------------------------------
    def api_get(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        """
        Извършва GET заявка към WordPress REST API.
        Реалната логика ще бъде добавена във v12.1.
        """
        url = f"{self.WP_API_BASE}/{endpoint}"
        self.logger.info(f"(skeleton) API GET: {url}")
        return None

    # ---------------------------------------------------------
    # 2) Намиране на root категорията (skeleton)
    # ---------------------------------------------------------
    def get_root_category(self) -> Optional[Dict[str, Any]]:
        """
        Намира root категорията по slug:
        spisanie-kartini-s-dumi-i-bagri
        """
        self.logger.info("(skeleton) Търсене на root категорията.")
        return None

    # ---------------------------------------------------------
    # 3) Намиране на годишните категории (skeleton)
    # ---------------------------------------------------------
    def get_year_categories(self, root_id: int) -> List[Dict[str, Any]]:
        """
        Намира всички годишни категории (2024, 2023, ...),
        които са деца на root категорията.
        """
        self.logger.info("(skeleton) Извличане на годишни категории.")
        return []

    # ---------------------------------------------------------
    # 4) Намиране на брой категории (skeleton)
    # ---------------------------------------------------------
    def get_issue_categories(self, year_category_id: int) -> List[Dict[str, Any]]:
        """
        Намира всички брой категории (4-2024, 3-2024, ...),
        които са деца на годишната категория.
        """
        self.logger.info(f"(skeleton) Извличане на брой категории за година {year_category_id}.")
        return []

    def get_orphan_issue_categories(self, root_id: int) -> List[Dict[str, Any]]:
        """
        Намира брой категории, които са директни деца на root категорията.
        Това покрива специалния случай: 0-2018.
        """
        self.logger.info("(skeleton) Извличане на 'осиротели' брой категории (напр. 0-2018).")
        return []

    # ---------------------------------------------------------
    # 5) Извличане на публикации в брой (skeleton)
    # ---------------------------------------------------------
    def get_issue_posts(self, issue_category_id: int) -> List[Dict[str, Any]]:
        """
        Извлича публикациите в дадена категория 'брой'.
        """
        self.logger.info(f"(skeleton) Извличане на публикации за брой {issue_category_id}.")
        return []

    # ---------------------------------------------------------
    # 6) Извличане на метаданни за брой (skeleton)
    # ---------------------------------------------------------
    def extract_issue_metadata(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Извлича:
        - issue_id (slug)
        - title
        - description
        - cover_image (ако темата го поддържа)
        """
        self.logger.info(f"(skeleton) Извличане на метаданни за брой: {category_data.get('slug')}")
        return {}

    # ---------------------------------------------------------
    # 7) Комбиниране на данни за брой (skeleton)
    # ---------------------------------------------------------
    def merge_issue_data(
        self,
        metadata: Dict[str, Any],
        posts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Комбинира метаданни и публикации в един issue JSON.
        """
        self.logger.info("(skeleton) Комбиниране на данни за брой.")
        return {
            "issue_id": metadata.get("issue_id"),
            "title": metadata.get("title"),
            "description": metadata.get("description"),
            "cover_image": metadata.get("cover_image"),
            "publications": posts
        }

    # ---------------------------------------------------------
    # 8) Записване на issue JSON (skeleton)
    # ---------------------------------------------------------
    def save_issue_json(self, issue_id: str, issue_data: Dict[str, Any]):
        """
        Записва финалния JSON файл за брой.
        """
        self.logger.info(f"(skeleton) Записване на JSON за брой: {issue_id}")

        output_path = os.path.join(self.output_dir, f"{issue_id}.json")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(issue_data, f, ensure_ascii=False, indent=2)
        except Exception:
            self.logger.error(f"(skeleton) Грешка при запис на JSON за {issue_id}")

    # ---------------------------------------------------------
    # 9) Главен метод — orchestration (skeleton)
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("ExtractIssues (final skeleton) — стартиране.")

        root = self.get_root_category()
        if not root:
            self.logger.error("Root категорията не е намерена.")
            return

        root_id = root.get("id")

        year_categories = self.get_year_categories(root_id)
        orphan_issues = self.get_orphan_issue_categories(root_id)

        # Обработка на годишните категории
        for year_cat in year_categories:
            year_id = year_cat.get("id")
            issue_categories = self.get_issue_categories(year_id)

            for issue_cat in issue_categories:
                metadata = self.extract_issue_metadata(issue_cat)
                posts = self.get_issue_posts(issue_cat.get("id"))
                merged = self.merge_issue_data(metadata, posts)
                self.save_issue_json(metadata.get("issue_id"), merged)

        # Обработка на специални броеве (напр. 0-2018)
        for issue_cat in orphan_issues:
            metadata = self.extract_issue_metadata(issue_cat)
            posts = self.get_issue_posts(issue_cat.get("id"))
            merged = self.merge_issue_data(metadata, posts)
            self.save_issue_json(metadata.get("issue_id"), merged)

        self.logger.info("ExtractIssues (final skeleton) — завършено.")
