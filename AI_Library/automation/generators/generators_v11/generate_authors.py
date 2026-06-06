import json
import os
import re
from collections import Counter

POSTS_FILE = "database/json/posts.json"
MERGED_TAGS_FILE = "database/json/tags_merged.json"
OUTPUT_FILE = "database/json/authors.json"

MIN_KEYWORD_LEN = 4
TOP_KEYWORDS_PER_AUTHOR = 20

STOPWORDS_BG = {
    "и", "в", "на", "за", "с", "по", "от", "до", "че", "не", "се", "ще",
    "както", "като", "но", "или", "та", "ни", "ви", "аз", "ти", "той",
    "тя", "то", "ние", "вие", "те", "това", "този", "тази", "тези",
    "един", "една", "едно", "няма", "има", "беше", "са", "съм", "сме",
    "сте", "бил", "била", "били", "било"
}

def load_json(path):
    if not os.path.exists(path):
        print(f"Липсва файл: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-zа-я0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(text: str):
    norm = normalize_text(text)
    words = norm.split()
    filtered = [
        w for w in words
        if len(w) >= MIN_KEYWORD_LEN and w not in STOPWORDS_BG
    ]
    counter = Counter(filtered)
    return [w for w, _ in counter.most_common(TOP_KEYWORDS_PER_AUTHOR)]


def extract_rendered(field):
    if isinstance(field, dict):
        return field.get("rendered", "")
    if isinstance(field, str):
        return field
    return ""


def main():
    posts = load_json(POSTS_FILE)
    merged_tags = load_json(MERGED_TAGS_FILE)

    # Индекс по ID → merged tag
    tags_by_id = {t["id"]: t for t in merged_tags if "id" in t}

    authors = {}

    for post in posts:
        post_id = post.get("id")
        post_slug = post.get("slug", "")
        post_url = post.get("link", "")
        post_date = post.get("date", "")

        post_title = extract_rendered(post.get("title"))
        post_excerpt = extract_rendered(post.get("excerpt"))
        post_content = extract_rendered(post.get("content"))

        combined_text = " ".join([post_title, post_excerpt, post_content])

        post_tags = post.get("tags") or []

        for tag_id in post_tags:
            tag = tags_by_id.get(tag_id)
            if not tag:
                continue

            if tag.get("type_key") != "author":
                continue

            author_slug = tag.get("slug")
            author_name = tag.get("name")

            if not author_slug or not author_name:
                continue

            if author_slug not in authors:
                authors[author_slug] = {
                    "name": author_name,
                    "slug": author_slug,
                    "bio": "",
                    "keywords": [],
                    "nationality": "",
                    "roles": [],
                    "links": {
                        "website": "",
                        "facebook": "",
                        "instagram": "",
                        "other": ""
                    },
                    "posts": [],
                    "_kw_text": ""
                }

            authors[author_slug]["posts"].append({
                "id": post_id,
                "title": post_title,
                "slug": post_slug,
                "url": post_url,
                "date": post_date
            })

            authors[author_slug]["_kw_text"] += " " + combined_text

    # Извличаме ключови думи
    for slug, data in authors.items():
        kw_text = data.pop("_kw_text", "")
        data["keywords"] = extract_keywords(kw_text)

    authors_list = list(authors.values())

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(authors_list, f, ensure_ascii=False, indent=4)

    print(f"Генериран е файл с автори: {OUTPUT_FILE}")
    print(f"Общ брой автори: {len(authors_list)}")


if __name__ == "__main__":
    main()
