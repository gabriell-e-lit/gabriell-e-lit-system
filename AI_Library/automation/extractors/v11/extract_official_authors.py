import requests
from bs4 import BeautifulSoup
import json
import os
import re

# ============================
# 1) URL-И НА СТРАНИЦИТЕ С АВТОРИ
# ============================

URLS = {
    "publisher": "https://gabriell-e-lit.com/izdatelstvo/gabriell-e-lit/authors-gabriell-e-lit/",
    "e_library": "https://gabriell-e-lit.com/izdatelstvo/authors-e-library-gabriell-e-lit/",
    "e_gallery": "https://gabriell-e-lit.com/izdatelstvo/artists-e-gallery-gabriell-e-lit/",
    "guest_editors": "https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/ekip-spisanie/gost-redaktori/",
    "guest_editors_science": "https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/ekip-spisanie/gost-redaktori-razdel-nauka/"
}

# ============================
# 2) ДИРЕКТОРИИ ЗА JSON ФАЙЛОВЕ
# ============================

OUTPUT_DIRS = {
    "publisher": "/home/gabriell/public_html/p-izdatelstvo/data/authors",
    "guest_editors": "/home/gabriell/public_html/spisanie/data/gost-redaktori",
    "guest_editors_science": "/home/gabriell/public_html/spisanie/data/gost-redaktori/nauka",
    "e_library": "/home/gabriell/public_html/subdomains/e-library/data/authors",
    "e_gallery": "/home/gabriell/public_html/subdomains/e-gallery/data/authors/e-gallery",
    "e_gallery_illustrators": "/home/gabriell/public_html/subdomains/e-gallery/data/authors/gabriell-e-lit",
    "e_gallery_magazine": "/home/gabriell/public_html/subdomains/e-gallery/data/authors/kartini-s-dumi-i-bagri"
}

for path in OUTPUT_DIRS.values():
    os.makedirs(path, exist_ok=True)

# ============================
# 3) ФУНКЦИЯ ЗА СЪЗДАВАНЕ НА SLUG
# ============================

def make_slug(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")

# ============================
# 4) ИЗВЛИЧАНЕ НА ИМЕНА + ГРУПИ ОТ СТРАНИЦА
# ============================

def extract_names(url: str):
    print(f"Извличам: {url}")
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    results = []
    current_group = None

    # Основна логика: H2 = група, H3 = име
    for tag in soup.find_all(["h2", "h3"]):
        if tag.name == "h2":
            text = tag.get_text(strip=True)
            if text:
                current_group = text
        elif tag.name == "h3":
            name = tag.get_text(strip=True)
            if name and len(name.split()) >= 2:
                results.append({
                    "name": name,
                    "group": current_group
                })

    # Fallback: ако няма нито един H3, приемаме H2 за имена (без група)
    if not results:
        for h2 in soup.find_all("h2"):
            name = h2.get_text(strip=True)
            if name and len(name.split()) >= 2:
                results.append({
                    "name": name,
                    "group": None
                })

    return results

# ============================
# 5) ЗАРЕЖДАНЕ НА ГОЛЕМИЯ JSON
# ============================

with open("database/json/authors_final.json", "r", encoding="utf-8") as f:
    big_json = json.load(f)

authors_by_name = {a["name"]: a for a in big_json}

# ============================
# 6) ОБРАБОТКА НА ВСЯКА ГРУПА
# ============================

def save_group(group_key: str, items, output_dir: str):
    for item in items:
        name = item["name"]
        group = item["group"]

        if name not in authors_by_name:
            print(f"⚠ Пропуснат (не е в големия JSON): {name}")
            continue

        # Копираме данните от големия JSON
        data = dict(authors_by_name[name])

        # По желание добавяме групата (ако има)
        if group:
            data["group"] = group

        slug = make_slug(name)
        output_path = os.path.join(output_dir, f"{slug}.json")

        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, indent=4)

        print(f"✔ Създаден JSON: {output_path}")

# ============================
# 7) ИЗВЛИЧАНЕ И ЗАПИС
# ============================

publisher_items = extract_names(URLS["publisher"])
e_library_items = extract_names(URLS["e_library"])
e_gallery_items = extract_names(URLS["e_gallery"])
guest_editors_items = extract_names(URLS["guest_editors"])
guest_editors_science_items = extract_names(URLS["guest_editors_science"])

save_group("publisher", publisher_items, OUTPUT_DIRS["publisher"])
save_group("e_library", e_library_items, OUTPUT_DIRS["e_library"])
save_group("e_gallery", e_gallery_items, OUTPUT_DIRS["e_gallery"])
save_group("guest_editors", guest_editors_items, OUTPUT_DIRS["guest_editors"])
save_group("guest_editors_science", guest_editors_science_items, OUTPUT_DIRS["guest_editors_science"])

print("\nГотово! Всички JSON файлове са създадени.")

