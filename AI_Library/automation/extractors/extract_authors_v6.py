import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v6.json"


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def extract_name(h2, content_div):
    """
    1) Основен източник: <h2><a>Име</a></h2>
    2) Fallback: <strong><a>Име</a></strong> вътре в биографията
    """
    # 1) Основен източник
    a = h2.find("a")
    if a:
        name = clean_text(a.get_text())
        if name:
            return name

    # 2) Fallback: strong вътре в биографията
    if content_div:
        strong = content_div.find("strong")
        if strong:
            a2 = strong.find("a")
            if a2:
                name2 = clean_text(a2.get_text())
                if name2:
                    return name2

    return ""


def extract_bio(content_div):
    """
    Събира всички <p> вътре в <div class="wp-block-media-text__content">
    """
    if not content_div:
        return ""

    paragraphs = content_div.find_all("p")
    bio_parts = [clean_text(p.get_text()) for p in paragraphs if clean_text(p.get_text())]

    return "\n\n".join(bio_parts)


def extract_authors(html):
    soup = BeautifulSoup(html, "html.parser")

    # Намираме всички H2 заглавия
    h2_list = soup.find_all("h2", class_="wp-block-heading")
    if not h2_list:
        return []

    authors = []

    # Пропускаме първото H2 ("Автори в брой...")
    h2_list = h2_list[1:]

    for h2 in h2_list:
        # Намираме следващия блок с биографията
        content_div = h2.find_next("div", class_="wp-block-media-text__content")

        # Извличаме име
        name = extract_name(h2, content_div)
        if not name:
            continue

        # Извличаме биография
        bio = extract_bio(content_div)

        authors.append({
            "name": name,
            "bio": bio
        })

    return authors


def main():
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    authors = extract_authors(html)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Извлечени са {len(authors)} автори.")


if __name__ == "__main__":
    main()