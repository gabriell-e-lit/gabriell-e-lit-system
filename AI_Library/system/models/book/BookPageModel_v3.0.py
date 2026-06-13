from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------
# SEO
# ---------------------------------------------------------
@dataclass
class BookSEO:
    title: str = ""
    description: str = ""
    canonical_url: str = ""


# ---------------------------------------------------------
# Metadata (официални данни от регистъра)
# ---------------------------------------------------------
@dataclass
class BookMetadata:
    title: str = ""
    author: str = ""
    genre: str = ""
    year: str = ""
    pages: str = ""
    binding_print: str = ""
    format_print: str = ""
    isbn_print: str = ""
    isbn_pdf: str = ""
    isbn_epub: str = ""


# ---------------------------------------------------------
# Covers
# ---------------------------------------------------------
@dataclass
class BookCover:
    ebook_url: str = ""
    ebook_alt: str = ""
    print_url: str = ""
    print_alt: str = ""


# ---------------------------------------------------------
# Formats (PDF, EPUB, Print, Audio)
# ---------------------------------------------------------
@dataclass
class BookFormats:
    pdf_url: str = ""
    epub_url: str = ""
    pbook_url: str = ""
    audio_url: str = ""


# ---------------------------------------------------------
# Links (author page, tag, registry, goodreads, bookstore)
# ---------------------------------------------------------
@dataclass
class BookLinks:
    author_page_url: str = ""
    tag_url: str = ""
    registry_url: str = ""
    goodreads_url: str = ""
    bookstore_url: str = ""


# ---------------------------------------------------------
# Reviews
# ---------------------------------------------------------
@dataclass
class BookReview:
    text: str = ""
    source_url: str = ""
    source_label: str = ""


# ---------------------------------------------------------
# Navigation flags
# ---------------------------------------------------------
@dataclass
class BookNavigation:
    alphabetical: bool = True
    genre: bool = False


# ---------------------------------------------------------
# Visual flags
# ---------------------------------------------------------
@dataclass
class BookVisual:
    include_book_cell: bool = True


# ---------------------------------------------------------
# FINAL MODEL: BookPageModel_v3.0
# ---------------------------------------------------------
@dataclass
class BookPageModel:
    seo: BookSEO = field(default_factory=BookSEO)
    metadata: BookMetadata = field(default_factory=BookMetadata)
    cover: BookCover = field(default_factory=BookCover)
    formats: BookFormats = field(default_factory=BookFormats)
    links: BookLinks = field(default_factory=BookLinks)

    intro: str = ""          # HTML intro extracted from tag
    description: str = ""    # Full description (future extension)

    reviews: List[BookReview] = field(default_factory=list)

    navigation: BookNavigation = field(default_factory=BookNavigation)
    visual: BookVisual = field(default_factory=BookVisual)
