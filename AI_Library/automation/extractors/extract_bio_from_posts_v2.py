import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "post_page.html"
INPUT_AUTHORS_JSON = "database/json/authors_with_wikipedia.json"
OUTPUT_JSON = "database/json/authors_with_fragments.json"

# Псевдоними, които НЕ трябва да получават биография
PSEUDONYMS = ["КАС", "KAS", "Kas"]


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[^a-zа-яёіїєґ0-9]+", "", name)
    return name


# Ключови думи за писатели
WRITER_KEYWORDS = [
    "е български", "е българска",
    "роден", "родена",
    "завършил", "завършила",
    "поет", "писател", "преводач", "критик", "есеист",
    "автор е на", "публикувал е"
]

# Ключови думи за художници
ARTIST_KEYWORDS = [
    "художник", "художничка",
    "живопис", "графика", "илюстрации",
    "изложба", "обща изложба", "самостоятелна изложба",
    "галерия", "пленер"
]

ALL_KEYWORDS = WRITER_KEYWORDS + ARTIST_KEYWORDS


def extract_main_content(soup):
    """
    Взимаме само основното съдържание на публикацията.
    Игнорираме sidebar, footer, менюта, widgets.
    """
    # Най-често срещаното в WordPress
    content = soup.find("div", class_="entry-content")
    if content:
        return clean_text(content.get_text())

    # fallback: article
    article = soup.find("article")
    if article:
        return clean_text(article.get_text())

    # fallback: целият текст (краен вариант)
    return clean_text(soup.get_text())


def extract_sentences(text):
    """Разделя текста на изречения."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [clean_text(p) for p in parts if clean_text(p)]


def find_bio_fragments(sentences):
    """Намира изречения с ключови думи + контекст."""
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

                fragment = " ".join(context)
                fragments.append(fragment)
                break

    return fragments


def match_fragment_to_author(fragment, authors):
    """Опитва да разпознае автора по име вътре в текста."""
    fragment_norm = normalize_name(fragment)

    for author in authors:
        name = author["name"]

        # 1) Прескачаме псевдоними
        if name.upper() in PSEUDONYMS:
            continue

        name_norm = normalize_name(name)

        # 2) Минимална дължина
        if len(name_norm) < 4:
            continue

        # 3) Съвпадение само като отделна дума
        if re.search(r"\b" + re.escape(name_norm) + r"\b", fragment_norm):
            return name

    return None


def main():
    print("Старт на extract_bio_from_posts_v2...")

    # 1) Зареждаме HTML
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # 2) Взимаме само основното съдържание
    text = extract_main_content(soup)

    # 3) Зареждаме авторите
    with open(INPUT_AUTHORS_JSON, "r", encoding="utf-8") as f:
        authors = json.load(f)

    # 4) Разделяме текста на изречения
    sentences = extract_sentences(text)

    # 5) Намираме биографични фрагменти
    fragments = find_bio_fragments(sentences)
    print(f"Намерени биографични фрагменти: {len(fragments)}")

    # 6) Сдвояваме фрагментите с авторите
    for fragment in fragments:
        matched_name = match_fragment_to_author(fragment, authors)

        if matched_name:
            for a in authors:
                if a["name"] == matched_name:
                    if "bio_fragments" not in a:
                        a["bio_fragments"] = []
                    a["bio_fragments"].append(fragment)

    # 7) Записваме резултата
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
