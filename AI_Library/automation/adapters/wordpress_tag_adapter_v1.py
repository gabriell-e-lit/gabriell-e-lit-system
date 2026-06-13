# WordPressTagAdapter v1.0
# Извлича публикации на автор от WordPress таг страница

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any


class WordPressTagAdapter:
    """
    Адаптер за извличане на публикации от WordPress таг страница.
    Пример URL:
    https://gabriell-e-lit.com/tag/ivan-ivanov/
    """

    def __init__(self):
        pass

    # -----------------------------
    # UTILS
    # -----------------------------

    def fetch_html(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def extract_text(self, el):
        return el.get_text(strip=True) if el else ""

    # -----------------------------
    # MAIN EXTRACTION
    # -----------------------------

    def extract_publications(self, tag_url: str) -> List[Dict[str, Any]]:
        """
        Връща списък от публикации:
        [
            {
                "title": "...",
                "url": "...",
                "date": "...",
                "excerpt": "...",
                "featured_image": "..."
            }
        ]
        """

        soup = self.fetch_html(tag_url)
        articles = soup.find_all("article")

        publications = []

        for art in articles:
            # Заглавие
            title_el = art.select_one("h2.entry-title a")
            title = self.extract_text(title_el)
            url = title_el["href"] if title_el else ""

            # Дата
            date_el = art.find("time")
            date = date_el["datetime"] if date_el and date_el.has_attr("datetime") else ""
            if not date:
                date = self.extract_text(date_el)

            # Откъс
            excerpt_el = art.select_one(".entry-summary, .entry-content")
            excerpt = self.extract_text(excerpt_el)

            # Featured image
            img_el = art.select_one("img")
            featured_image = img_el["src"] if img_el else ""

            publications.append({
                "title": title,
                "url": url,
                "date": date,
                "excerpt": excerpt,
                "featured_image": featured_image
            })

        return publications
