import json

INPUT_FILE = "database/json/tags_classified.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def looks_like_author(name):
    """Открива имена, които приличат на автори, но не са в правилния формат."""
    parts = name.split()

    # Име + фамилия + още нещо → вероятен псевдоним
    if len(parts) >= 3:
        return True

    # Смесена кирилица + латиница → вероятен псевдоним
    has_cyr = any("а" <= ch <= "я" or "А" <= ch <= "Я" for ch in name)
    has_lat = any("a" <= ch.lower() <= "z" for ch in name)
    if has_cyr and has_lat:
        return True

    return False

def main():
    tags = load_json(INPUT_FILE)

    print("\n=== Тагове, които вероятно са автори с псевдоним, но НЕ са в правилния формат ===\n")

    for tag in tags:
        name = tag["name"]
        type_key = tag["type_key"]

        # 1) Автор, но не в синтаксиса "Име Фамилия - Псевдоним"
        if type_key == "author" and " - " not in name:
            print(f"[AUTHOR WRONG FORMAT] {name}")
            continue

        # 2) Не е автор, но прилича на автор с псевдоним
        if type_key != "author" and looks_like_author(name):
            print(f"[LIKELY AUTHOR] {name}  --> classified as {type_key}")

    print("\nГотово.\n")

if __name__ == "__main__":
    main()