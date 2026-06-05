import json
import os
from collections import defaultdict

FIXES_FILE = "database/json/tag_fixes.json"
OUTPUT_FILE = "database/json/reclassify_groups.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"Липсва файл: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    fixes = load_json(FIXES_FILE)

    reclassify = {tid: t for tid, t in fixes.items() if t["suggested_action"] == "reclassify"}

    groups = defaultdict(list)
    stats = defaultdict(int)

    for tid, t in reclassify.items():
        key = f"{t['current_type']} → {t['suggested_type']}"
        groups[key].append({
            "id": tid,
            "slug": t["slug"],
            "name": t["name"]
        })
        stats[t["suggested_type"]] += 1

    # Записваме групите в JSON
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)

    # Печатаме статистика
    print("Групиране на reclassify тагове:")
    print("--------------------------------")
    for suggested_type, count in stats.items():
        print(f"{suggested_type:12} : {count}")

    print("\nГрупите са записани в reclassify_groups.json")


if __name__ == "__main__":
    main()