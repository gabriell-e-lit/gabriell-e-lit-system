import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
INPUT_AUTHORS_JSON = "database/json/authors_raw_v11.json"
OUTPUT_JSON = "database/json/authors_with_wikipedia.json"


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def normalize_name(name):
    """Нормализиране за сравнение."""
    name = name.lower()
    name = re.sub(r"[^a-zа-яёіїєґ0-9]+", "", name)
    return name


def extract_wikipedia_links(html):
    soup = BeautifulSoup(html, "html.parser")

    wikipedia_links = []

    # Универсален регекс за всички езикови версии на Уикипедия
    wiki_regex = r"https://[a-z]{2,3}\.wikipedia\.org/"

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.search(wiki_regex, href):
            link_text = clean_text(a.get_text())
            wikipedia_links.append((link_text, href))

    return wikipedia_links


def merge_wikipedia_links(authors, wiki_links):
    """
    Свързва Уикипедия линковете с авторите по нормализирано име.
    """
    # Създаваме map: нормализирано име → авторски запис
    author_map = {normalize_name(a["name"]): a for a in authors}

    for link_text, url in wiki_links:
        norm = normalize_name(link_text)

        if norm in author_map:
            author = author_map[norm]

            # Ако авторът няма URL → добавяме
            if "wikipedia_url" not in author or not author["wikipedia_url"]:
                author["wikipedia_url"] = url
            else:
                # Ако има няколко URL → взимаме най-дългия (най-пълен)
                if len(url) > len(author["wikipedia_url"]):
                    author["wikipedia_url"] = url

    return authors


def main():
    print("Старт на extract_external_links_v1...")

    # 1) Зареждаме HTML
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # 2) Зареждаме авторите от v11
    with open(INPUT_AUTHORS_JSON, "r", encoding="utf-8") as f:
        authors = json.load(f)

    # 3) Извличаме Уикипедия линкове
    wiki_links = extract_wikipedia_links(html)
    print(f"Намерени Уикипедия линкове: {len(wiki_links)}")

    # 4) Сдвояваме с авторите
    authors = merge_wikipedia_links(authors, wiki_links)

    # 5) Записваме резултата
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()