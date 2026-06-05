import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "post_page.html"
INPUT_AUTHORS_JSON = "database/json/authors_with_wikipedia.json"
OUTPUT_JSON = "database/json/authors_with_fragments.json"

# Псевдоними, които НЕ трябва да получават биография
PSEUDONYMS = ["КАС", "KAS", "Kas"]

# Заглавия, които маркират биографична секция
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
    """Взимаме само основното съдържание на публикацията."""
    content = soup.find("div", class_="entry-content")
    if content:
        return content
    article = soup.find("article")
    if article:
        return article
    return soup  # fallback


def extract_structured_bio(content):
    """Извлича биография от структурирани секции (най-силен метод)."""
    bio_text = []

    # Намираме всички заглавия
    headers = content.find_all(["h2", "h3", "h4"])

    for h in headers:
        title = clean_text(h.get_text()).lower()

        # Проверяваме дали заглавието е биографично
        if any(key in title for key in BIO_HEADERS):
            # Вземаме всички параграфи след заглавието
            for sibling in h.find_all_next():
                if sibling.name in ["h2", "h3", "h4"]:
                    break  # спираме при следващо заглавие
                if sibling.name == "p":
                    bio_text.append(clean_text(sibling.get_text()))
            break

    return " ".join(bio_text).strip()


def extract_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [clean_text(p) for p in parts if clean_text(p)]


def find_keyword_fragments(text):
    """Резервен метод: ключови думи + контекст."""
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

        # Псевдоними – прескачаме
        if name.upper() in PSEUDONYMS:
            continue

        name_norm = normalize_name(name)

        # Минимална дължина
        if len(name_norm) < 4:
            continue

        # Съвпадение само като отделна дума
        if re.search(r"\b" + re.escape(name_norm) + r"\b", fragment_norm):
            return name

    return None


def main():
    print("Старт на extract_bio_from_posts_v3...")

    # 1) Зареждаме HTML
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    content = extract_main_content(soup)

    # 2) Зареждаме авторите
    with open(INPUT_AUTHORS_JSON, "r", encoding="utf-8") as f:
        authors = json.load(f)

    # 3) Структурна биография
    structured_bio = extract_structured_bio(content)

    # 4) Ключови фрагменти (резервен метод)
    text = clean_text(content.get_text())
    keyword_fragments = find_keyword_fragments(text)

    # 5) Сдвояване
    for author in authors:
        if author["name"].upper() in PSEUDONYMS:
            continue

        # Структурна биография – най-силна
        if structured_bio:
            if "bio_fragments" not in author:
                author["bio_fragments"] = []
            author["bio_fragments"].append(structured_bio)

        # Ключови фрагменти – резервни
        for fragment in keyword_fragments:
            matched = match_fragment_to_author(fragment, [author])
            if matched:
                if "bio_fragments" not in author:
                    author["bio_fragments"] = []
                author["bio_fragments"].append(fragment)

    # 6) Запис
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()