import requests
import json
import os

# Базовият URL на твоя WordPress (в поддиректория /izdatelstvo/)
BASE_URL = "https://gabriell-e-lit.com/izdatelstvo/wp-json/wp/v2/tags"

# Къде да запишем суровите WordPress тагове
OUTPUT_FILE = "database/json/tags_wp.json"

def fetch_all_tags():
    tags = []
    page = 1

    while True:
        url = f"{BASE_URL}?per_page=100&page={page}"
        print(f"Изтеглям: {url}")

        response = requests.get(url, timeout=20)

        if response.status_code == 400:
            # Няма повече страници
            break

        if response.status_code != 200:
            print(f"Грешка {response.status_code}: {response.text}")
            break

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            break

        tags.extend(data)
        page += 1

    return tags


def main():
    print("Започвам изтегляне на тагове от WordPress…")

    tags = fetch_all_tags()

    print(f"Общо изтеглени тагове: {len(tags)}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=4)

    print(f"Готово! Записано в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()