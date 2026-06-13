# BookExtractor v1.0
# Превръща raw_book → BookPageModel

from typing import Dict, Any, List


class BookExtractorV1:
    """
    Превръща raw_book речник (от BooksAdapter)
    в BookPageModel структура, която генераторът може да рендерира.
    """

    def __init__(self, tag_adapter=None):
        """
        tag_adapter: WordPressTagAdapter (по избор)
        """
        self.tag_adapter = tag_adapter

    # -----------------------------
    # UTILS
    # -----------------------------

    def safe(self, value: Any, default=""):
        return value if value else default

    # -----------------------------
    # MAIN EXTRACTION
    # -----------------------------

    def extract(self, raw_book: Dict[str, Any]) -> Dict[str, Any]:
        """
        Връща BookPageModel (като dict).
        """

        title = self.safe(raw_book.get("title"))
        slug = self.safe(raw_book.get("slug"))
        author_display = self.safe(raw_book.get("author_display"))

        canonical_page_url = self.safe(raw_book.get("canonical_page_url"))
        static_pdf_url = self.safe(raw_book.get("static_pdf_url"))
        ebooks_pdf_url = self.safe(raw_book.get("ebooks_pdf_url"))
        ebooks_epub_url = self.safe(raw_book.get("ebooks_epub_url"))
        book_tag_url = self.safe(raw_book.get("book_tag_url"))

        # Публикации от WordPress таг
        publications: List[Dict[str, Any]] = []
        if self.tag_adapter and book_tag_url:
            try:
                publications = self.tag_adapter.extract_publications(book_tag_url)
            except Exception:
                publications = []

        # Сглобяване на BookPageModel
        model = {
            "identity": {
                "title": title,
                "slug": slug,
                "author_display": author_display
            },

            "urls": {
                "canonical_page": canonical_page_url,
                "static_pdf": static_pdf_url,
                "ebooks_pdf": ebooks_pdf_url,
                "ebooks_epub": ebooks_epub_url,
                "book_tag": book_tag_url
            },

            "files": {
                "pdf_static": static_pdf_url,
                "pdf_ebooks": ebooks_pdf_url,
                "epub_ebooks": ebooks_epub_url
            },

            "publications": publications,

            "seo": {
                "title": raw_book.get("seo_title", f"{title} – {author_display}"),
                "description": raw_book.get("seo_description", title),
                "canonical_url": raw_book.get("canonical_url", canonical_page_url)
            }
        }

        return model
