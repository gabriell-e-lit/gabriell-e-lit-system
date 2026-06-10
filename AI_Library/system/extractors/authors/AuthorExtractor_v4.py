import re
from urllib.parse import urlparse

from .author_extractor_canon_v3 import CanonExtractorV3
from .author_extractor_issue_v3 import IssueExtractorV3
from .integrator import integrate_author_data


class AuthorExtractorV4:
    """
    Unified Author Extractor v4.0
    - Uses CanonExtractorV3 + IssueExtractorV3
    - Integrates data
    - Transforms to AuthorModel_v4.2
    """

    # ---------------------------------------------------------
    # INITIALIZATION
    # ---------------------------------------------------------
    def __init__(self, html: str, mode: str, url: str = ""):
        self.html = html
        self.mode = mode
        self.url = url

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def generate_page_filename(self, slug: str) -> str:
        """
        Converts slug → static page filename.
        Example: zad-garba-gabriela-zaneva → zadgarbagabrielazaneva.php
        """
        return slug.replace("-", "") + ".php"

    def detect_static_page_category(self, canon_data, gallery_data=None, library_data=None):
        """
        Determines whether the author should have a static page
        and which category it belongs to.
        """

        # 1) Canon role determines static page category
        role = canon_data.get("role", "").lower()

        if "издателство" in role or "publisher" in role:
            return True, "publisher"

        if "гост" in role or "guest" in role:
            return True, "guest_editor"

        # 2) Library data
        if library_data and library_data.get("static_page_url"):
            return True, "library"

        # 3) Gallery data
        if gallery_data and gallery_data.get("gallery_subcategory"):
            sub = gallery_data["gallery_subcategory"]
            if sub == "e-gallery":
                return True, "gallery_e_gallery"
            if sub == "kartini-s-dumi-i-bagri":
                return True, "gallery_magazine"
            if sub == "gabriell-e-lit":
                return True, "gallery_illustrator"

        # 4) Otherwise → no static page
        return False, ""

    # ---------------------------------------------------------
    # MAIN PIPELINE
    # ---------------------------------------------------------
    def run(self):
        """
        Main extraction pipeline.
        Returns AuthorModel_v4.2 object.
        """

        # -----------------------------------------------------
        # 1. Extract using v3 extractors
        # -----------------------------------------------------
        if self.mode == "canon":
            canon_extractor = CanonExtractorV3(self.html)
            canon_data = canon_extractor.extract()
            issue_data = None

        elif self.mode == "issue":
            issue_extractor = IssueExtractorV3(self.html)
            issue_list = issue_extractor.extract()

            # Issue pages return a LIST of authors
            # AuthorExtractor_v4 processes ONE author at a time
            # → caller must loop externally
            return issue_list

        else:
            raise ValueError("Unsupported mode for AuthorExtractorV4")

        # -----------------------------------------------------
        # 2. Integrate data (canon + issue + library + gallery)
        # -----------------------------------------------------
        author_v3 = integrate_author_data(
            canon_data=canon_data,
            issue_data=None,
            library_data=None,
            gallery_data=None
        )

        # -----------------------------------------------------
        # 3. Determine static page category
        # -----------------------------------------------------
        static_required, static_category = self.detect_static_page_category(
            canon_data=canon_data,
            gallery_data=None,
            library_data=None
        )

        # -----------------------------------------------------
        # 4. Transform to AuthorModel_v4.2
        # -----------------------------------------------------
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

            "origin": author_v3["origin"],

            "sources": {
                "tag_page": author_v3["links"]["tag_url"],
                "wikipedia": "",
                "static_page": author_v3["links"]["library_url"]
            },

            "books_publisher": author_v3["books"],
            "books_library": [],

            "publications": author_v3["publications"],

            "gallery": {
                "subcategory": author_v3["links"]["gallery_subcategory"],
                "url": author_v3["links"]["gallery_url"]
            },

            "roles": [canon_data.get("role", "")],

            "publication_display_mode": "list"
        }

        return author_v4
