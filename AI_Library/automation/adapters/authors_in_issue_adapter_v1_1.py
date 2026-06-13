# AuthorsInIssueAdapter v1.1
# Извлича автори от страниците "Автори на брой Х"
# Различава нови автори (с блок медия+текст) от стари автори (без блок)

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any


class AuthorsInIssueAdapter:
    """
    Адаптер за страниците "Автори на брой Х".
    """

    def __init__(self):
        pass

    def fetch_html(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def extract_text(self, element):
        if not element:
            return ""
        return element.get_text(strip=True)

    def extract_authors_from_issue(self, url: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Връща:
        {
            "new_authors": [...],
            "existing_authors": [...]
        }
        """

        soup = self.fetch_html(url)
        h2_list = soup.find_all("h2")

        new_authors = []
        existing_authors = []

        for h2 in h2_list:
            name_display = self.extract_text(h2)
            if not name_display:
                continue

            # Проверяваме дали има линк към тага
            tag_link_el = h2.find("a")
            tag_url = tag_link_el["href"] if tag_link_el else ""

            # Следващият sibling е или блок медия+текст, или нещо друго
            block = h2.find_next_sibling()

            # Проверяваме дали това е блок медия+текст
            is_media_block = (
                block
                and block.name == "div"
                and "wp-block-media-text" in block.get("class", [])
            )

            if not is_media_block:
                # Това е стар автор → няма биография в този брой
                existing_authors.append({
                    "name_display": name_display,
                    "tag_url": tag_url,
                    "first_appearance": False
                })
                continue

            # Нов автор → извличаме снимка + биография
            img = block.select_one("img")
            photo_url = img["src"] if img else ""
            photo_alt = img["alt"] if img else ""

            bio_el = block.select_one("p, div")
            bio_text = bio_el.decode_contents() if bio_el else ""

            new_authors.append({
                "name_display": name_display,
                "name_original": name_display,

                "photo_url": photo_url,
                "photo_alt": photo_alt,

                "bio_short": "",
                "bio_long": bio_text,

                "quote": "",

                "country": "",
                "city": "",
                "birth_year": "",
                "death_year": "",

                "tag_url": tag_url,

                "first_appearance": True,

                "seo_title": name_display,
                "seo_description": self.extract_text(bio_el) if bio_el else "",
                "canonical_url": url + "#" + name_display.replace(" ", "-").lower(),
            })

        return {
            "new_authors": new_authors,
            "existing_authors": existing_authors
        }
