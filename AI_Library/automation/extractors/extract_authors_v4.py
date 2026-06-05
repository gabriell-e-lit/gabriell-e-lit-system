import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v4.json"

def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()

def extract_authors(html):
    soup = BeautifulSoup(html, "html.parser")

    # Взимаме всички H2 заглавия
    h2_list = soup.find_all("h2", class_="wp-block-heading")
    if not h2_list:
        return []

    authors = []

    # Пропускаме първото H2 (секционно заглавие)
    h2_list = h2_list[1:]

    for h2 in h2_list:
        # Името е вътре в <a>
        a = h2.find("a")
        if not a:
            continue

        name = clean_text(a.get_text())

        # Биографията е първият <p> след H2
        p = h2.find_next("p")
        if not p:
            bio = ""
        else:
            bio = clean_text(p.get_text())

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