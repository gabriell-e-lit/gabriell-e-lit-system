import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v10.json"


def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()


def normalize_name(name):
    """Нормализиране за сравнение."""
    name = name.lower()
    name = re.sub(r"[^a-zа-яёіїєґ0-9]+", "", name)
    return name


def extract_bio(content_div):
    """Събира всички <p> вътре в блока с биографията."""
    if not content_div:
        return ""
    paragraphs = content_div.find_all("p")
    bio_parts = [clean_text(p.get_text()) for p in paragraphs if clean_text(p.get_text())]
    return "\n\n".join(bio_parts)


def extract_authors(html):
    soup = BeautifulSoup(html, "html.parser")

    # 1) Всички H2 заглавия (автори)
    h2_list = soup.find_all("h2", class_="wp-block-heading")

    # Пропускаме първото H2 (заглавие на страницата)
    if h2_list:
        h2_list = h2_list[1:]

    authors = []
    name_map = {}

    # Създаваме речник: нормализирано име → {оригинално име, h2 елемент}
    for h2 in h2_list:
        name = clean_text(h2.get_text())
        norm = normalize_name(name)
        name_map[norm] = {
            "name": name,
            "h2": h2
        }
        authors.append({"name": name, "bio": ""})

    # 2) Биографични блокове (всички media-text)
    bio_blocks = soup.find_all("div", class_="wp-block-media-text__content")

    # За да знаем кои блокове вече са сдвоени
    matched_blocks = set()

    # --- ПЪРВИ ПРОХОД: СДВОЯВАНЕ ПО ИМЕ ---
    for idx, content_div in enumerate(bio_blocks):
        strong = content_div.find("strong")
        if not strong:
            continue

        bio_name = clean_text(strong.get_text())
        norm_bio_name = normalize_name(bio_name)

        if norm_bio_name in name_map:
            target_name = name_map[norm_bio_name]["name"]

            for a in authors:
                if a["name"] == target_name and not a["bio"]:
                    a["bio"] = extract_bio(content_div)
                    matched_blocks.add(idx)
                    break

    # --- ВТОРИ ПРОХОД: FALLBACK ПО ПОЗИЦИЯ ---
    for idx, content_div in enumerate(bio_blocks):
        if idx in matched_blocks:
            continue  # вече сдвоен по име

        prev_h2 = content_div.find_previous("h2", class_="wp-block-heading")
        if not prev_h2:
            continue

        prev_name = clean_text(prev_h2.get_text())

        for a in authors:
            if a["name"] == prev_name and not a["bio"]:
                a["bio"] = extract_bio(content_div)
                break

    return authors


def main():
    print("Старт на extract_authors_v10...")

    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    authors = extract_authors(html)
    print(f"Извлечени автори: {len(authors)}")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Записано в {OUTPUT_JSON}")


if __name__ == "__main__":
    main()