import re
from bs4 import BeautifulSoup
import json

INPUT_HTML = "authors_page.html"
OUTPUT_JSON = "database/json/authors_raw_v3.json"

# --- Помощни функции ---

def clean_text(t):
    if not t:
        return ""
    return re.sub(r"\s+", " ", t).strip()

def is_name_like(text):
    """
    Проверява дали текстът прилича на лично име:
    - 2 или 3 думи
    - започват с главна буква
    - без цифри
    - без ключови думи като 'автори', 'през', 'издателството'
    """
    if not text:
        return False

    t = text.strip()

    # филтрираме очевидни секционни заглавия
    if re.search(r"(автори|през\s*20\d{2}|издателството|стават|биографии)", t, re.IGNORECASE):
        return False

    words = t.split()
    if len(words) < 2 or len(words) > 3:
        return False

    for w in words:
        if not re.match(r"^[A-ZА-Я][a-zа-я]+$", w):
            return False

    return True

def extract_bio_before(element):
    """
    Взима първия <p> ПРЕДИ даденото <h2>.
    Това е правилната биография за структурата на страниците.
    """
    prev = element.find_previous_sibling()
    while prev:
        if prev.name == "p":
            return clean_text(prev.get_text())
        prev = prev.find_previous_sibling()
    return ""

def extract_bio_after(element):
    """
    Fallback: ако няма <p> преди <h2>, взимаме първия <p> след него.
    """
    nxt = element.find_next()
    while nxt:
        if nxt.name == "p":
            return clean_text(nxt.get_text())
        nxt = nxt.find_next()
    return ""

# --- Основна логика ---

def extract_authors(html):
    soup = BeautifulSoup(html, "html.parser")

    h2_list = soup.find_all("h2")
    if not h2_list:
        return []

    authors = []

    # Правило 1: пропускаме първото H2 (секционно заглавие)
    h2_list = h2_list[1:]

    for h2 in h2_list:
        h2_text = clean_text(h2.get_text())

        # Правило 2: H2 е водещ кандидат за име
        if not is_name_like(h2_text):
            continue

        final_name = h2_text

        # Правило 3: биографията е <p> ПРЕДИ <h2>
        bio = extract_bio_before(h2)

        # fallback: ако няма <p> преди <h2>, взимаме след него
        if not bio:
            bio = extract_bio_after(h2)

        authors.append({
            "name": final_name,
            "bio": bio
        })

    return authors

# --- Изпълнение ---

def main():
    with open(INPUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    authors = extract_authors(html)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

    print(f"Готово. Извлечени са {len(authors)} автори.")

if __name__ == "__main__":
    main()
