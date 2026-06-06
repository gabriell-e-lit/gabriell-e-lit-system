import json
import os
import re
from collections import Counter, defaultdict

MERGED_TAGS_FILE = "database/json/tags_merged.json"
POSTS_FILE = "database/json/posts.json"
OUTPUT_FILE = "database/json/semantic_report.json"

HTML_TAGS = re.compile(r"<[^>]+>")

# Думи, които винаги означават НЕ-автор
INSTITUTION_WORDS = [
    "галерия", "литература", "изкуства", "култура", "новини",
    "събития", "театър", "музика", "кино", "фестивал",
    "музей", "център", "фондация", "сдружение", "клуб",
    "студио", "академия", "университет", "институт"
]

# Жанрови думи
GENRE_WORDS = [
    "поезия", "проза", "есе", "роман", "разказ", "хайку",
    "фантастика", "критика", "драма"
]

# Фамилни окончания (български)
BG_LASTNAME_SUFFIXES = [
    "ов", "ев", "ин", "ски", "ова", "ева", "ина", "иева",
    "арова", "чева", "кова", "цка", "чка"
]

def load_json(path):
    if not os.path.exists(path):
        print(f"Липсва файл: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    if not text:
        return ""
    text = HTML_TAGS.sub(" ", text)
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-Zа-яА-Я0-9\- ]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def looks_like_real_person(name, slug):
    parts = name.split()

    # 1) Име с две или повече думи → почти сигурно човек
    if len(parts) >= 2:
        return True

    # 2) Еднословно име, започващо с главна буква → псевдоним или чуждо име
    if len(parts) == 1 and name[0].isupper():
        return True

    # 3) slug от вида ime-familia или ime-familia-psevdonim
    slug_parts = slug.split("-")
    if 1 <= len(slug_parts) <= 3:
        # Проверка дали частите приличат на имена (букви, без цифри)
        if all(re.match(r"^[a-zA-Zа-яА-Я]+$", p) for p in slug_parts):
            return True

    # 4) Име с диакритики → почти винаги човек
    if re.search(r"[áéíóúàèìòùâêîôûäëïöüçñłśźżőű]", name.lower()):
        return True

    return False

def looks_like_non_author(name, slug):
    name_l = name.lower()
    slug_l = slug.lower()

    # 1) Институции
    for w in INSTITUTION_WORDS:
        if w in name_l or w in slug_l:
            return True

    # 2) Жанрови думи
    for w in GENRE_WORDS:
        if w in name_l or w in slug_l:
            return True

    # 3) Име в кавички → институция
    if "„" in name_l or "\"" in name_l:
        return True

    # 4) slug с цифри → не е автор
    if re.search(r"\d", slug_l):
        return True

    # 5) slug с повече от 2 тирета → не прилича на име
    if slug_l.count("-") > 2:
        return True

    return False

def main():
    tags = load_json(MERGED_TAGS_FILE)
    posts = load_json(POSTS_FILE)

    tags_by_id = {t["id"]: t for t in tags}
    tag_text = defaultdict(str)

    # Събиране на текст за ключови думи (само за справка)
    for post in posts:
        combined = clean_text(
            " ".join([
                post.get("title", {}).get("rendered", ""),
                post.get("excerpt", {}).get("rendered", ""),
                post.get("content", {}).get("rendered", "")
            ])
        )
        for tag_id in post.get("tags", []):
            if tag_id in tags_by_id:
                tag_text[tag_id] += " " + combined

    report = {
        "misclassified_authors": [],
        "tag_summaries": []
    }

    for tag in tags:
        tag_id = tag["id"]
        slug = tag["slug"]
        name = tag["name"]
        type_key = tag["type_key"]

        text = tag_text[tag_id]
        keywords = Counter(text.split()).most_common(15)

        # Маркираме като грешка само ако:
        # 1) е маркиран като author
        # 2) прилича на НЕ-автор
        # 3) НЕ прилича на човек
        if type_key == "author":
            if looks_like_non_author(name, slug) and not looks_like_real_person(name, slug):
                report["misclassified_authors"].append({
                    "id": tag_id,
                    "slug": slug,
                    "name": name,
                    "reason": "Жанр/категория/институция, маркирана като автор",
                    "top_keywords": keywords
                })

        report["tag_summaries"].append({
            "id": tag_id,
            "slug": slug,
            "name": name,
            "type_key": type_key,
            "top_keywords": keywords
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    print("Готово! Създаден е semantic_report.json")
    print(f" - Misclassified authors: {len(report['misclassified_authors'])}")


if __name__ == "__main__":
    main()