import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "post_page.html"
INPUT_AUTHORS_JSON = "database/json/authors_with_wikipedia.json"
OUTPUT_JSON = "database/json/authors_with_fragments.json"

PSEUDONYMS = ["КАС", "KAS", "Kas"]

BIO_HEADERS = [
    "биография",
    "биографични бележки",
    "в паметта ни",
    "за автора",
    "за авторката",
    "за поета",
    "за писателя",
    "за художника",
    "за твореца"
]


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def normalize_header(h):
    h = h.lower()
    h = re.sub(r"[^\w\s]", " ", h)
    h = re.sub(r"\s+", " ", h).strip()
    return h


def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[^a-zа-яёіїєґ0-9]+", "", name)
    return name


WRITER_KEYWORDS = [
    "е български", "е българска",
    "роден", "родена",
    "завършил", "завършила",
    "поет", "писател", "преводач", "критик", "есеист",
    "автор е на", "публикувал е"
]

ARTIST_KEYWORDS = [
    "художник", "художничка",
    "живопис", "графика", "илюстрации",
    "изложба", "обща изложба", "самостоятелна изложба",
    "галерия", "пленер"
]

ALL_KEYWORDS = WRITER_KEYWORDS + ARTIST_KEYWORDS


def extract_main_content(soup):
    content = soup.find("div", class_="entry-content")
    if content:
        return content
    article = soup.find("article")
    if article:
        return article
    return soup


def extract_structured_bio(content):
    bio_text = []

    headers = content.find_all(["h2", "h3", "h4"])

    for h in headers:
        title = normalize_header(h.get_text())

        if any(key in title for key in BIO_HEADERS):
            for sibling in h.find_all_next():
                if sibling.name in ["h2", "h3", "h4"]:
                    break
                if sibling.name == "p":
                    bio_text.append(clean_text(sibling.get_text()))
            break

    return " ".join(bio_text).strip()


def extract_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [clean_text(p) for p in parts if clean_text(p)]


def find_keyword_fragments(text):
    sentences = extract_sentences(text)
    fragments = []

    for i, s in enumerate(sentences):
        for kw in ALL_KEYWORDS:
            if kw in s.lower():
                context = []
                if i > 0:
                    context.append(sentences[i - 1])
                context.append(sentences[i])
                if i < len(sentences) - 1:
                    context.append(sentences[i + 1])
                fragments.append(" ".join(context))
                break

    return fragments


def match_fragment_to_author(fragment, authors):
    fragment_norm = normalize_name(fragment)

    for author in authors:
        name = author["name"]

        if name.upper() in PSEUDONYMS:
            continue

        name_norm = normalize_name(name)

        if len(name_norm) < 4:
            continue

        if re.search(r"\b" + re.escape(name_norm) + r"\b", fragment_norm):
            return name

    return None


def main():
    print("Старт на extract_bio_from_posts_v4...")

    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    content = extract_main_content(soup)

    with open(INPUT_AUTHORS_JSON, "r", encoding="utf-8") as f:
        authors = json.load(f)

    structured_bio = extract_structured_bio(content)

    text = clean_text(content.get_text())
    keyword_fragments = find_keyword_fragments(text)

    for author in authors:
        if author["name"].upper() in PSEUDONYMS:
            continue

        if structured_bio:
            if "bio_fragments" not in author:
                author["bio_fragments"] = []
            author["bio_fragments"].append(structured_bio)

        for fragment in keyword_fragments:
            matched = match_fragment_to_author(fragment, [author])
            if matched:
                if "bio_fragments" not in author:
                    author["bio_fragments"] = []
                author["bio_fragments"].append(fragment)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()