from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def extract_authors_from_canon_page(html, default_role=None):
    """
    Extracts canonical authors from a page using:
    - H3.author-name  → author identity
    - next .author-block → photo + links
    - H2.author-role → role (if present)
    - fallback: nearest H2 above the author

    Returns objects in AuthorModel_v3 structure (only filled fields).
    """

    soup = BeautifulSoup(html, "html.parser")
    authors = []

    # 1. Collect all roles explicitly marked with author-role
    explicit_roles = {}
    for h2 in soup.find_all("h2", class_=lambda c: c and "author-role" in c):
        role_text = h2.get_text(strip=True)
        explicit_roles[h2] = role_text

    # 2. Find all author names (H3 or H4 with class author-name)
    name_blocks = soup.find_all(["h3", "h4"], class_=lambda c: c and "author-name" in c)

    for name_block in name_blocks:
        name_display = name_block.get_text(strip=True)

        # Fallback slug from name
        slug = normalize_slug(name_display)

        # 3. Find the next author-block after the name
        block = name_block.find_next("div", class_=lambda c: c and "author-block" in c)

        tag_url = ""
        static_page_url = ""
        wikipedia_url = ""
        photo_url = ""
        photo_alt = ""

        if block:
            # Extract photo
            img = block.find("img")
            if img:
                photo_url = img.get("src", "").strip()
                photo_alt = img.get("alt", "").strip()

            # Extract links
            links = block.find_all("a", href=True)
            for link in links:
                href = link["href"]

                if "/tag/" in href:
                    tag_url = href
                    # slug from tag URL overrides fallback
                    slug = urlparse(href).path.rstrip("/").split("/")[-1]

                elif "/authors/" in href:
                    static_page_url = href

                elif "wikipedia.org" in href:
                    wikipedia_url = href

        # 4. Determine role
        role = None

        # Priority 1: explicit author-role marker
        if explicit_roles:
            for h2 in reversed(soup.find_all("h2")):
                if h2 in explicit_roles and h2.sourcepos < name_block.sourcepos:
                    role = explicit_roles[h2]
                    break

        # Priority 2: default_role parameter
        if not role and default_role:
            role = default_role

        # Priority 3: fallback → nearest H2 above
        if not role:
            h2 = name_block.find_previous("h2")
            if h2:
                role = h2.get_text(strip=True)
            else:
                role = "Неопределена роля"

        author_id = f"author_{slug.replace('-', '_')}"

        # 5. Build AuthorModel_v3 structure (only filled fields)
        author_obj = {
            "seo": {
                "title": "",
                "description": "",
                "canonical_url": ""
            },

            "identity": {
                "author_id": author_id,
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
                "url": photo_url,
                "alt": photo_alt
            },

            "origin": {
                "country": "",
                "city": "",
                "birth_year": "",
                "death_year": ""
            },

            "links": {
                "tag_url": tag_url,
                "gallery_subcategory": "",
                "gallery_url": "",
                "library_url": static_page_url
            },

            "structure": {
                "structural_pages_h2": [],
                "structural_pages_h3": [],
                "first_appearance": ""
            },

            "books": [],
            "publications": [],
            "magazine_issues": [],
            "exhibitions": [],
            "collections": [],

            "navigation": {
                "alphabetical": True
            },

            "visual": {
                "show_quote": False,
                "show_origin": False,
                "show_gallery": False,
                "show_publications": False
            },

            "role": role,
            "source": "canon_page"
        }

        authors.append(author_obj)

    return authors


def normalize_slug(name):
    """
    Converts a Cyrillic name into a slug-like Latin identifier.
    Minimal transliteration for fallback cases.
    """
    name = name.lower()
    name = re.sub(r"[^a-zа-яё0-9\s-]", "", name)
    name = name.replace(" ", "-")
    return name
