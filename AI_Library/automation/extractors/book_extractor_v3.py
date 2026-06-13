# BookPageModel v3.0 – екстрактор за страница на книга

from dataclasses import asdict
from typing import Dict, Any, List

from system.models.book.BookPageModel_v3_0 import (
    BookPageModel,
    BookSEO,
    BookMetadata,
    BookCover,
    BookFormats,
    BookLinks,
    BookReview,
    BookNavigation,
    BookVisual,
)


def extract_book_page(raw_book: Dict[str, Any],
                      raw_reviews: List[Dict[str, Any]]) -> BookPageModel:
    """
    raw_book: сурови данни за книга (от e-books, p-izdatelstvo, registry и т.н.)
    raw_reviews: сурови рецензии
    """

    seo = BookSEO(
        title=raw_book.get("seo_title", ""),
        description=raw_book.get("seo_description", ""),
        canonical_url=raw_book.get("canonical_url", ""),
    )

    metadata = BookMetadata(
        title=raw_book.get("title", ""),
        author=raw_book.get("author", ""),
        genre=raw_book.get("genre", ""),
        year=raw_book.get("year", ""),
        pages=raw_book.get("pages", ""),
        binding_print=raw_book.get("binding_print", ""),
        format_print=raw_book.get("format_print", ""),
        isbn_print=raw_book.get("isbn_print", ""),
        isbn_pdf=raw_book.get("isbn_pdf", ""),
        isbn_epub=raw_book.get("isbn_epub", ""),
    )

    cover = BookCover(
        ebook_url=raw_book.get("cover_ebook_url", ""),
        ebook_alt=raw_book.get("cover_ebook_alt", ""),
        print_url=raw_book.get("cover_print_url", ""),
        print_alt=raw_book.get("cover_print_alt", ""),
    )

    formats = BookFormats(
        pdf_url=raw_book.get("pdf_url", ""),
        epub_url=raw_book.get("epub_url", ""),
        pbook_url=raw_book.get("pbook_url", ""),
        audio_url=raw_book.get("audio_url", ""),
    )

    links = BookLinks(
        author_page_url=raw_book.get("author_page_url", ""),
        tag_url=raw_book.get("tag_url", ""),
        registry_url=raw_book.get("registry_url", ""),
        goodreads_url=raw_book.get("goodreads_url", ""),
        bookstore_url=raw_book.get("bookstore_url", ""),
    )

    intro = raw_book.get("intro", "")
    description = raw_book.get("description", "")

    reviews_models = [
        BookReview(
            text=r.get("text", ""),
            source_url=r.get("source_url", ""),
            source_label=r.get("source_label", ""),
        )
        for r in raw_reviews
    ]

    navigation = BookNavigation(
        alphabetical=raw_book.get("navigation_alphabetical", True),
        genre=raw_book.get("navigation_genre", False),
    )

    visual = BookVisual(
        include_book_cell=raw_book.get("include_book_cell", True),
    )

    model = BookPageModel(
        seo=seo,
        metadata=metadata,
        cover=cover,
        formats=formats,
        links=links,
        intro=intro,
        description=description,
        reviews=reviews_models,
        navigation=navigation,
        visual=visual,
    )

    return model


def book_page_to_json_dict(model: BookPageModel) -> Dict[str, Any]:
    """
    Превръща BookPageModel в dict, готов за запис като JSON.
    """
    return asdict(model)
