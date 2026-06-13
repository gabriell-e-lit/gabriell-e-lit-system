# BooksAdapter v1.0
# Събира всички URL-и, свързани с една книга, и ги подрежда в raw_book структура

from typing import Dict, Any


class BooksAdapter:
    """
    Адаптер, който приема всички URL-и, свързани с една книга,
    и ги подрежда в единен raw_book речник.
    """

    def __init__(self):
        pass

    def build_raw_book(self,
                       title: str,
                       author_display: str,
                       slug: str,
                       canonical_page_url: str,
                       static_pdf_url: str = "",
                       ebooks_pdf_url: str = "",
                       ebooks_epub_url: str = "",
                       book_tag_url: str = "") -> Dict[str, Any]:
        """
        Връща raw_book речник, който екстракторът ще превърне в BookPageModel.
        """

        raw_book = {
            "title": title,
            "slug": slug,
            "author_display": author_display,

            # Основни URL-и
            "canonical_page_url": canonical_page_url,
            "static_pdf_url": static_pdf_url,
            "ebooks_pdf_url": ebooks_pdf_url,
            "ebooks_epub_url": ebooks_epub_url,
            "book_tag_url": book_tag_url,

            # SEO
            "seo_title": f"{title} – {author_display}",
            "seo_description": f"Книга от {author_display}: {title}",
            "canonical_url": canonical_page_url
        }

        return raw_book
