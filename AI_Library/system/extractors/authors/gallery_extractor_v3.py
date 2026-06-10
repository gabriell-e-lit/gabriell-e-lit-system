from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class GalleryExtractorV3:
    """
    Extracts artist data from the dynamic gallery page:
    https://gabriell-e-lit.com/izdatelstvo/artists-e-gallery-gabriell-e-lit/

    Produces partial AuthorModel_v3 objects.
    """

    CATEGORY_MAP = {
        "ХУДОЖНИЦИ В е-ГАЛЕРИЯ gabriell-e-lit": "gallery_e_gallery",
        "ХУДОЖНИЦИ В ИЗДАТЕЛСТВО gabriell-e-lit": "gallery_illustrator",
        "ХУДОЖНИЦИ, ПРЕДСТАВЕНИ В СП. “КАРТИНИ С ДУМИ И БАГРИ”": "gallery_magazine"
    }

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

    # ---------------------------------------------------------
    # MAIN EXTRACTION
    # ---------------------------------------------------------
    def extract(self):
        artists = []

        # Find all H2 blocks that match the known categories
        h2_blocks = self.soup.find_all("h2")

        for h2 in h2_blocks:
            h2_text = h2.get_text(strip=True)

            # Determine category
            category = None
            for title, cat in self.CATEGORY_MAP.items():
                if title in h2_text:
                    category = cat
                    break

            if not category:
                continue  # skip unrelated H2

            # All H3 under this H2 are artists in this category
            h3_blocks = []
            next_node = h2.find_next_sibling()

            while next_node:
                if next_node.name == "h2":
                    break  # next category reached
                if next_node.name == "h3":
                    h3_blocks.append(next_node)
                next_node = next_node.find_next_sibling()

            # Process each artist
            for h3 in h3_blocks:
                name_display = h3.get_text(strip=True)

                # Try to get slug from link
                tag_url = ""
                a = h3.find("a", href=True)
                if a and "/tag/" in a["href"]:
                    tag_url = a["href"]
                    slug = urlparse(tag_url).path.rstrip("/").split("/")[-1]
                else:
                    slug = self.slugify(name_display)

                # Build partial AuthorModel_v3 object
                artist_obj = {
                    "identity": {
                        "author_id": f"author_{slug.replace('-', '_')}",
                        "slug": slug,
                        "name_original": name_display,
                        "name_display": name_display
                    },

                    "biography": {
                        "short": "",
                        "long": "",
                        "quote": ""
                    },

                    "photo": {
                        "url": "",
                        "alt": ""
                    },

                    "links": {
                        "tag_url": tag_url,
                        "library_url": "",
                        "gallery_url": "",
                        "gallery_subcategory": category
                    },

                    "structure": {
                        "first_appearance": "",
                        "structural_pages_h2": [],
                        "structural_pages_h3": []
                    },

                    "publications": [],
                    "magazine_issues": [],
                    "books": [],
                    "exhibitions": [],
                    "collections": [],

                    "navigation": {
                        "alphabetical": True
                    },

                    "visual": {
                        "show_quote": False,
                        "show_origin": False,
                        "show_gallery": True,
                        "show_publications": False
                    },

                    "source": "gallery_page"
                }

                artists.append(artist_obj)

        return artists
