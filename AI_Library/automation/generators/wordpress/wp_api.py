# generator/wordpress/wp_api.py (v12)

import requests
from typing import Optional, Dict, List
from AI_Library.utils.logging import Logger


class WordPressAPI:
    """
    Обвивка за WordPress REST API.
    Използва Basic Auth (username + application password).
    """

    def __init__(self, base_url: str, username: str, app_password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.app_password = app_password
        self.logger = Logger("WordPressAPI")

    # ---------------------------------------------------------
    # 1) Вътрешен метод за заявки
    # ---------------------------------------------------------
    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                auth=(self.username, self.app_password),
                **kwargs
            )
        except Exception as e:
            self.logger.error(f"Грешка при заявка към WordPress: {e}")
            return None

        if not response.ok:
            self.logger.error(
                f"Грешка от WordPress API ({response.status_code}): {response.text}"
            )
            return None

        try:
            return response.json()
        except Exception:
            return response.text

    # ---------------------------------------------------------
    # 2) Тагове
    # ---------------------------------------------------------
    def find_tag_by_slug(self, slug: str) -> Optional[Dict]:
        endpoint = f"/wp-json/wp/v2/tags?slug={slug}"
        data = self._request("GET", endpoint)
        if isinstance(data, list) and data:
            return data[0]
        return None

    def create_tag(self, name: str, slug: str) -> Dict:
        endpoint = "/wp-json/wp/v2/tags"
        payload = {
            "name": name,
            "slug": slug,
        }
        return self._request("POST", endpoint, json=payload)

    def update_tag_content(self, tag_id: int, html: str):
        endpoint = f"/wp-json/wp/v2/tags/{tag_id}"
        payload = {
            "description": html
        }
        return self._request("POST", endpoint, json=payload)

    # ---------------------------------------------------------
    # 3) Страници
    # ---------------------------------------------------------
    def get_page(self, page_id: int) -> Optional[Dict]:
        endpoint = f"/wp-json/wp/v2/pages/{page_id}"
        return self._request("GET", endpoint)

    def update_page_content(self, page_id: int, html: str):
        endpoint = f"/wp-json/wp/v2/pages/{page_id}"
        payload = {
            "content": html
        }
        return self._request("POST", endpoint, json=payload)

    # ---------------------------------------------------------
    # 4) Специална функция: текущата страница „Автори на брой Х“
    # ---------------------------------------------------------
    def get_current_issue_page(self) -> Optional[Dict]:
        from config import load_config
        cfg = load_config()
        page_id = cfg["current_issue_page_id"]
        return self.get_page(page_id)

    def update_issue_page_content(self, page_id: int, html: str):
        return self.update_page_content(page_id, html)
