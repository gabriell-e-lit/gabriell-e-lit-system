# CanonicalAuthorsAdapter v2.0
# Пълна поддръжка на реалната структура на четирите канонични страници

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List


class CanonicalAuthorsAdapter:

    def __init__(self):
        self.pages = {
            "publisher": "https://gabriell-e-lit.com/izdatelstvo/gabriell-e-lit/authors-gabriell-e-lit/",
            "library":   "https://gabriell-e-lit.com/izdatelstvo/authors-e-library-gabriell-e-lit/",
            "gallery":   "https://gabriell-e-lit.com/izdatelstvo/artists-e-gallery-gabriell-e-lit/",
            "guest":     "https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/ekip-spisanie/gost-redaktori/"
        }

    # ---------------------------------------------------------
    # UTILS
    # ---------------------------------------------------------

    def fetch_html(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def extract_text(self, el):
        return el.get_text(strip=True) if el else ""

    def extract_slug(self, href: str, name_display: str) -> str:
        if not href:
            return name_display.lower().replace(" ", "-")
        if "/tag/" in href or "/authors/" in href:
            return href.rstrip("/").split("/")[-1]
        return name_display.lower().replace(" ", "-")

    # ---------------------------------------------------------
    # PUBLISHER PAGE
    # ---------------------------------------------------------

    def extract_publisher_authors(self, url: str) -> Dict[str, Any]:
        soup = self.fetch_html(url)
        result = {}

        h2_list = soup.find_all("h2")

        for h2 in h2_list:
            year = self.extract_text(h2)
            if not year.isdigit():
                continue

            # Под H2 → H3 автори
            sibling = h2.find_next_sibling()
            while sibling and sibling.name != "h2":
                if sibling.name == "h3":
                    name_display = self.extract_text(sibling)
                    a = sibling.find("a")
                    href = a["href"] if a else ""
                    slug = self.extract_slug(href, name_display)

                    result[slug] = {
                        "name_display": name_display,
                        "role": "publisher",
                        "publisher_first_year": year,
                        "has_static_page": True,
                        "tag_url": href if "/tag/" in href else ""
                    }
                sibling = sibling.find_next_sibling()

        return result

    # ---------------------------------------------------------
    # LIBRARY PAGE
    # ---------------------------------------------------------

    def extract_library_authors(self, url: str) -> Dict[str, Any]:
        soup = self.fetch_html(url)
        result = {}

        h2_list = soup.find_all("h2")

        for h2 in h2_list:
            title = self.extract_text(h2).lower()

            if "електронни книги" in title or "e-library" in title:
                subcat = "ebooks-platform"
            else:
                subcat = "free-library"

            sibling = h2.find_next_sibling()
            while sibling and sibling.name != "h2":
                if sibling.name == "h3":
                    name_display = self.extract_text(sibling)
                    a = sibling.find("a")
                    href = a["href"] if a else ""
                    slug = self.extract_slug(href, name_display)

                    result[slug] = {
                        "name_display": name_display,
                        "role": "library",
                        "library_subcategory": subcat,
                        "has_static_page": True,
                        "tag_url": href if "/tag/" in href else ""
                    }
                sibling = sibling.find_next_sibling()

        return result

    # ---------------------------------------------------------
    # GALLERY PAGE
    # ---------------------------------------------------------

    def extract_gallery_authors(self, url: str) -> Dict[str, Any]:
        soup = self.fetch_html(url)
        result = {}

        h2_list = soup.find_all("h2")

        for h2 in h2_list:
            title = self.extract_text(h2).lower()

            if "илюстратор" in title:
                subcat = "illustrator"
            elif "изложб" in title:
                subcat = "exhibition"
            elif "списани" in title:
                subcat = "magazine-artist"
            else:
                subcat = "unknown"

            sibling = h2.find_next_sibling()
            while sibling and sibling.name != "h2":
                if sibling.name == "h3":
                    name_display = self.extract_text(sibling)
                    a = sibling.find("a")
                    href = a["href"] if a else ""
                    slug = self.extract_slug(href, name_display)

                    result[slug] = {
                        "name_display": name_display,
                        "role": "gallery",
                        "gallery_subcategory": subcat,
                        "has_static_page": True,
                        "tag_url": href if "/tag/" in href else ""
                    }
                sibling = sibling.find_next_sibling()

        return result

    # ---------------------------------------------------------
    # GUEST EDITORS PAGE
    # ---------------------------------------------------------

    def extract_guest_editors(self, url: str) -> Dict[str, Any]:
        soup = self.fetch_html(url)
        result = {}

        h2_list = soup.find_all("h2")

        for h2 in h2_list:
            issue = self.extract_text(h2)

            sibling = h2.find_next_sibling()
            while sibling and sibling.name != "h2":
                if sibling.name == "h3":
                    name_display = self.extract_text(sibling)
                    a = sibling.find("a")
                    href = a["href"] if a else ""
                    slug = self.extract_slug(href, name_display)

                    result[slug] = {
                        "name_display": name_display,
                        "role": "guest",
                        "guest_editor_issue": issue,
                        "has_static_page": True,
                        "tag_url": href if "/tag/" in href else ""
                    }
                sibling = sibling.find_next_sibling()

        return result

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def extract_all_canonical_authors(self) -> Dict[str, Any]:
        result = {}

        result.update(self.extract_publisher_authors(self.pages["publisher"]))
        result.update(self.extract_library_authors(self.pages["library"]))
        result.update(self.extract_gallery_authors(self.pages["gallery"]))
        result.update(self.extract_guest_editors(self.pages["guest"]))

        return result
