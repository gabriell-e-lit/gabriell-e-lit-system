# AuthorPageModel v4.3 – екстрактор за авторска страница

from dataclasses import asdict
from typing import Dict, Any, List

from system.models.author.AuthorPageModel_v4_3 import (
    AuthorPageModel,
    AuthorSEO,
    AuthorIdentity,
    AuthorBiography,
    AuthorPhoto,
    AuthorOrigin,
    AuthorLinks,
    AuthorStructure,
    AuthorNavigation,
    AuthorVisual,
)
from automation.extractors.book_cell_builder_v2 import build_book_cell_from_raw


def extract_author_page(raw_author: Dict[str, Any],
                        raw_books: List[Dict[str, Any]],
                        raw_publications: List[Dict[str, Any]],
                        raw_magazine_issues: List[Dict[str, Any]],
                        raw_exhibitions: List[Dict[str, Any]],
                        raw_collections: List[Dict[str, Any]]) -> AuthorPageModel:
    """
    raw_author: сурови данни за автора (от WordPress, JSON, CSV и т.н.)
    raw_books: сурови данни за книги на автора
    останалите: сурови списъци за публикации, броеве, изложби, колекции
    """

    seo = AuthorSEO(
        title=raw_author.get("seo_title", ""),
        description=raw_author.get("seo_description", ""),
        canonical_url=raw_author.get("canonical_url", ""),
    )

    identity = AuthorIdentity(
        author_id=raw_author.get("author_id", ""),
        slug=raw_author.get("author_slug", ""),
        name_original=raw_author.get("name_original", ""),
        name_display=raw_author.get("name_display", ""),
    )

    biography = AuthorBiography(
        short=raw_author.get("bio_short", ""),
        long=raw_author.get("bio_long", ""),
        quote=raw_author.get("quote", ""),
    )

    photo = AuthorPhoto(
        url=raw_author.get("photo_url", ""),
        alt=raw_author.get("photo_alt", ""),
    )

    origin = AuthorOrigin(
        country=raw_author.get("country", ""),
        city=raw_author.get("city", ""),
        birth_year=raw_author.get("birth_year", ""),
        death_year=raw_author.get("death_year", ""),
    )

    links = AuthorLinks(
        tag_url=raw_author.get("tag_url", ""),
        gallery_subcategory=raw_author.get("gallery_subcategory", ""),
        gallery_url=raw_author.get("gallery_url", ""),
        library_url=raw_author.get("library_url", ""),
    )

    structure = AuthorStructure(
        structural_pages_h2=raw_author.get("structural_pages_h2", []) or [],
        structural_pages_h3=raw_author.get("structural_pages_h3", []) or [],
        first_appearance=raw_author.get("first_appearance", ""),
    )

    navigation = AuthorNavigation(
        alphabetical=raw_author.get("navigation_alphabetical", True),
    )

    visual = AuthorVisual(
        show_quote=raw_author.get("show_quote", True),
        show_origin=raw_author.get("show_origin", True),
        show_gallery=raw_author.get("show_gallery", True),
        show_publications=raw_author.get("show_publications", True),
    )

    # книги → BookCellModel
    books_models = [build_book_cell_from_raw(b) for b in raw_books]

    model = AuthorPageModel(
        seo=seo,
        identity=identity,
        biography=biography,
        photo=photo,
        origin=origin,
        links=links,
        structure=structure,
        books=books_models,
        publications=raw_publications or [],
        magazine_issues=raw_magazine_issues or [],
        exhibitions=raw_exhibitions or [],
        collections=raw_collections or [],
        navigation=navigation,
        visual=visual,
    )

    return model


def author_page_to_json_dict(model: AuthorPageModel) -> Dict[str, Any]:
    """
    Превръща AuthorPageModel в dict, готов за запис като JSON.
    """
    return asdict(model)
