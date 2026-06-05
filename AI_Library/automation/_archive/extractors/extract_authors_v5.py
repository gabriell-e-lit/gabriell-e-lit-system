import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v5.json"


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def collect_bio_paragraphs(start):
    """
    Събира всички последователни <p> след даден елемент,
    докато не срещне <h2> или <hr>.
    """
    bio_parts = []
    node = start.find_next_sibling()
    while node:
        if node.name in ("h2", "hr"):
            break
        if node.name == "p":
            bio_parts.append(clean_text(node.get_text()))
        node = node.find_next_sibling()
    return "\n\n".join(p for p in bio_parts if p)


def extract_first_author(soup):
    """
    Първият автор е структуриран като:
    <p><strong><a>Име</a></strong> ...</p>
    Връща (name, bio) или None.
    """
    p_tags = soup.find_all("p")
    for p in p_tags:
        strong = p.find("strong")
        if not strong:
            continue
        a = strong.find("a")
        if not a:
            continue
        name = clean_text(a.get_text())
        if not name:
            continue

        # биографията: този <p> + следващите <p> до <hr> или <h2>
        bio_parts = [clean_text(p.get_text())]
        node = p.find_next_sibling()
        while node:
            if node.name in ("h2", "hr"):
                break
            if node.name == "p":
                bio_parts.append(clean_text(node.get_text()))
            node = node.find_next_sibling()
        bio = "\n\n".join(part for part in bio_parts if part)

        return {"name": name, "bio": bio}
    return None


def extract_other_authors(soup):
    """
    Останалите автори са в:
    <h2 class="wp-block-heading"><a>Име</a></h2>
    Биографията е в последователните <p> след h2 до <hr> или следващ h2.
    """
    authors = []
    h2_list = soup.find_all("h2", class_="wp-block-heading")
    if not h2_list:
        return authors

    # първото h2 е "Автори в брой..." – пропускаме го
    h2_list = h2_list[1:]

    for h2 in h2_list:
        a = h2.find("a")
        if not a:
            continue
        name = clean_text(a.get_text())
        if not name:
            continue

        bio = collect_bio_paragraphs(h2)
        authors.append({"name": name, "bio": bio})

    return authors


def main():
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    authors = []

    first_author = extract_first_author(soup)
    if first_author:
        authors.append(first_author)

    authors.extend(extract_other_authors(soup))

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Извлечени са {len(authors)} автори.")


if __name__ == "__main__":
    main()