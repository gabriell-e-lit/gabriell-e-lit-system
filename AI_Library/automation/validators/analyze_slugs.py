import json
import re
import os

# Път към локалния JSON с тагове
TAGS_FILE = "database/json/tags.json"

# Зареждаме всички тагове
with open(TAGS_FILE, "r", encoding="utf-8") as f:
    tags = json.load(f)

print("Анализирам slug-овете...\n")

invalid_slugs = []
duplicate_slugs = []
seen = set()

slug_pattern = re.compile(r"^[a-z0-9\-]+$")  # само латиница, цифри и тирета

for tag in tags:
    name = tag.get("name", "")
    slug = tag.get("slug", "")

    # Проверка за дублиране
    if slug in seen:
        duplicate_slugs.append((name, slug))
    else:
        seen.add(slug)

    # Проверка за валидност
    if not slug_pattern.match(slug):
        invalid_slugs.append((name, slug))

# Резултати
print("=== Невалидни slug-ове (не са нормализирани) ===")
if invalid_slugs:
    for name, slug in invalid_slugs:
        print(f"- {name} → {slug}")
else:
    print("Няма невалидни slug-ове.")

print("\n=== Дублирани slug-ове ===")
if duplicate_slugs:
    for name, slug in duplicate_slugs:
        print(f"- {name} → {slug}")
else:
    print("Няма дублирани slug-ове.")

print("\nАнализът е завършен.")