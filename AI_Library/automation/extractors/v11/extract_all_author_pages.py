import requests
from bs4 import BeautifulSoup
import json
import re
import time

BASE = "https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie-authors-spisanie"

OUTPUT_RAW = "database/json/authors_raw.json"
OUTPUT_FINAL = "database/json/authors_final.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def url_exists(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.status_code == 200
    except:
        return False


def extract_authors_from_page(url):
    print(f"Обработвам: {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        print("❗ Грешка при зареждане")
        return []

    content = soup.find("div", class_="entry-content")
    if not content:
        print("❗ Няма entry-content")
        return []

    authors = []

    blocks = content.find_all(["h2", "h3"])
    for h in blocks:
        name = h.get_text(strip=True)
        if not name:
            continue

        # следващият <p> е биографията
        p = h.find_next_sibling("p")
        bio = p.get_text(strip=True) if p else ""

        authors.append({
            "name": name,
            "bio": bio,
            "source_page": url
        })

    return authors


def normalize_author(a):
    """Премахва дубли, чисти текст, нормализира."""
    a["name"] = re.sub(r"\s+", " ", a["name"]).strip()
    a["bio"] = re.sub(r"\s+", " ", a["bio"]).strip()
    return a


def main():
    print("Старт на extract_all_author_pages.py")

    # -----------------------------------------
    # 1) Генерираме URL‑и по формула
    # -----------------------------------------

    all_authors = []

    # 2018 – само authors-0-2018/
    year = 2018
    url = f"{BASE}/authors-0-{year}/"
    all_authors.extend(extract_authors_from_page(url))

    # 2019 – authors-1-2019/ до authors-4-2019/
    year = 2019
    for season in range(1, 5):
        url = f"{BASE}/authors-{season}-{year}/"
        all_authors.extend(extract_authors_from_page(url))

    # 2020–2025 – authors-1..4-year-global_index
    for year in range(2020, 2026):
        base_index = 6 + (year - 2020) * 4
        for season in range(1, 5):
            global_index = base_index + (season - 1)
            url = f"{BASE}/authors-{season}-{year}-{global_index}/"
            all_authors.extend(extract_authors_from_page(url))
            time.sleep(0.5)

    # 2026 – засега имаме само 1 и 2 (30, 31)
    year = 2026
    base_index = 6 + (year - 2020) * 4  # дава 30
    for season in range(1, 3):  # 1, 2
        global_index = base_index + (season - 1)  # 30, 31
        url = f"{BASE}/authors-{season}-{year}-{global_index}/"
        all_authors.extend(extract_authors_from_page(url))
        time.sleep(0.5)

    # -----------------------------------------
    # 2) Записваме RAW
    # -----------------------------------------

    with open(OUTPUT_RAW, "w", encoding="utf-8") as f:
        json.dump(all_authors, f, ensure_ascii=False, indent=4)

    print(f"\nЗаписано RAW: {OUTPUT_RAW}")

    # -----------------------------------------
    # 3) Нормализираме и премахваме дубли
    # -----------------------------------------

    final = {}
    for a in all_authors:
        a = normalize_author(a)
        key = a["name"].lower()
        if key not in final:
            final[key] = a
        else:
            # ако има по-дълга биография → взимаме нея
            if len(a["bio"]) > len(final[key]["bio"]):
                final[key] = a

    final_list = list(final.values())

    with open(OUTPUT_FINAL, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано FINAL: {OUTPUT_FINAL}")


if __name__ == "__main__":
    main()