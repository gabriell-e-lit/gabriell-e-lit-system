import json
import os
from semantic_tags_v6 import looks_like_non_author, looks_like_real_person

MERGED_TAGS_FILE = "database/json/tags_merged.json"
OUTPUT_FILE = "database/json/tag_fixes.json"

# Фиксирани типове (стабилният слой)
FIXED_TYPES = [
    "author",
    "institution",
    "genre",
    "category",
    "theme",
    "book",
    "event",
    "contest",
    "noise"
]

def load_json(path):
    if not os.path.exists(path):
        print(f"Липсва файл: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def suggest_type(tag):
    """
    Предлага тип САМО ако current_type е 'author' или е празен/невалиден.
    Във всички други случаи уважава current_type.
    """

    name = tag["name"]
    slug = tag["slug"]
    current_type = tag["type_key"]

    # 1) Ако current_type е валиден → НЕ го променяме
    if current_type in FIXED_TYPES and current_type != "author":
        return current_type, "keep"

    # 2) Ако current_type е 'author', но НЕ прилича на автор → reclassify
    if current_type == "author":
        if looks_like_non_author(name, slug) and not looks_like_real_person(name, slug):
            return "institution", "reclassify"
        else:
            return "author", "keep"

    # 3) Ако current_type е празен или невалиден → предлагаме тип
    # Институции
    if looks_like_non_author(name, slug):
        return "institution", "reclassify"

    # Жанрови думи
    genre_words = ["поезия", "проза", "есе", "роман", "критика", "хайку", "фантастика"]
    if any(w in name.lower() for w in genre_words):
        return "genre", "reclassify"

    # Категории
    category_keywords = ["интервю", "новини", "събития", "анализ", "галерия"]
    if any(w in name.lower() for w in category_keywords):
        return "category", "reclassify"

    # Теми (една дума, главна буква)
    if len(name.split()) == 1 and name[0].isupper():
        return "theme", "reclassify"

    # Всичко останало → noise
    return "noise", "review"

def main():
    tags = load_json(MERGED_TAGS_FILE)

    fixes = {}

    for tag in tags:
        tag_id = tag["id"]
        name = tag["name"]
        slug = tag["slug"]
        current_type = tag["type_key"]

        suggested_type, action = suggest_type(tag)

        fixes[tag_id] = {
            "slug": slug,
            "name": name,
            "current_type": current_type,
            "suggested_type": suggested_type,
            "suggested_action": action,
            "notes": ""
        }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(fixes, f, ensure_ascii=False, indent=4)

    print("Готово! Създаден е tag_fixes.json")
    print(f" - Общо тагове: {len(fixes)}")
    print(" - Прегледай само 'reclassify' и 'review' секциите.")


if __name__ == "__main__":
    main()