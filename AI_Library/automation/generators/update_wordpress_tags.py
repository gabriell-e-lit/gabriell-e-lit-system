import requests
import json
import re

# -----------------------------------------
# НАСТРОЙКИ
# -----------------------------------------

WP_URL = "https://gabriell-e-lit.com/izdatelstvo/wp-json/wp/v2/tags"
WP_USER = "gabriell-e"
WP_PASS = "x8JS ZuvC XtwO N9o0 Jh6P sF3l"

INPUT_AUTHORS = "database/json/authors_v2.json"

DRY_RUN = False # <<< НАЙ-ВАЖНОТО — работещ режим
  # <<< НАЙ-ВАЖНОТО — безопасен режим


# -----------------------------------------
# ПОМОЩНИ ФУНКЦИИ
# -----------------------------------------

def find_images_in_html(html):
    """Открива <img> тагове в HTML."""
    if not html:
        return []
    return re.findall(r'<img[^>]+>', html, flags=re.IGNORECASE)


def normalize(s):
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9]+", "", s)
    return s

def get_tag_by_name(name):
    """Търси таг по име, slug и частично съвпадение."""
    search = name
    params = {"search": search}
    r = requests.get(WP_URL, params=params, auth=(WP_USER, WP_PASS), verify=False)

    if r.status_code != 200:
        print("❗ Грешка при заявка към WordPress:", r.status_code)
        return None

    data = r.json()
    if not data:
        print("❗ Няма резултати за:", name)
        return None

    norm_target = normalize(name)

    best = None
    best_score = 0

    for tag in data:
        tag_name = tag.get("name", "")
        tag_slug = tag.get("slug", "")

        norm_name = normalize(tag_name)
        norm_slug = normalize(tag_slug)

        score = 0

        if norm_name == norm_target:
            score += 100
        if norm_slug == norm_target:
            score += 100
        if norm_target in norm_name:
            score += 50
        if norm_target in norm_slug:
            score += 50

        if score > best_score:
            best_score = score
            best = tag

    if best:
        print(f"Намерих таг: {best['name']} (slug: {best['slug']})")
    else:
        print("❗ Не успях да избера най-добър таг.")

    return best

def update_tag(tag_id, new_description):
    payload = {"description": new_description}
    r = requests.post(f"{WP_URL}/{tag_id}", json=payload, auth=(WP_USER, WP_PASS), verify=False)
    return r.status_code, r.text

# -----------------------------------------
# ОСНОВНА ЛОГИКА
# -----------------------------------------

def main():
    print("Старт на update_wordpress_tags.py (DRY_RUN =", DRY_RUN, ")")

    with open(INPUT_AUTHORS, "r", encoding="utf-8") as f:
        authors = json.load(f)

    for a in authors:
        name = a["name"]
        new_bio = a.get("bio", "").strip()

        print("\n==============================================")
        print("Таг:", name)

        tag = get_tag_by_name(name)
        if not tag:
            print("❗ Тагът не е намерен в WordPress.")
            continue

        tag_id = tag["id"]
        old_description = tag.get("description", "")

        print("URL:", tag["link"])

        # --- СТАРО ОПИСАНИЕ ---
        print("\n--- СТАРО ОПИСАНИЕ ---")
        print(old_description if old_description else "(празно)")

        # --- НОВО ОПИСАНИЕ ---
        print("\n--- НОВО ОПИСАНИЕ ---")
        print(new_bio if new_bio else "(празно)")

        # --- СНИМКИ В СТАРОТО ОПИСАНИЕ ---
        images = find_images_in_html(old_description)
        print("\n--- СНИМКИ В СТАРОТО ОПИСАНИЕ ---")
        if images:
            print("Намерени <img> тагове:", len(images))
            for img in images:
                print(" ", img)
        else:
            print("Няма <img> тагове")

        # --- ЩЕ БЪДАТ ЛИ ПРЕМАХНАТИ? ---
        print("\n--- ЩЕ БЪДАТ ЛИ ПРЕМАХНАТИ? ---")
        if images:
            print("ДА — защото description ще бъде заменено изцяло.")
        else:
            print("Не — няма снимки в description.")

        # --- ДЕЙСТВИЕ ---
        print("\n--- ДЕЙСТВИЕ ---")
        if DRY_RUN:
            print("DRY RUN → Няма да се изпълни обновяване.")
        else:
            status, response = update_tag(tag_id, new_bio)
            print("Обновяване изпратено → статус:", status)
            print("Отговор:", response)


if __name__ == "__main__":
    main()