# AuthorPageModel v4.3
# Пълен модел за авторска страница

from dataclasses import dataclass, field
from typing import List
from system.models.book_cell.BookCellModel_v2_0 import BookCellModel


@dataclass
class AuthorSEO:
    title: str = ""
    description: str = ""
    canonical_url: str = ""


@dataclass
class AuthorIdentity:
    author_id: str = ""
    slug: str = ""
    name_original: str = ""
    name_display: str = ""


@dataclass
class AuthorBiography:
    short: str = ""
    long: str = ""
    quote: str = ""


@dataclass
class AuthorPhoto:
    url: str = ""
    alt: str = ""


@dataclass
class AuthorOrigin:
    country: str = ""
    city: str = ""
    birth_year: str = ""
    death_year: str = ""


@dataclass
class AuthorLinks:
    tag_url: str = ""
    gallery_subcategory: str = ""
    gallery_url: str = ""
    library_url: str = ""


@dataclass
class AuthorStructure:
    structural_pages_h2: List[str] = field(default_factory=list)
    structural_pages_h3: List[str] = field(default_factory=list)
    first_appearance: str = ""


@dataclass
class AuthorNavigation:
    alphabetical: bool = True


@dataclass
class AuthorVisual:
    show_quote: bool = True
    show_origin: bool = True
    show_gallery: bool = True
    show_publications: bool = True


@dataclass
class AuthorPageModel:
    seo: AuthorSEO = field(default_factory=AuthorSEO)
    identity: AuthorIdentity = field(default_factory=AuthorIdentity)
    biography: AuthorBiography = field(default_factory=AuthorBiography)
    photo: AuthorPhoto = field(default_factory=AuthorPhoto)
    origin: AuthorOrigin = field(default_factory=AuthorOrigin)
    links: AuthorLinks = field(default_factory=AuthorLinks)
    structure: AuthorStructure = field(default_factory=AuthorStructure)

    books: List[BookCellModel] = field(default_factory=list)
    publications: List[dict] = field(default_factory=list)
    magazine_issues: List[dict] = field(default_factory=list)
    exhibitions: List[dict] = field(default_factory=list)
    collections: List[dict] = field(default_factory=list)

    navigation: AuthorNavigation = field(default_factory=AuthorNavigation)
    visual: AuthorVisual = field(default_factory=AuthorVisual)
