import requests
from bs4 import BeautifulSoup
import json
import re
import os
from urllib.parse import urljoin, urlparse

MAIN_URL = "https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie-authors-spisanie/"
OUTPUT_BY_ISSUE = "database/json/authors_by_issue.json"
OUTPUT_RAW = "database/json/authors_raw.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"Грешка при сваляне на {url}: {e}")
        return None

def extract_slug_from_tag_url(url):
    """Взима slug от URL на авторския таг."""
    parts = urlparse(url).path.strip("/").split("/")
    if "tag" in parts:
        idx = parts.index("tag")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None

def normalize_name(name):
    """Премахва излишни интервали и HTML."""
    name = re.sub(r"\s+", " ", name).strip()
    return name

def choose_best_name(name_h2, name_bio, name_slug):
    """Правилото: ако две от трите съвпадат → това е името."""
    candidates = [name_h2, name_bio, name_slug]
    counts = {}

    for c in candidates:
        if c:
            counts[c] = counts.get(c, 0) + 1

    # Ако някое име се среща два пъти → това е правилното
    for name, count in counts.items():
        if count >= 2:
            return name

    # Иначе → взимаме името от slug
    return name_slug or name_h2 or name_bio

def extract_issue_id(url):
    """Вади issue_id от URL, напр. authors-1-2019 → 1-2019."""
    m = re.search(r"authors-(\d+-\d+)", url)
    return m.group(1) if m else None

def extract_first_issue(text):
    """Търси 'от брой X/година'."""
    m = re.search(r"от брой\s+(\d+\/\d+)", text)
    return m.group(1) if m else None

def extract_roles(text):
    roles = []
    if "редактор" in text.lower():
        roles.append("редактор")
    if "художник" in text.lower():
        roles.append("художник")
    if "поет" in text.lower():
        roles.append("поет")
    if "писател" in text.lower():
        roles.append("писател")
    if "преводач" in text.lower():
        roles.append("преводач")
    return roles

def parse_author_block(h2, block, issue_url):
    """Парсира един авторски блок."""
    name_h2 = normalize_name(h2.get_text())
    tag_url = h2.find("a")["href"] if h2.find("a") else None
    slug = extract_slug_from_tag_url(tag_url) if tag_url else None
    name_slug = slug.replace("-", " ").title() if slug else None

    # Снимка
    img = block.find("img")
    image_url = None
    if img:
        image_url = img.get("data-orig-file") or img.get("src")

    # Биография
    content = block.find("div", class_="wp-block-media-text__content")
    bio_text = ""
    if content:
        bio_text = " ".join([p.get_text(" ", strip=True) for p in content.find_all("p")])
    name_bio = None
    if content:
        strong = content.find("strong")
        if strong:
            name_bio = normalize_name(strong.get_text())

    # Първа поява
    first_issue = extract_first_issue(bio_text)

    # Роли
    roles = extract_roles(bio_text)

    # Issue ID
    issue_id = extract_issue_id(issue_url)

    # Избор на най-добро име
    final_name = choose_best_name(name_h2, name_bio, name_slug)

    return {
        "name": final_name,
        "slug": slug,
        "tag_url": tag_url,
        "image_url": image_url,
        "bio": bio_text,
        "first_issue": first_issue,
        "roles": roles,
        "issue_id": issue_id,
        "source_page": issue_url
    }

def extract_issue(url):
    html = fetch(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    authors = []

    h2_list = soup.find_all("h2", class_="wp-block-heading")

    for h2 in h2_list:
        block = h2.find_next("div", class_="wp-block-media-text")
        if block:
            authors.append(parse_author_block(h2, block, url))

    return authors

def main():
    print("Свалям главната страница…")
    html = fetch(MAIN_URL)
    if not html:
        print("Не мога да сваля главната страница.")
        return

    soup = BeautifulSoup(html, "html.parser")

    # Взимаме всички линкове към броеве
    issue_links = []
    for a in soup.find_all("a", href=True):
        if "authors-" in a["href"]:
            issue_links.append(urljoin(MAIN_URL, a["href"]))

    issue_links = list(sorted(set(issue_links)))

    print(f"Намерени {len(issue_links)} броя.")

    authors_by_issue = {}
    authors_raw = []

    for link in issue_links:
        print(f"Обработвам {link}…")
        issue_id = extract_issue_id(link)
        authors = extract_issue(link)
        authors_by_issue[issue_id] = [a["name"] for a in authors]
        authors_raw.extend(authors)

    os.makedirs(os.path.dirname(OUTPUT_BY_ISSUE), exist_ok=True)

    with open(OUTPUT_BY_ISSUE, "w", encoding="utf-8") as f:
        json.dump(authors_by_issue, f, ensure_ascii=False, indent=4)

    with open(OUTPUT_RAW, "w", encoding="utf-8") as f:
        json.dump(authors_raw, f, ensure_ascii=False, indent=4)

    print("Готово!")
    print(f"Създадени файлове:\n - {OUTPUT_BY_ISSUE}\n - {OUTPUT_RAW}")

if __name__ == "__main__":
    main()