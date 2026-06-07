"""
extract_books.py (v12 — final architecture skeleton)

Екстрактор за книги в платформата gabriell-e-lit.

Архитектурни цели:

1) Разпознаване на книги чрез WordPress тагове и жанрови страници.
2) Извличане на:
   - заглавие
   - автор(и)
   - кратко описание
   - жанр(ове)
   - корици (ebook/print)
   - формати (pdf, epub, pbook, audio)
   - връзка към пълното съдържание (статичен сайт)
   - рецензии и откъси (WordPress публикации)
3) Създаване на два модела:
   - BookModel (пълна книга — за статична страница)
   - BookCellModel (разпределител — за каталози)
4) Записване в:
   output/books/<book_slug>.json
   output/book_cells/<book_slug>.json
"""

from typing import Optional, Dict, Any, List
from AI_Library.utils.logging import Logger
import requests
import json
import os
import re


class ExtractBooks:
    """
    Екстрактор за книги (final skeleton).
    """

    WP_API_BASE = "https://gabriell-e-lit.com/wp-json/wp/v2"

    def __init__(
        self,
        output_dir_books: str,
        output_dir_cells: str,
        authors_index: Dict[str, Any],
        logger: Optional[Logger] = None
    ):
        """
        :param output_dir_books: директория за BookModel JSON
        :param output_dir_cells: директория за BookCellModel JSON
        :param authors_index: индекс на автори (от extract_authors)
        """
        self.output_dir_books = output_dir_books
        self.output_dir_cells = output_dir_cells
        self.authors_index = authors_index
        self.logger = logger or Logger("ExtractBooks")

    # ---------------------------------------------------------
    # 1) REST API helper (skeleton)
    # ---------------------------------------------------------
    def api_get(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        url = f"{self.WP_API_BASE}/{endpoint}"
        self.logger.info(f"(skeleton) API GET: {url}")
        return None

    # ---------------------------------------------------------
    # 2) Извличане на тагове, които представляват книги (skeleton)
    # ---------------------------------------------------------
    def get_book_tags(self) -> List[Dict[str, Any]]:
        """
        Намира тагове, които представляват книги.
        Алгоритъм:
        - име на тага съдържа „ – “ (заглавие – автор)
        - има описание или свързани публикации
        """
        self.logger.info("(skeleton) Извличане на тагове за книги.")
        return []

    # ---------------------------------------------------------
    # 3) Парсване на заглавие и автор(и) от име на таг (skeleton)
    # ---------------------------------------------------------
    def parse_title_and_authors(self, tag_name: str) -> Dict[str, Any]:
        """
        Пример:
        'Зад гърба – Габриела Цанева'
        -> title='Зад гърба', authors=['gabriela-caneva']
        """
        self.logger.info(f"(skeleton) Парсване на заглавие и автори от таг: {tag_name}")
        return {
            "title": None,
            "authors": []
        }

    # ---------------------------------------------------------
    # 4) Извличане на публикации (рецензии, откъси) (skeleton)
    # ---------------------------------------------------------
    def get_related_publications(self, tag_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """
        Връща:
        {
            "reviews": [...],
            "excerpts": [...]
        }
        """
        self.logger.info(f"(skeleton) Извличане на публикации за таг (книга) {tag_id}.")
        return {
            "reviews": [],
            "excerpts": []
        }

    # ---------------------------------------------------------
    # 5) Извличане на жанрова информация (skeleton)
    # ---------------------------------------------------------
    def get_genres_for_book(self, tag_slug: str) -> List[str]:
        """
        Намира жанрове чрез жанрови страници или категории.
        """
        self.logger.info(f"(skeleton) Извличане на жанрове за книга {tag_slug}.")
        return []

    # ---------------------------------------------------------
    # 6) Извличане на корици (skeleton)
    # ---------------------------------------------------------
    def get_covers(self, tag_slug: str) -> Dict[str, Any]:
        """
        Намира корици от:
        - жанрови страници
        - RSS
        - статичен сайт
        """
        self.logger.info(f"(skeleton) Извличане на корици за книга {tag_slug}.")
        return {
            "ebook_url": "",
            "ebook_alt": "",
            "print_url": "",
            "print_alt": ""
        }

    # ---------------------------------------------------------
    # 7) Извличане на формати (skeleton)
    # ---------------------------------------------------------
    def get_formats(self, tag_slug: str) -> Dict[str, Any]:
        """
        Намира PDF, EPUB, печатна книга, аудио.
        """
        self.logger.info(f"(skeleton) Извличане на формати за книга {tag_slug}.")
        return {
            "pdf_url": "",
            "epub_url": "",
            "pbook_url": "",
            "audio_url": ""
        }

    # ---------------------------------------------------------
    # 8) Извличане на връзка към пълното съдържание (skeleton)
    # ---------------------------------------------------------
    def get_full_content_url(self, tag_slug: str) -> Optional[str]:
        """
        Намира линк към статичния сайт.
        """
        self.logger.info(f"(skeleton) Извличане на full_content_url за книга {tag_slug}.")
        return None

    # ---------------------------------------------------------
    # 9) Създаване на BookModel (skeleton)
    # ---------------------------------------------------------
    def build_book_model(
        self,
        tag_data: Dict[str, Any],
        title: str,
        authors: List[str],
        genres: List[str],
        covers: Dict[str, Any],
        formats: Dict[str, Any],
        full_content_url: Optional[str],
        related_pubs: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Създава пълния модел на книга (за статична страница).
        """
        self.logger.info(f"(skeleton) Създаване на BookModel за {tag_data.get('slug')}.")

        return {
            "seo": {
                "title": title,
                "description": tag_data.get("description", ""),
                "canonical_url": f"/books/{tag_data.get('slug')}/"
            },

            "metadata": {
                "title": title,
                "author": ", ".join(authors),
                "genre": ", ".join(genres),
                "year": "",
                "pages": "",
                "binding_print": "",
                "format_print": "",
                "isbn_print": "",
                "isbn_pdf": "",
                "isbn_epub": ""
            },

            "cover": covers,
            "formats": formats,

            "links": {
                "author_page_url": "",
                "tag_url": tag_data.get("link"),
                "registry_url": "",
                "goodreads_url": "",
                "bookstore_url": ""
            },

            "intro": "",
            "description": tag_data.get("description", ""),

            "reviews": [
                {
                    "text": "",
                    "source_url": pub.get("link"),
                    "source_label": pub.get("title", {}).get("rendered")
                }
                for pub in related_pubs.get("reviews", [])
            ],

            "navigation": {
                "alphabetical": True,
                "genre": True
            },

            "visual": {
                "include_book_cell": True
            }
        }

    # ---------------------------------------------------------
    # 10) Създаване на BookCellModel (skeleton)
    # ---------------------------------------------------------
    def build_book_cell_model(
        self,
        tag_slug: str,
        title: str,
        authors: List[str],
        covers: Dict[str, Any],
        formats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Създава опростения модел за каталози.
        """
        self.logger.info(f"(skeleton) Създаване на BookCellModel за {tag_slug}.")

        return {
            "book_page_url": f"/books/{tag_slug}/",
            "title": title,
            "author_name": ", ".join(authors),
            "author_page_url": "",

            "covers": covers,
            "formats": formats,

            "display": {
                "show_author": True,
                "show_formats": True,
                "show_double_cover": True
            }
        }

    # ---------------------------------------------------------
    # 11) Записване на JSON (skeleton)
    # ---------------------------------------------------------
    def save_json(self, directory: str, slug: str, data: Dict[str, Any]):
        self.logger.info(f"(skeleton) Записване на JSON за книга: {slug}")

        output_path = os.path.join(directory, f"{slug}.json")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            self.logger.error(f"(skeleton) Грешка при запис на JSON за {slug}")

    # ---------------------------------------------------------
    # 12) Главен метод — orchestration (skeleton)
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("ExtractBooks (final skeleton) — стартиране.")

        book_tags = self.get_book_tags()

        for tag_data in book_tags:
            tag_slug = tag_data.get("slug")
            tag_name = tag_data.get("name")

            parsed = self.parse_title_and_authors(tag_name)
            title = parsed["title"]
            authors = parsed["authors"]

            genres = self.get_genres_for_book(tag_slug)
            covers = self.get_covers(tag_slug)
            formats = self.get_formats(tag_slug)
            full_content_url = self.get_full_content_url(tag_slug)
            related_pubs = self.get_related_publications(tag_data.get("id"))

            book_model = self.build_book_model(
                tag_data,
                title,
                authors,
                genres,
                covers,
                formats,
                full_content_url,
                related_pubs
            )

            book_cell = self.build_book_cell_model(
                tag_slug,
                title,
                authors,
                covers,
                formats
            )

            self.save_json(self.output_dir_books, tag_slug, book_model)
            self.save_json(self.output_dir_cells, tag_slug, book_cell)

        self.logger.info("ExtractBooks (final skeleton) — завършено.")
