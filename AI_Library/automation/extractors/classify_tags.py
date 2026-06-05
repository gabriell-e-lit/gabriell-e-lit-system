import json
import os
import re

# Пътища към файловете
TAGS_FILE = "database/json/tags.json"
CATEGORIES_FILE = "database/json/categories.json"
OUTPUT_FILE = "database/json/tags_classified.json"

# Типове тагове според редакционната структура
TAG_TYPES = {
    "author": "Автор",
    "book": "Книга",
    "exhibition": "Изложба (творческа единица)",
    "format": "Формат на издание",
    "genre": "Жанр / форма",
    "category": "Категория / направление",
    "organization": "Организация / институция",
    "event": "Конкурс / събитие",
    "theme": "Тематичен / концептуален",
    "invalid": "Празен / автоматичен / грешен"
}

# Специални еквиваленти на категории
SPECIAL_CATEGORY_EQUIVALENTS = {
    "съвременна поезия",
    "съвременна проза"
}

# Ключови думи
KEYWORDS = {
    "format": [
        "е-книга", "е книга", "електронна книга",
        "р-книга", "р книга", "хартиена книга",
        "pdf", "epub", "аудио", "аудиокнига"
    ],
    "event": [
        "конкурс", "фестивал", "събитие",
        "премиера", "откриване", "представяне",
        "публична покана", "покана", "покана за участие", "покана - отговор"
    ],
    "organization": [
        "галерия", "институт", "издателство", "читалище", "нч",
        "клуб", "съюз", "вестник", "списание",
        "център", "музей", "фондация", "университет",
        # чуждоезикови маркери за институции
        "centre", "international", "documentation", "research",
        "institute", "association", "foundation"
    ],
    "genre": [
        "миниатюра", "притча", "хайку", "символизъм",
        "поезия", "есе", "разказ", "роман", "афоризми",
        "импресионизъм", "танка", "тан-ку", "танка проза",
        "хайбун", "хайга", "ренсаку",
        "документална проза", "проза", "къса проза"
    ],
    "theme": [
        "море", "детство", "любов", "самота",
        "светлина", "тишина", "път", "дом"
    ]
}

# Академични / почетни титли, които да се игнорират при разпознаване на автори
ACADEMIC_TITLES_PREFIXES = [
    "проф. дн", "проф. д.н.", "проф. д. н.",
    "проф.", "проф ",
    "доц. дн", "доц. д.н.", "доц. д. н.",
    "доц.", "доц ",
    "акад.", "акад ",
    "д-р", "д-р.", "д.р.", "д. р.",
    "дн", "д.н."
]

# Безопасна нормализация (само за сравнение, не за промяна на данни)
def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^\w\sа-яА-ЯёЁіІїЇєЄ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_protected_categories():
    categories = load_json(CATEGORIES_FILE)
    protected = set()
    for cat in categories:
        name = (cat.get("name") or "").strip()
        if name:
            protected.add(normalize(name))
    # добавяме и специалните еквиваленти
    for eq in SPECIAL_CATEGORY_EQUIVALENTS:
        protected.add(normalize(eq))
    return protected


def contains_word(text: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", text) is not None


def strip_academic_title(name: str) -> str:
    """
    Премахва академични титли в началото на името, за да може да се разпознае автор.
    Не се записва никъде – използва се само за класификация.
    """
    name_stripped = name.strip()
    lower = name_stripped.lower()
    for prefix in ACADEMIC_TITLES_PREFIXES:
        if lower.startswith(prefix):
            # режем префикса и евентуален следващ интервал
            cut_len = len(prefix)
            return name_stripped[cut_len:].lstrip(" .,-")
    return name_stripped


def classify_tag(name: str, slug: str, protected_categories: set) -> str:
    name = (name or "").strip()
    slug = (slug or "").strip()
    name_lower = name.lower()
    normalized_name = normalize(name)

    # 0) Празни / грешни slug-ове
    if slug.startswith("%") or slug == "":
        return "invalid"

    # 1) Читалища (НЧ ...) винаги са организации
    if name.startswith("НЧ ") or name_lower.startswith("народно читалище"):
        return "organization"

    # 2) Автор с академична титла в началото
    stripped_for_author = strip_academic_title(name)
    stripped_parts = stripped_for_author.split()
    if len(stripped_parts) in (2, 3):
        # ако след премахване на титлата имаме 2–3 имена → автор
        return "author"

    # 3) Категории (твърдо правило – след титлите, преди всичко друго)
    if normalized_name in protected_categories:
        return "category"

    # 4) Формати
    for kw in KEYWORDS["format"]:
        if contains_word(name_lower, kw):
            return "format"

    # 5) Събития
    for kw in KEYWORDS["event"]:
        if contains_word(name_lower, kw):
            return "event"

    # 6) Организации
    for kw in KEYWORDS["organization"]:
        if contains_word(name_lower, kw):
            return "organization"

    # 7) Жанрове
    for kw in KEYWORDS["genre"]:
        if contains_word(name_lower, kw):
            return "genre"

    # 8) Книга: "Заглавие" - Автор
    if name.startswith('"'):
        return "book"

    # 9) Теми
    for kw in KEYWORDS["theme"]:
        if contains_word(name_lower, kw):
            return "theme"

    # 10) Автор с псевдоним: "Име Фамилия - Псевдоним"
    if " - " in name:
        left, right = name.split(" - ", 1)
        left = left.strip()
        right = right.strip()
        if len(left.split()) in (2, 3) and right:
            return "author"

    # 11) Автор без псевдоним: две или три имена
    parts = name.split()
    if len(parts) in (2, 3):
        return "author"

    # 12) По подразбиране → категория
    return "category"


def main():
    if not os.path.exists(TAGS_FILE):
        print(f"Липсва файл с тагове: {TAGS_FILE}")
        return

    tags = load_json(TAGS_FILE)
    protected_categories = build_protected_categories()

    classified = []

    for tag in tags:
        name = tag.get("name", "")
        slug = tag.get("slug", "")

        tag_type_key = classify_tag(name, slug, protected_categories)
        tag_type_label = TAG_TYPES.get(tag_type_key, "Категория / направление")

        classified.append({
            "name": name,
            "slug": slug,
            "type_key": tag_type_key,
            "type": tag_type_label
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(classified, f, ensure_ascii=False, indent=4)

    print("Класификацията на таговете е завършена.")
    print(f"Резултатът е записан в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()