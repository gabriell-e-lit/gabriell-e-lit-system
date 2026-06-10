# AuthorExtractor_v4.py
# Финална версия – интегрира canon + issue (+ gallery през интегратора)
# и връща AuthorModel_v4.2

from urllib.parse import urlparse

from .author_extractor_canon_v3 import CanonExtractorV3
from .author_extractor_issue_v3 import IssueExtractorV3
from .gallery_extractor_v3 import GalleryExtractorV3
from .integrator import integrate_author_data


# По желание: константи за директориите на галерията (използват се от генератора, не задължително тук)
GALLERY_STATIC_PATHS = {
    "gallery_illustrator": "https://e-gallery.gabriell-e-lit.com/authors/gabriell-e-lit/",
    "gallery_e_gallery": "https://e-gallery.gabriell-e-lit.com/authors/e-gallery/",
    "gallery_magazine": "https://e-gallery.gabriell-e-lit.com/authors/kartini-s-dumi-i-bagri/"
}


class AuthorExtractorV4:
    """
    Unified Author Extractor v4.0

    - mode="canon": извлича един автор от канон страница
    - mode="issue": извлича списък автори от страница „Автори в брой X“
      (тук връщаме директно v3-обектите, защото са много автори)
    - галерийните данни влизат през интегратора като gallery_data
    """

    def __init__(self, html: str, mode: str, url: str = "", gallery_html: str = None, library_data=None):
        """
        html        – HTML на текущата страница (канон или брой)
        mode        – "canon" или "issue"
        url         – URL на страницата (по избор)
        gallery_html – HTML на галерийната страница (ако искаш да интегрираш художници)
        library_data – по-късно: данни от библиотечен екстрактор
        """
        self.html = html
        self.mode = mode
        self.url = url
        self.gallery_html = gallery_html
        self.library_data = library_data

    # ----------------- helpers -----------------
    def generate_page_filename(self, slug: str) -> str:
        """
        slug → име на статичен файл.
        Пример: zad-garba-gabriela-zaneva → zadgarbagabrielazaneva.php
        """
        return slug.replace("-", "") + ".php"

    def detect_static_page_flags(self, canon_data, gallery_data=None, library_data=None):
        """
        Определя:
        - дали авторът има статична страница
        - в коя категория попада
        На база:
        - роля от канона
        - галерийни данни
        - библиотечни данни (по-късно)
        """

        # 1) Канон – издателство / гост-редактор
        role = (canon_data or {}).get("role", "").lower()

        if "издателство" in role or "publisher" in role:
            return True, "publisher"

        if "гост" in role or "guest" in role:
            return True, "guest_editor"

        # 2) Библиотека – ако има отделен static_page_url (по-късно)
        if library_data and library_data.get("static_page_url"):
            return True, "library"

        # 3) Галерия – ако има gallery_subcategory
        if gallery_data and gallery_data.get("links", {}).get("gallery_subcategory"):
            sub = gallery_data["links"]["gallery_subcategory"]
            if sub == "gallery_e_gallery":
                return True, "gallery_e_gallery"
            if sub == "gallery_magazine":
                return True, "gallery_magazine"
            if sub == "gallery_illustrator":
                return True, "gallery_illustrator"

        # 4) В противен случай – няма статична страница
        return False, ""

    # ----------------- main -----------------
    def run(self):
        """
        Главен pipeline.
        В режим "canon" → връща един AuthorModel_v4.2 обект.
        В режим "issue" → връща списък от v3-обекти (един брой → много автори).
        """

        # ---------- режим: issue ----------
        if self.mode == "issue":
            issue_extractor = IssueExtractorV3(self.html)
            issue_list_v3 = issue_extractor.extract()
            # Тук нарочно връщаме v3-обектите, защото са много автори
            # и трансформацията към v4.2 може да се прави по-късно, по един.
            return issue_list_v3

        # ---------- режим: canon ----------
        if self.mode != "canon":
            raise ValueError("Unsupported mode for AuthorExtractorV4 (use 'canon' or 'issue').")

        # 1) CanonExtractorV3 – извличаме канон данни за един автор
        canon_extractor = CanonExtractorV3(self.html)
        canon_data = canon_extractor.extract()

        # 2) GalleryExtractorV3 – ако имаме gallery_html, можем да подадем gallery_data за интеграция
        gallery_data = None
        if self.gallery_html:
            gallery_extractor = GalleryExtractorV3(self.gallery_html)
            gallery_list = gallery_extractor.extract()
            # Тук трябва да намерим съответния художник по slug или име, ако е художник.
            # За момента оставяме gallery_data=None, освен ако не се подаде отвън
            # конкретен обект. Това може да се разшири по-късно.
            # gallery_data = ...

        # 3) Интегратор – обединява canon + issue + library + gallery → AuthorModel_v3
        author_v3 = integrate_author_data(
            canon_data=canon_data,
            issue_data=None,
            library_data=self.library_data,
            gallery_data=gallery_data
        )

        # 4) Определяме статична страница (да/не) и категория
        static_required, static_category = self.detect_static_page_flags(
            canon_data=canon_data,
            gallery_data=gallery_data,
            library_data=self.library_data
        )

        # 5) Трансформация към AuthorModel_v4.2
        slug = author_v3["identity"]["slug"]
        name = author_v3["identity"]["name_display"]

        author_v4 = {
            "name": name,
            "slug": slug,
            "page_filename": self.generate_page_filename(slug) if static_required else "",
            "static_page_required": static_required,
            "static_page_category": static_category,

            "biography": author_v3["biography"]["short"],
            "photo": author_v3["photo"]["url"],
            "photo_alt": author_v3["photo"]["alt"],

            "origin": author_v3.get("origin", {
                "country": "",
                "city": "",
                "year_of_birth": "",
                "year_of_death": "",
                "notes": ""
            }),

            "sources": {
                "tag_page": author_v3["links"]["tag_url"],
                "wikipedia": "",  # може да дойде от канона, ако го добавите там
                "static_page": author_v3["links"]["library_url"]  # или друг източник
            },

            "books_publisher": author_v3.get("books", []),
            "books_library": [],  # по-късно – ако имате отделен library екстрактор

            "publications": author_v3.get("publications", []),

            "gallery": {
                "subcategory": author_v3["links"]["gallery_subcategory"],
                "url": author_v3["links"]["gallery_url"]
            },

            "roles": [canon_data.get("role", "")] if canon_data.get("role") else [],

            "publication_display_mode": "list"
        }

        return author_v4
