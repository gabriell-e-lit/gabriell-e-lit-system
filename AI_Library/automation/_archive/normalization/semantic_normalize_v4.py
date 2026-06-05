import json
import os
from semantic_tags_v6 import looks_like_non_author, looks_like_real_person

MERGED_TAGS_FILE = "database/json/tags_merged.json"
POSTS_FILE = "database/json/posts.json"
AUTHORS_BY_ISSUE_FILE = "database/json/authors_by_issue.json"
OUTPUT_FILE = "database/json/tag_fixes.json"

FIXED_TYPES = [
    "author",
    "person",
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

def detect_visual_art(post):
    """Проверява дали публикацията съдържа изображения (визуални творби)."""
    content = post.get("content", {}).get("rendered", "").lower()
    return "<img" in content or "wp-image" in content

def detect_textual_work(post):
    """Проверява дали публикацията съдържа текстова творба."""
    keywords = ["стих", "поезия", "разказ", "есе", "творба", "превод", "антология"]
    text = (
        post.get("title", {}).get("rendered", "") +
        post.get("content", {}).get("rendered", "")
    ).lower()
    return any(k in text for k in keywords)

def detect_author_posts(tag_id, posts):
    """Връща True, ако тагът е свързан с публикации, съдържащи творби (текстови или визуални)."""
    for post in posts:
        if tag_id in post.get("tags", []):
            if detect_textual_work(post) or detect_visual_art(post):
                return True
    return False

def detect_person_posts(tag_id, posts):
    """Връща True, ако тагът е свързан с публикации, но без творби."""
    for post in posts:
        if tag_id in post.get("tags", []):
            return True
    return False

def is_author_in_issue_pages(name, authors_by_issue):
    """Проверява дали личността фигурира в 'Автори на броя'."""
    for issue, authors in authors_by_issue.items():
        if name in authors:
            return True
    return False

def suggest_type(tag, posts, authors_by_issue):
    name = tag["name"]
    slug = tag["slug"]
    current_type = tag["type_key"]
    tag_id = tag["id"]

    # 1) Ако current_type е валиден и не е author → не го пипаме
    if current_type in FIXED_TYPES and current_type != "author":
        return current_type, "keep"

    # 2) Ако е реално име → проверяваме контекста
    if looks_like_real_person(name, slug):

        # 2.1) Ако фигурира в "Автори на броя" → author
        if is_author_in_issue_pages(name, authors_by_issue):
            return "author", "reclassify" if current_type != "author" else "keep"

        # 2.2) Ако има творби (текстови или визуални) → author
        if detect_author_posts(tag_id, posts):
            return "author", "reclassify" if current_type != "author" else "keep"

        # 2.3) Ако има публикации, но не творби → person
        if detect_person_posts(tag_id, posts):
            return "person", "reclassify"

        # 2.4) Ако няма нищо → person
        return "person", "reclassify"

    # 3) Институции
    if looks_like_non_author(name, slug):
        return "institution", "reclassify"

    # 4) Жанрови думи
    genre_words = ["поезия", "проза", "есе", "роман", "критика", "хайку", "фантастика"]
    if any(w in name.lower() for w in genre_words):
        return "genre", "reclassify"

    # 5) Категории
    category_keywords = ["интервю", "новини", "събития", "анализ", "галерия"]
    if any(w in name.lower() for w in category_keywords):
        return "category", "reclassify"

    # 6) Теми
    if len(name.split()) == 1 and name[0].isupper():
        return "theme", "reclassify"

    # 7) Noise
    return "noise", "review"

def main():
    tags = load_json(MERGED_TAGS_FILE)
    posts = load_json(POSTS_FILE)
    authors_by_issue = load_json(AUTHORS_BY_ISSUE_FILE)

    fixes = {}

    for tag in tags:
        tag_id = tag["id"]
        suggested_type, action = suggest_type(tag, posts, authors_by_issue)

        fixes[tag_id] = {
            "slug": tag["slug"],
            "name": tag["name"],
            "current_type": tag["type_key"],
            "suggested_type": suggested_type,
            "suggested_action": action,
            "notes": ""
        }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(fixes, f, ensure_ascii=False, indent=4)

    print("Готово! Създаден е tag_fixes.json")
    print("Прегледай само 'reclassify' и 'review' секциите.")


if __name__ == "__main__":
    main()