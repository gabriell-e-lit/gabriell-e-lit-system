# AI_Library/automation/generators/wordpress/generator_wordpress_tags.py

import requests
from typing import Dict, List, Optional

from AI_Library.utils.text_utils import TextUtils
from AI_Library.utils.logging import Logger
from AI_Library.automation.generators.wordpress.wp_api import WordPressAPI


class TagGenerator:
    """
    Генератор за WordPress тагове (v12).

    Основни задачи:
    - намира или създава WordPress таг за всеки автор
    - обновява съдържанието на тага (биография, снимка, линкове)
    - добавя Wikipedia линк (ако има подаден finder)
    - добавя линк към статичната страница (ако е каноничен автор и има подаден locator)
    - добавя външни линкове
    - добавя линк към тага в страницата „Автори на брой Х“
    """

    def __init__(
        self,
        authors: List[Dict],
        canonical_authors: List[str],
        wp_api: WordPressAPI,
        static_page_locator=None,
        wikipedia_finder=None,
        issue_page_updater=None,
    ):
        self.authors = authors
        self.canonical = canonical_authors
        self.wp = wp_api
        self.static_pages = static_page_locator
        self.wikipedia = wikipedia_finder
        self.issue_page_updater = issue_page_updater
        self.logger = Logger("TagGenerator")

    # ---------------------------------------------------------
    # 1) Главен метод
    # ---------------------------------------------------------
    def run(self):
        for author in self.authors:
            try:
                self.process_author(author)
            except Exception as e:
                self.logger.exception(f"Грешка при обработка на автор: {author.get('name')}: {e}")

    # ---------------------------------------------------------
    # 2) Обработка на един автор
    # ---------------------------------------------------------
    def process_author(self, author: Dict):
        name = self.normalize_name(author["name"])
        slug = TextUtils.slugify(name)

        # 1) намираме или създаваме таг
        tag_id = self.find_or_create_tag(slug, name)

        # 2) събираме съдържанието
        content = self.build_tag_content(author, slug)

        # 3) обновяваме тага
        self.wp.update_tag_content(tag_id, content)

        # 4) обновяваме страницата „Автори на брой Х“
        if self.issue_page_updater:
            self.issue_page_updater.update_issue_page(author["name"], slug)

    # ---------------------------------------------------------
    # 3) Нормализация на името
    # ---------------------------------------------------------
    def normalize_name(self, name: str) -> str:
        return TextUtils.clean_whitespace(name)

    # ---------------------------------------------------------
    # 4) Намиране или създаване на таг
    # ---------------------------------------------------------
    def find_or_create_tag(self, slug: str, name: str) -> int:
        tag = self.wp.find_tag_by_slug(slug)
        if tag:
            return tag["id"]

        self.logger.info(f"Създавам нов таг за {name} ({slug})")
        new_tag = self.wp.create_tag(name=name, slug=slug)
        return new_tag["id"]

    # ---------------------------------------------------------
    # 5) Генериране на HTML съдържание за тага
    # ---------------------------------------------------------
    def build_tag_content(self, author: Dict, slug: str) -> str:
        parts = []

        # Име
        parts.append(f"<h2>{author['name']}</h2>")

        # Снимка
        if author.get("image_url"):
            parts.append(f'<p><img src="{author["image_url"]}" alt="{author["name"]}"></p>')

        # Биография
        if author.get("bio"):
            parts.append(f"<p>{author['bio']}</p>")

        # Wikipedia
        if self.wikipedia:
            wiki = self.wikipedia.find(author["name"])
            if wiki:
                parts.append(f'<p><a href="{wiki}" target="_blank">Wikipedia</a></p>')

        # Статична страница
        if author["name"] in self.canonical and self.static_pages:
            static_page = self.static_pages.get_static_page(slug)
            if static_page:
                parts.append(
                    f'<p><a href="{static_page}" target="_blank">Статична страница</a></p>'
                )

        # Външни линкове
        for link in author.get("external_links", []):
            parts.append(f'<p><a href="{link["url"]}" target="_blank">{link["label"]}</a></p>')

        return "\n".join(parts)
