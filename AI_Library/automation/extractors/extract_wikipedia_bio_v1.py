import requests
from bs4 import BeautifulSoup
import json
import re

INPUT_JSON = "database/json/authors_with_wikipedia.json"
OUTPUT_JSON = "database/json/authors_with_wikipedia_bio.json"


def clean_text(t):
    if not t:
        return ""
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def extract_first_paragraph(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return ""

        soup = BeautifulSoup(r.text, "html.parser")

        content = soup.find("div", {"class": "mw-parser-output"})
        if not content:
            return ""

        for p in content.find_all("p", recursive=False):
            text = clean_text(p.get_text())
            if len(text) > 50:
                return text

        return ""
    except:
        return ""


def main():
    print("Старт на extract_wikipedia_bio_v1...")

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        authors = json.load(f)

    for a in authors:
        url = a.get("wikipedia_url", "")
        if url:
            bio = extract_first_paragraph(url)
            if bio:
                a["bio_wikipedia"] = bio

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()