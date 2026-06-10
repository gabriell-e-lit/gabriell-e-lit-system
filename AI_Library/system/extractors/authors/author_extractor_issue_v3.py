from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class IssueExtractorV3:
    """
    Extracts author data from 'Автори в брой X' pages.
    Produces partial AuthorModel_v3 objects.
    """

    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def slugify(self, name: str) -> str:
        name = name.lower()
        name = re.sub(r"[^a-zа-яё0-9\s-]", "", name)
        name = name.replace(" ", "-")
        return name

    def extract_issue_number(self):
        """
        Extracts issue number from page title or H1.
        Example: 'Автори в брой 31' → 31
        """
        h1 = self.soup.find("h1")
        if not h1:
            return ""

        text = h1.get_text(strip=True)
        match = re.search(r"брой\s+(\d+)", text, re.IGNORECASE)
        return match.group(1) if match else ""

    # ---------------------------------------------------------
    # MAIN EXTRACTION
    # ---------------------------------------------------------
    def extract(self):
        authors = []
        issue_number = self.extract_issue_number()

        # All authors are listed as H2
        h2_blocks = self.soup.find_all("h2")

        for h2 in h2_blocks:
            name_display = h2.get_text(strip=True)

            # Check if H2 contains a link to tag page
            tag_url = ""
            a = h2.find("a", href=True)
            if a and "/tag/" in a["href"]:
                tag_url = a["href"]
                slug = urlparse(tag_url).path.rstrip("/").split("/")[-1]
            else:
                slug = self.slugify(name_display)

            # Find media+text block (first appearance)
            block = h2.find_next("div", class_=lambda c: c and "media-text" in c or "author-block" in c)

            photo_url = ""
            photo_alt = ""
            biography_short = ""
            publications = []

            if block:
                # Photo
                img = block.find("img")
                if img:
                    photo_url = img.get("src", "").strip()
                    photo_alt = img.get("alt", "").strip()

                # Biography (first <p>)
                p = block.find("p")
                if p:
                    biography_short = p.get_text(strip=True)

                # Publications
                for link in block.find_all("a", href=True):
                    href = link["href"]
                    if "/izdatelstvo/" in href or "/spisanie/" in href:
                        publications.append({
                            "title": link.get_text(strip=True),
                            "url": href
                        })

            # Build partial AuthorModel_v3 object
            author_obj = {
                "identity": {
                    "author_id": f"author_{slug.replace('-', '_')}",
                    "slug": slug,
                    "name_original": name_display,
                    "name_display": name_display
                },

                "biography": {
                    "short": biography_short,
                    "long": "",
                    "quote": ""
                },

                "photo": {
                    "url": photo_url,
                    "alt": photo_alt
                },

                "links": {
                    "tag_url": tag_url,
                    "library_url": "",
                    "gallery_url": "",
                    "gallery_subcategory": ""
                },

                "structure": {
                    "first_appearance": issue_number,
                    "structural_pages_h2": [],
                    "structural_pages_h3": []
                },

                "publications": publications,
                "magazine_issues": [issue_number] if issue_number else [],
                "books": [],
                "exhibitions": [],
                "collections": [],

                "navigation": {
                    "alphabetical": True
                },

                "visual": {
                    "show_quote": False,
                    "show_origin": False,
                    "show_gallery": False,
                    "show_publications": True
                },

                "source": "issue_page"
            }

            authors.append(author_obj)

        return authors
