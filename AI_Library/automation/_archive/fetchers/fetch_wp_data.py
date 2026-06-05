import requests
import json
import os

BASE_URL = "https://gabriell-e-lit.com/izdatelstvo/wp-json/wp/v2"
OUTPUT_DIR = "database/json"

def fetch_all(endpoint, per_page=100):
    """Изтегля всички страници от даден WP endpoint (категории, страници и др.)."""
    results = []
    page = 1

    while True:
        url = f"{BASE_URL}/{endpoint}?per_page={per_page}&page={page}"
        print(f"Изтеглям: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Грешка при заявката: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        results.extend(data)
        page += 1

    return results


def save_json(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Записано: {path}")


def main():
    print("=== Изтегляне на категории ===")
    categories = fetch_all("categories")
    save_json(categories, "categories.json")

    print("=== Изтегляне на страници ===")
    pages = fetch_all("pages")
    save_json(pages, "pages.json")

    print("Готово. Всички данни са изтеглени.")


if __name__ == "__main__":
    main()