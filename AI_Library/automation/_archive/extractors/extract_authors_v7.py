import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v7.json"


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def extract_name_from_h2(h2):
    """Основен източник: <h2><a>Име</a></h2>"""
    if not h2:
        return ""
    a = h2.find("a")
    if a:
        return clean_text(a.get_text())
    return ""


def extract_name_from_strong(content_div):
    """Fallback: <strong><a>Име</a></strong> вътре в биографията"""
    if not content_div:
        return ""
    strong = content_div.find("strong")
    if strong:
        a = strong.find("a")
        if a:
            return clean_text(a.get_text())
    return ""


def extract_bio(content_div):
    """Събира всички <p> вътре в блока с биографията"""
    if not content_div:
        return ""
    paragraphs = content_div.find_all("p")
    bio_parts = [clean_text(p.get_text()) for p in paragraphs if clean_text(p.get_text())]
    return "\n\n".join(bio_parts)


def extract_authors(html):
    soup = BeautifulSoup(html, "html.parser")

    # Намираме всички блокове с биография
    content_blocks = soup.find_all("div", class_="wp-block-media-text__content")

    authors = []

    for content_div in content_blocks:

        # Търсим най-близкия предходен <h2>
        h2 = content_div.find_previous("h2", class_="wp-block-heading")

        # Опитваме се да вземем име от H2
        name = extract_name_from_h2(h2)

        # Ако H2 липсва или е празен → fallback към strong
        if not name:
            name = extract_name_from_strong(content_div)

        # Ако пак няма име → пропускаме (не би трябвало да се случи)
        if not name:
            continue

        # Биография
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