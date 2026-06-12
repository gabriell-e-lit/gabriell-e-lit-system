# BookCellModel v2.0
# Модел за визуална клетка на книга (UI компонент)

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BookCellCovers:
    ebook_url: str = ""
    ebook_alt: str = ""
    print_url: str = ""
    print_alt: str = ""


@dataclass
class BookCellFormats:
    pdf_url: str = ""
    epub_url: str = ""
    pbook_url: str = ""
    audio_url: str = ""


@dataclass
class BookCellDisplay:
    show_author: bool = True
    show_formats: bool = True
    show_double_cover: bool = True


@dataclass
class BookCellModel:
    book_page_url: str = ""
    title: str = ""
    author_name: str = ""
    author_page_url: str = ""

    covers: BookCellCovers = field(default_factory=BookCellCovers)
    formats: BookCellFormats = field(default_factory=BookCellFormats)
    display: BookCellDisplay = field(default_factory=BookCellDisplay)
