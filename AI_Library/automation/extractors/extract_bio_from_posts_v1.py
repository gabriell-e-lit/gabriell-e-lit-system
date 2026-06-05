import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "post_page.html"   # публикация
INPUT_AUTHORS_JSON = "database/json/authors_with_wikipedia.json"
OUTPUT_JSON = "database/json/authors_with_fragments.json"


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
                # Вземаме контекст: предишно, текущо, следващо изречение
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
        name_norm = normalize_name(author["name"])
        if name_norm in fragment_norm:
            return author["name"]

    return None


def main():
    print("Старт на extract_bio_from_posts_v1...")

    # 1) Зареждаме HTML на публикацията
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    text = clean_text(soup.get_text())

    # 2) Зареждаме авторите
    with open(INPUT_AUTHORS_JSON, "r", encoding="utf-8") as f:
        authors = json.load(f)

    # 3) Разделяме текста на изречения
    sentences = extract_sentences(text)

    # 4) Намираме биографични фрагменти
    fragments = find_bio_fragments(sentences)
    print(f"Намерени биографични фрагменти: {len(fragments)}")

    # 5) Сдвояваме фрагментите с авторите
    for fragment in fragments:
        matched_name = match_fragment_to_author(fragment, authors)

        if matched_name:
            for a in authors:
                if a["name"] == matched_name:
                    if "bio_fragments" not in a:
                        a["bio_fragments"] = []
                    a["bio_fragments"].append(fragment)

    # 6) Записваме резултата
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()