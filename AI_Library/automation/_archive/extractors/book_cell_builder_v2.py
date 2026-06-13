# BookCellModel v2.0 – builder от сурови данни за книга

from system.models.book_cell.BookCellModel_v2_0 import (
    BookCellModel,
    BookCellCovers,
    BookCellFormats,
    BookCellDisplay,
)


def build_book_cell_from_raw(raw: dict) -> BookCellModel:
    """
    raw: суров речник с данни за книга (от e-books, p-izdatelstvo, registry и т.н.)
    Очаквани ключове (примерно):
      - "book_page_url"
      - "title"
      - "author_name"
      - "author_page_url"
      - "cover_ebook_url", "cover_ebook_alt"
      - "cover_print_url", "cover_print_alt"
      - "pdf_url", "epub_url", "pbook_url", "audio_url"
    """

    covers = BookCellCovers(
        ebook_url=raw.get("cover_ebook_url", ""),
        ebook_alt=raw.get("cover_ebook_alt", ""),
        print_url=raw.get("cover_print_url", ""),
        print_alt=raw.get("cover_print_alt", ""),
    )

    formats = BookCellFormats(
        pdf_url=raw.get("pdf_url", ""),
        epub_url=raw.get("epub_url", ""),
        pbook_url=raw.get("pbook_url", ""),
        audio_url=raw.get("audio_url", ""),
    )

    display = BookCellDisplay(
        show_author=raw.get("show_author", True),
        show_formats=raw.get("show_formats", True),
        show_double_cover=raw.get("show_double_cover", True),
    )

    model = BookCellModel(
        book_page_url=raw.get("book_page_url", ""),
        title=raw.get("title", ""),
        author_name=raw.get("author_name", ""),
        author_page_url=raw.get("author_page_url", ""),
        covers=covers,
        formats=formats,
        display=display,
    )

    return model
