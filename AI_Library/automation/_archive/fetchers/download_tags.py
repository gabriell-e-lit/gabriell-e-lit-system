import json
import os
import requests

CONFIG_FILE = "config.json"
OUTPUT_FILE = "database/json/tags.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_all_tags(api_url, auth):
    tags = []
    page = 1

    while True:
        url = f"{api_url}/tags?per_page=100&page={page}"
        response = requests.get(url, auth=auth)

        if response.status_code == 400:
            break

        response.raise_for_status()
        batch = response.json()

        if not batch:
            break

        tags.extend(batch)
        page += 1

    return tags

def main():
    config = load_config()
    api_url = config["api_url"]
    username = config["username"]
    app_password = config["app_password"]

    auth = (username, app_password)

    print("Свалям таговете...")
    tags = fetch_all_tags(api_url, auth)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=4)

    print(f"Готово. Свалени са {len(tags)} тага.")
    print(f"Записани в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()