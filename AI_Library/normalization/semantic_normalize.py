import json
import os
from collections import defaultdict
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
    Предлага тип за НЕ-авторски тагове.
    Това е само предложение — редакторът решава окончателно.
    """

    name = tag["name"]
    slug = tag["slug"]
    type_key = tag["type_key"]

    # 1) Ако е автор → остава автор
    if type_key == "author" and looks_like_real_person(name, slug):
        return "author"

    # 2) Ако прилича на институция
    if looks_like_non_author(name, slug):
        # Институции имат най-висок приоритет
        return "institution"

    # 3) Ако съдържа жанрова дума
    genre_words = ["поезия", "проза", "есе", "роман", "критика", "хайку", "фантастика"]
    if any(w in name.lower() for w in genre_words):
        return "genre"

    # 4) Ако прилича на рубрика (категория)
    category_keywords = ["интервю", "новини", "събития", "анализ", "галерия"]
    if any(w in name.lower() for w in category_keywords):
        return "category"

    # 5) Ако е тематичен таг (една дума, абстрактна)
    if len(name.split()) == 1 and name[0].isupper():
        return "theme"

    # 6) Всичко останало → noise
    return "noise"

def main():
    tags = load_json(MERGED_TAGS_FILE)

    fixes = {}

    for tag in tags:
        tag_id = tag["id"]
        name = tag["name"]
        slug = tag["slug"]
        type_key = tag["type_key"]

        # Предложение за нов тип
        suggested_type = suggest_type(tag)

        # Предложено действие
        if suggested_type == "author":
            action = "keep"
        elif suggested_type == "noise":
            action = "review"
        else:
            action = "reclassify"

        fixes[tag_id] = {
            "slug": slug,
            "name": name,
            "current_type": type_key,
            "suggested_type": suggested_type,
            "suggested_action": action,
            "notes": ""
        }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(fixes, f, ensure_ascii=False, indent=4)

    print("Готово! Създаден е tag_fixes.json")
    print(f" - Общо тагове: {len(fixes)}")
    print(" - Прегледай noise и reclassify секциите.")


if __name__ == "__main__":
    main()