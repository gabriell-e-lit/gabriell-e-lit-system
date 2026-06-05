import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v8.json"


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def extract_bio(content_div):
    """Събира всички <p> вътре в блока с биографията."""
    if not content_div:
        return ""
    paragraphs = content_div.find_all("p")
    bio_parts = [clean_text(p.get_text()) for p in paragraphs if clean_text(p.get_text())]
    return "\n\n".join(bio_parts)


def extract_authors(html):
    soup = BeautifulSoup(html, "html.parser")

    # 1) Всички H2 заглавия (автори)
    h2_list = soup.find_all("h2", class_="wp-block-heading")

    # Пропускаме първото H2 (заглавие на страницата)
    if h2_list:
        h2_list = h2_list[1:]

    # 2) Всички биографични блокове
    bio_blocks = soup.find_all("div", class_="wp-block-media-text__content")

    authors = []

    # 3) Сдвояване по позиция
    bio_index = 0

    for h2 in h2_list:
        name = clean_text(h2.get_text())

        # Ако има биографичен блок за този автор
        if bio_index < len(bio_blocks):
            bio = extract_bio(bio_blocks[bio_index])
            bio_index += 1
        else:
            bio = ""

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
