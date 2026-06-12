# BookCellCollectorAdapter_v1_0.py

from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import re

from bs4 import BeautifulSoup

from system.models.book_cell.BookCellModel_v2_0 import (
    BookCellModel,
    BookCellCovers,
    BookCellFormats,
    BookCellDisplay,
)
from system.models.book_cell.BookCellModel_v2_0_builder import build_book_cell_from_raw

from system.services.SlugifyService_v1_0 import SlugifyServiceV1_0
from system.resolvers.GenreResolver_v1_0 import GenreResolverV1_0
from system.resolvers.BookPageURLResolver_v1_0 import BookPageURLResolverV1_0


class BookCellCollectorAdapterV1_0:
    """
    Универсален адаптер, който:
      - парсва book_cell елементи от HTML
      - нормализира данните
      - определя жанра (GenreResolver)
      - генерира slug (SlugifyService)
      - генерира URL за статична страница (BookPageURLResolver)
      - връща BookCellModel_v2_0
    """

    def __init__(self, source_url: str):
        self.source_url = source_url

        # Интегрирани услуги
        self.slugify = SlugifyServiceV1_0()
        self.genre_resolver = GenreResolverV1_0()
        self.url_resolver = BookPageURLResolverV1_0()

    # ---------------------------------------------------------
    # Публичен метод
    # ---------------------------------------------------------

    def collect(self, html: str) -> List[BookCellModel]:
        """
        Парсва HTML и връща списък от BookCellModel.
        """
        soup = BeautifulSoup(html, "html.parser")
        cells = soup.select(".book_cell")

        results = []
        for cell in cells:
            raw = self.parse_cell(cell)
            model = build_book_cell_from_raw(raw)
            results.append(model)

        return results

    # ---------------------------------------------------------
    # Парсване на единична клетка
    # ---------------------------------------------------------

    def parse_cell(self, cell) -> Dict[str, Any]:
        """
        Извлича сурови данни от HTML елемент .book_cell
        и ги нормализира.
        """

        # Заглавие
        title_el = cell.select_one(".book_title")
        title = title_el.get_text(strip=True) if title_el else ""

        # Автор
        author_el = cell.select_one(".book_author")
        author_name = author_el.get_text(strip=True) if author_el else ""

        # Линк към авторска страница (ако има)
        author_link_el = cell.select_one(".book_author a")
        author_page_url = author_link_el["href"] if author_link_el else ""

        # Корици
        cover_ebook_el = cell.select_one(".cover_ebook img")
        cover_print_el = cell.select_one(".cover_print img")

        cover_ebook_url = cover_ebook_el["src"] if cover_ebook_el else ""
        cover_print_url = cover_print_el["src"] if cover_print_el else ""

        cover_ebook_alt = cover_ebook_el.get("alt", "") if cover_ebook_el else ""
        cover_print_alt = cover_print_el.get("alt", "") if cover_print_el else ""

        # Формати
        pdf_el = cell.select_one(".format_pdf a")
        epub_el = cell.select_one(".format_epub a")
        pbook_el = cell.select_one(".format_pbook a")
        audio_el = cell.select_one(".format_audio a")

        pdf_url = pdf_el["href"] if pdf_el else ""
        epub_url = epub_el["href"] if epub_el else ""
        pbook_url = pbook_el["href"] if pbook_el else ""
        audio_url = audio_el["href"] if audio_el else ""

        # ---------------------------------------------------------
        # Жанр (GenreResolver)
        # ---------------------------------------------------------

        genre_info = self.genre_resolver.resolve(
            source_url=self.source_url,
            cover_url=cover_ebook_url or cover_print_url,
            pdf_url=pdf_url,
        )

        primary_genre = genre_info["primary_genre"]

        # ---------------------------------------------------------
        # Slug (SlugifyService)
        # ---------------------------------------------------------

        if pdf_url:
            # slug от PDF filename
            pdf_name = pdf_url.split("/")[-1].split(".")[0]
            slug = self.slugify.remove_dashes(pdf_name)
        else:
            # slug от заглавие
            slug = self.slugify.from_title(title)

        # ---------------------------------------------------------
        # URL за статична страница (BookPageURLResolver)
        # ---------------------------------------------------------

        book_page_url = self.url_resolver.resolve(primary_genre, slug)

        # ---------------------------------------------------------
        # Сглобяване на суровия речник
        # ---------------------------------------------------------

        raw = {
            "book_page_url": book_page_url,
            "title": title,
            "author_name": author_name,
            "author_page_url": author_page_url,

            "cover_ebook_url": cover_ebook_url,
            "cover_ebook_alt": cover_ebook_alt,
            "cover_print_url": cover_print_url,
            "cover_print_alt": cover_print_alt,

            "pdf_url": pdf_url,
            "epub_url": epub_url,
            "pbook_url": pbook_url,
            "audio_url": audio_url,

            "show_author": True,
            "show_formats": True,
            "show_double_cover": True,
        }

        return raw
