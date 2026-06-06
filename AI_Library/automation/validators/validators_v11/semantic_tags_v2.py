import json
import os
import re
from collections import Counter, defaultdict

MERGED_TAGS_FILE = "database/json/tags_merged.json"
POSTS_FILE = "database/json/posts.json"
OUTPUT_FILE = "database/json/semantic_report.json"

NOISE_WORDS = {
    "https", "http", "www", "com", "gabriell", "izdatelstvo",
    "uploads", "content", "wp", "image", "class", "figure",
    "attachment", "data", "block", "title", "width", "height",
    "src", "href", "alt", "img", "jpg", "jpeg", "png", "gif",
    "quot", "amp", "nbsp", "optimole"
}

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

def looks_like_genre_or_category(name, slug):
    genre_words = [
        "поезия", "проза", "есе", "визуални", "изкуства",
        "музика", "театър", "кино", "култура", "литература",
        "галерия", "критика", "събития", "новини"
    ]
    for w in genre_words:
        if w in name.lower() or w in slug.lower():
            return True
    return False

def looks_like_person(name):
    if len(name.split()) >= 2:
        return True
    if len(name.split()) == 1 and name[0].isupper():
        return True
    return False

def main():
    tags = load_json(MERGED_TAGS_FILE)
    posts = load_json(POSTS_FILE)

    tags_by_id = {t["id"]: t for t in tags}
    tag_text = defaultdict(str)

    for post in posts:
        title = post.get("title", {}).get("rendered", "")
        excerpt = post.get("excerpt", {}).get("rendered", "")
        content = post.get("content", {}).get("rendered", "")
        combined = clean_text(" ".join([title, excerpt, content]))

        for tag_id in post.get("tags", []):
            if tag_id in tags_by_id:
                tag_text[tag_id] += " " + combined

    report = {
        "misclassified_authors": [],
        "weak_authors": [],
        "duplicate_authors": [],
        "tag_summaries": []
    }

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

    for tag in tags:
        tag_id = tag["id"]
        slug = tag["slug"]
        name = tag["name"]
        type_key = tag["type_key"]

        text = tag_text[tag_id]
        keywords = extract_keywords(text)
        freq = Counter(keywords).most_common(15)

        if type_key == "author" and looks_like_genre_or_category(name, slug):
            report["misclassified_authors"].append({
                "id": tag_id,
                "slug": slug,
                "name": name,
                "reason": "Името прилича на жанр/категория",
                "top_keywords": freq
            })

        if type_key == "author" and not looks_like_person(name):
            report["weak_authors"].append({
                "id": tag_id,
                "slug": slug,
                "name": name,
                "reason": "Еднословно име, което не прилича на човек",
                "top_keywords": freq
            })

        report["tag_summaries"].append({
            "id": tag_id,
            "slug": slug,
            "name": name,
            "type_key": type_key,
            "top_keywords": freq
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    print("Готово! Създаден е semantic_report.json")
    print(f" - Misclassified authors: {len(report['misclassified_authors'])}")
    print(f" - Weak authors: {len(report['weak_authors'])}")
    print(f" - Duplicate authors: {len(report['duplicate_authors'])}")


if __name__ == "__main__":
    main()