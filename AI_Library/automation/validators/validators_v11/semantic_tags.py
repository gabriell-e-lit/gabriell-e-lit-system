import json
import os
import re
from collections import Counter, defaultdict

MERGED_TAGS_FILE = "database/json/tags_merged.json"
POSTS_FILE = "database/json/posts.json"
OUTPUT_FILE = "database/json/semantic_report.json"

# HTML и технически шум, който е безопасно да се премахне
NOISE_WORDS = {
    "https", "http", "www", "com", "gabriell", "izdatelstvo",
    "uploads", "content", "wp", "image", "class", "figure",
    "attachment", "data", "block", "title", "width", "height",
    "src", "href", "alt", "img", "jpg", "jpeg", "png", "gif",
    "quot", "amp", "nbsp", "optimole"
}

# HTML тагове
HTML_TAGS = re.compile(r"<[^>]+>")

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

def extract_keywords(text):
    words = text.split()
    filtered = []
    for w in words:
        if w in NOISE_WORDS:
            continue
        if re.match(r"^\d+$", w):
            continue
        if re.match(r".*-\d+$", w):
            continue
        filtered.append(w)
    return filtered

def main():
    tags = load_json(MERGED_TAGS_FILE)
    posts = load_json(POSTS_FILE)

    # Индекс по ID → merged tag
    tags_by_id = {t["id"]: t for t in tags}

    # Събиране на текст за всеки таг
    tag_text = defaultdict(str)

    for post in posts:
        post_title = post.get("title", {}).get("rendered", "")
        post_excerpt = post.get("excerpt", {}).get("rendered", "")
        post_content = post.get("content", {}).get("rendered", "")

        combined = clean_text(" ".join([post_title, post_excerpt, post_content]))
        for tag_id in post.get("tags", []):
            if tag_id in tags_by_id:
                tag_text[tag_id] += " " + combined

    # Семантичен анализ
    report = {
        "unknown_tags": [],
        "potential_authors": [],
        "duplicate_authors": [],
        "noise_candidates": [],
        "tag_summaries": []
    }

    # Откриване на дублирани автори по име
    name_map = defaultdict(list)
    for t in tags:
        if t["type_key"] == "author":
            name_map[t["name"].lower()].append(t)

    for name, group in name_map.items():
        if len(group) > 1:
            report["duplicate_authors"].append({
                "name": name,
                "slugs": [g["slug"] for g in group],
                "ids": [g["id"] for g in group]
            })

    # Анализ на всеки таг
    for tag in tags:
        tag_id = tag["id"]
        slug = tag["slug"]
        name = tag["name"]
        type_key = tag["type_key"]

        text = tag_text[tag_id]
        keywords = extract_keywords(text)
        freq = Counter(keywords).most_common(15)

        # Тагове без класификация
        if type_key == "unknown":
            report["unknown_tags"].append({
                "id": tag_id,
                "slug": slug,
                "name": name,
                "top_keywords": freq
            })

        # Тагове, които вероятно НЕ са автори
        if type_key == "author" and len(freq) > 0:
            if any(w in NOISE_WORDS for w, _ in freq[:5]):
                report["noise_candidates"].append({
                    "id": tag_id,
                    "slug": slug,
                    "name": name,
                    "reason": "HTML/технически шум в ключовите думи",
                    "top_keywords": freq
                })

        # Тагове, които вероятно СА автори (по структура на името)
        if type_key == "unknown":
            if len(name.split()) in (2, 3) and name[0].isupper():
                report["potential_authors"].append({
                    "id": tag_id,
                    "slug": slug,
                    "name": name,
                    "reason": "Име с 2–3 думи, вероятно автор",
                    "top_keywords": freq
                })

        # Обобщение
        report["tag_summaries"].append({
            "id": tag_id,
            "slug": slug,
            "name": name,
            "type_key": type_key,
            "top_keywords": freq
        })

    # Запис
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    print(f"Готово! Създаден е semantic_report.json")
    print(f" - Unknown tags: {len(report['unknown_tags'])}")
    print(f" - Potential authors: {len(report['potential_authors'])}")
    print(f" - Duplicate authors: {len(report['duplicate_authors'])}")
    print(f" - Noise candidates: {len(report['noise_candidates'])}")


if __name__ == "__main__":
    main()