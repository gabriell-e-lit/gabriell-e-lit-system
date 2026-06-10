# gallery_extractor_v3.py
# Финална версия – работи по трите H2 заглавия и връща partial AuthorModel_v3

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class GalleryExtractorV3:
    """
    Extracts artist data from the dynamic gallery page:
    https://gabriell-e-lit.com/izdatelstvo/artists-e-gallery-gabriell-e-lit/

    Produces partial AuthorModel_v3 objects for artists.
    """

    # Трите точни заглавия → вътрешни категории
    CATEGORY_MAP = {
        "ХУДОЖНИЦИ В е-ГАЛЕРИЯ gabriell-e-lit": "gallery_e_gallery",
        "ХУДОЖНИЦИ В ИЗДАТЕЛСТВО gabriell-e-lit": "gallery_illustrator",
        "ХУДОЖНИЦИ, ПРЕДСТАВЕНИ В СП. “КАРТИНИ С ДУМИ И БАГРИ”": "gallery_magazine"
    }

    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    # ----------------- helpers -----------------
    def slugify(self, name: str) -> str:
        """
        Проста slug функция – достатъчна за fallback,
        ако няма tag линк.
        """
        name = name.lower()
        name = re.sub(r"[^a-zа-яё0-9\s-]", "", name)
        name = name.replace(" ", "-")
        return name

    # ----------------- main -----------------
    def extract(self):
        """
        Връща списък от partial AuthorModel_v3 обекти за художници.
        """
        artists = []

        # Всички H2 – търсим само тези, които са в CATEGORY_MAP
        h2_blocks = self.soup.find_all("h2")

        for h2 in h2_blocks:
            h2_text = h2.get_text(strip=True)

            # Определяме категорията по точния текст
            category = None
            for title, cat in self.CATEGORY_MAP.items():
                if title in h2_text:
                    category = cat
                    break

            if not category:
                continue  # този H2 не е от трите „официални“

            # Всички H3 след този H2, до следващ H2, са художници в тази категория
            h3_blocks = []
            next_node = h2.find_next_sibling()

            while next_node:
                if next_node.name == "h2":
                    break  # стигнали сме следващата категория
                if next_node.name == "h3":
                    h3_blocks.append(next_node)
                next_node = next_node.find_next_sibling()

            # Обработваме всеки художник
            for h3 in h3_blocks:
                name_display = h3.get_text(strip=True)

                # Опитваме да вземем slug от tag линк, ако има
                tag_url = ""
                a = h3.find("a", href=True)
                if a and "/tag/" in a["href"]:
                    tag_url = a["href"]
                    slug = urlparse(tag_url).path.rstrip("/").split("/")[-1]
                else:
                    slug = self.slugify(name_display)

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
