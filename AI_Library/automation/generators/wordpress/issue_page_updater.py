# generator/wordpress/issue_page_updater.py (v12)

from bs4 import BeautifulSoup
from AI_Library.utils.logging import Logger


class IssuePageUpdater:
    """
    Обновява страницата „Автори на брой Х“, като добавя линкове към таговете
    вътре в <h2 class="wp-block-heading">ИМЕ</h2>.

    Това превръща страницата в портал към автора.
    """

    def __init__(self, wp_api):
        self.wp = wp_api
        self.logger = Logger("IssuePageUpdater")

    # ---------------------------------------------------------
    # 1) Главен метод
    # ---------------------------------------------------------
    def update_issue_page(self, author_name: str, slug: str):
        """
        Обновява страницата „Автори на брой Х“ за даден автор.
        """
        page = self.wp.get_current_issue_page()
        if not page:
            self.logger.error("Не мога да заредя страницата „Автори на брой Х“.")
            return

        html = page["content"]["rendered"]
        soup = BeautifulSoup(html, "html.parser")

        updated = self._update_h2_link(soup, author_name, slug)

        if updated:
            new_html = str(soup)
            self.wp.update_issue_page_content(page["id"], new_html)
            self.logger.info(f"Обнових линка за автора: {author_name}")
        else:
            self.logger.warning(f"Не намерих H2 за автора: {author_name}")

    # ---------------------------------------------------------
    # 2) Обновяване на H2 елемент
    # ---------------------------------------------------------
    def _update_h2_link(self, soup, author_name: str, slug: str) -> bool:
        """
        Намира <h2 class="wp-block-heading">ИМЕ</h2> и добавя/поправя линка.
        """
        h2_list = soup.find_all("h2", class_="wp-block-heading")

        for h2 in h2_list:
            text = h2.get_text(strip=True)

            # Сравняваме нормализирано име
            if text.lower() != author_name.lower():
                continue

            tag_url = f"https://gabriell-e-lit.com/tag/{slug}/"

            # Ако вече има <a> вътре
            a = h2.find("a")
            if a:
                if a.get("href") != tag_url:
                    a["href"] = tag_url
                return True

            # Ако няма <a> → създаваме
            h2.clear()
            new_a = soup.new_tag("a", href=tag_url)
            new_a.string = author_name
            h2.append(new_a)

            return True

        return False
