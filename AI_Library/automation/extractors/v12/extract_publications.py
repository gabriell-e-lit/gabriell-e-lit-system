"""
extract_publications.py (v12 — corrected architecture skeleton)

Екстрактор за публикации в платформата gabriell-e-lit.

ВАЖНО УТОЧНЕНИЕ:
Публикациите съществуват САМО като WordPress динамични елементи.
Няма статични HTML файлове за публикации.
Няма статични страници за публикации.
Няма локални HTML копия на публикации.

Следователно:
- Извличаме публикации САМО чрез WordPress REST API.
- Извличаме линкове от content.rendered (HTML, върнат от API).
- Записваме вътрешни JSON файлове за автоматизация.
- НЕ генерираме статични HTML страници за публикации.
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger
import requests
import json
import os
import re


class ExtractPublications:
    """
    Екстрактор за публикации (final corrected skeleton).
    """

    WP_API_BASE = "https://gabriell-e-lit.com/wp-json/wp/v2"

    def __init__(
        self,
        output_dir: str,
        authors_index: Dict[str, Any],
        issues_index: Dict[str, Any],
        logger: Optional[Logger] = None
    ):
        """
        :param output_dir: директория за JSON резултати (publications/)
        :param authors_index: индекс на автори (от extract_authors)
        :param issues_index: индекс на броеве (от extract_issues)
        """
        self.output_dir = output_dir
        self.authors_index = authors_index
        self.issues_index = issues_index
        self.logger = logger or Logger("ExtractPublications")

    # ---------------------------------------------------------
    # 1) REST API helper (skeleton)
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
    # 2) Извличане на всички публикации (skeleton)
    # ---------------------------------------------------------
    def get_all_publications(self) -> List[Dict[str, Any]]:
        """
        Извлича всички публикации чрез REST API.
        Няма HTML scraping.
        """
        self.logger.info("(skeleton) Извличане на всички публикации.")
        return []

    # ---------------------------------------------------------
    # 3) Извличане на author_slug (skeleton)
    # ---------------------------------------------------------
    def resolve_author_slug(self, wp_author_id: int) -> Optional[str]:
        """
        Намира author_slug чрез authors_index.
        """
        self.logger.info(f"(skeleton) Намиране на author_slug за WP author ID {wp_author_id}.")
        return None

    # ---------------------------------------------------------
    # 4) Извличане на issue_id (съответния брой) (skeleton)
    # ---------------------------------------------------------
    def resolve_issue_id(self, category_ids: List[int]) -> Optional[str]:
        """
        Намира issue_id чрез issues_index.
        """
        self.logger.info("(skeleton) Намиране на issue_id за публикация.")
        return None

    # ---------------------------------------------------------
    # 5) Извличане на роли (skeleton)
    # ---------------------------------------------------------
    def extract_roles(self, tags: List[int]) -> List[str]:
        """
        Извлича роли (поет, прозаик, есеист...) от тагове или custom fields.
        """
        self.logger.info("(skeleton) Извличане на роли.")
        return []

    # ---------------------------------------------------------
    # 6) Извличане на тип (поезия, проза...) (skeleton)
    # ---------------------------------------------------------
    def extract_type(self, category_ids: List[int], tags: List[int]) -> Optional[str]:
        """
        Определя типа на публикацията.
        """
        self.logger.info("(skeleton) Определяне на тип публикация.")
        return None

    # ---------------------------------------------------------
    # 7) Извличане на линкове от content.rendered (skeleton)
    # ---------------------------------------------------------
    def extract_links_from_content(self, html: str) -> List[str]:
        """
        Извлича всички <a href="..."> линкове от HTML съдържанието,
        върнато от WordPress REST API.
        """
        self.logger.info("(skeleton) Извличане на линкове от content.rendered.")
        return []

    # ---------------------------------------------------------
    # 8) Структуриране на JSON за публикация (skeleton)
    # ---------------------------------------------------------
    def build_publication_json(
        self,
        wp_data: Dict[str, Any],
        author_slug: Optional[str],
        issue_id: Optional[str],
        roles: List[str],
        pub_type: Optional[str],
        links: List[str]
    ) -> Dict[str, Any]:
        """
        Структурира финалния JSON за публикация.
        """
        self.logger.info(f"(skeleton) Структуриране на JSON за публикация {wp_data.get('slug')}.")

        return {
            "publication_id": wp_data.get("slug"),
            "title": wp_data.get("title", {}).get("rendered"),
            "author_slug": author_slug,
            "issue_id": issue_id,
            "roles": roles,
            "type": pub_type,
            "date": wp_data.get("date"),
            "modified": wp_data.get("modified"),
            "excerpt": wp_data.get("excerpt", {}).get("rendered"),
            "content": wp_data.get("content", {}).get("rendered"),
            "links": links,
            "wp_id": wp_data.get("id"),
            "wp_url": wp_data.get("link")
        }

    # ---------------------------------------------------------
    # 9) Записване на JSON (skeleton)
    # ---------------------------------------------------------
    def save_publication_json(self, pub_id: str, data: Dict[str, Any]):
        """
        Записва JSON файл за публикация.
        """
        self.logger.info(f"(skeleton) Записване на JSON за публикация: {pub_id}")

        output_path = os.path.join(self.output_dir, f"{pub_id}.json")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            self.logger.error(f"(skeleton) Грешка при запис на JSON за {pub_id}")

    # ---------------------------------------------------------
    # 10) Главен метод — orchestration (skeleton)
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("ExtractPublications (final corrected skeleton) — стартиране.")

        publications = self.get_all_publications()

        for wp_data in publications:
            author_slug = self.resolve_author_slug(wp_data.get("author"))
            issue_id = self.resolve_issue_id(wp_data.get("categories"))
            roles = self.extract_roles(wp_data.get("tags"))
            pub_type = self.extract_type(wp_data.get("categories"), wp_data.get("tags"))
            links = self.extract_links_from_content(wp_data.get("content", {}).get("rendered", ""))

            pub_json = self.build_publication_json(
                wp_data,
                author_slug,
                issue_id,
                roles,
                pub_type,
                links
            )

            self.save_publication_json(pub_json["publication_id"], pub_json)

        self.logger.info("ExtractPublications (final corrected skeleton) — завършено.")
