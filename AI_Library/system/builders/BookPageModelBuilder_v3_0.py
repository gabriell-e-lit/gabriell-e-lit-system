from dataclasses import asdict

from system.models.BookPageModel_v3_0 import (
    BookSEO,
    BookMetadata,
    BookCover,
    BookFormats,
    BookLinks,
    BookReview,
    BookNavigation,
    BookVisual
)

from system.extractors.book.BookTagIntroExtractor_v1_0 import BookTagIntroExtractorV1_0
from system.extractors.book.BookMetadataExtractor_v2_0_registry import BookMetadataExtractorV2_0_Registry


class BookPageModelBuilderV3_0:
    """
    Combines:
    - BookCellModel_v2.0
    - Intro from tag description
    - Metadata from National Registry
    - (future) Reviews
    into a complete BookPageModel_v3.0
    """

    def __init__(self, wp_base_url: str, wp_user: str = "", wp_pass: str = ""):
        self.intro_extractor = BookTagIntroExtractorV1_0(wp_base_url, wp_user, wp_pass)
        self.metadata_extractor = BookMetadataExtractorV2_0_Registry()

    def build(self, book_cell_model, static_page_html: str, tag_id: int):
        """
        Main builder method.
        :param book_cell_model: BookCellModel_v2.0 instance
        :param static_page_html: HTML of the static book page
        :param tag_id: WordPress tag ID for the book
        """

        # -----------------------------------------
        # 1) Extract intro from tag
        # -----------------------------------------
        intro_html = self.intro_extractor.extract_intro(tag_id)

        # -----------------------------------------
        # 2) Extract metadata from registry
        # -----------------------------------------
        registry_metadata = self.metadata_extractor.extract(static_page_html)

        # -----------------------------------------
        # 3) Build BookMetadata section
        # -----------------------------------------
        metadata = BookMetadata(
            title=registry_metadata.get("title", book_cell_model.title),
            author=registry_metadata.get("author", book_cell_model.author),
            genre=book_cell_model.genre,
            year=registry_metadata.get("year", ""),
            pages=registry_metadata.get("pages", ""),
            binding_print=registry_metadata.get("binding", ""),
            format_print=registry_metadata.get("format", ""),
            isbn_print=registry_metadata.get("isbn_print", ""),
            isbn_pdf=registry_metadata.get("isbn_pdf", ""),
            isbn_epub=registry_metadata.get("isbn_epub", "")
        )

        # -----------------------------------------
        # 4) Build SEO section
        # -----------------------------------------
        seo = BookSEO(
            title=metadata.title,
            description=intro_html,
            canonical_url=book_cell_model.static_page_url
        )

        # -----------------------------------------
        # 5) Build Covers
        # -----------------------------------------
        covers = BookCover(
            ebook_url=book_cell_model.cover_ebook_url,
            ebook_alt=book_cell_model.cover_ebook_alt,
            print_url=book_cell_model.cover_print_url,
            print_alt=book_cell_model.cover_print_alt
        )

        # -----------------------------------------
        # 6) Build Formats
        # -----------------------------------------
        formats = BookFormats(
            pdf_url=book_cell_model.pdf_url,
            epub_url=book_cell_model.epub_url,
            pbook_url=book_cell_model.pbook_url,
            audio_url=book_cell_model.audio_url
        )

        # -----------------------------------------
        # 7) Build Links
        # -----------------------------------------
        links = BookLinks(
            author_page_url=book_cell_model.author_page_url,
            tag_url=book_cell_model.tag_url,
            registry_url=registry_metadata.get("registry_url", ""),
            goodreads_url="",
            bookstore_url=""
        )

        # -----------------------------------------
        # 8) Navigation + Visual
        # -----------------------------------------
        navigation = BookNavigation()
        visual = BookVisual()

        # -----------------------------------------
        # 9) Final model dictionary
        # -----------------------------------------
        return {
            "seo": asdict(seo),
            "metadata": asdict(metadata),
            "covers": asdict(covers),
            "formats": asdict(formats),
            "links": asdict(links),
            "navigation": asdict(navigation),
            "visual": asdict(visual),
            "intro_html": intro_html
        }
