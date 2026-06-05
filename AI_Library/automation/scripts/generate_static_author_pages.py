import os
import shutil
import json
import re

# ============================
# 1) ПЪТИЩА ДО JSON ДИРЕКТОРИИТЕ
# ============================

JSON_DIRS = {
    "publisher": "/home/gabriell/public_html/p-izdatelstvo/data/authors",
    "guest_editors": "/home/gabriell/public_html/spisanie/data/gost-redaktori",
    "guest_editors_science": "/home/gabriell/public_html/spisanie/data/gost-redaktori/nauka",
    "e_library": "/home/gabriell/public_html/subdomains/e-library/data/authors",
    "e_gallery": "/home/gabriell/public_html/subdomains/e-gallery/data/authors/e-gallery",
    "e_gallery_illustrators": "/home/gabriell/public_html/subdomains/e-gallery/data/authors/gabriell-e-lit",
    "e_gallery_magazine": "/home/gabriell/public_html/subdomains/e-gallery/data/authors/kartini-s-dumi-i-bagri"
}

# ============================
# 2) ПЪТИЩА ДО СТАТИЧНИТЕ PHP ДИРЕКТОРИИ
# ============================

OUTPUT_DIRS = {
    "publisher": "/home/gabriell/public_html/p-izdatelstvo/authors",
    "guest_editors": "/home/gabriell/public_html/spisanie/gost-redaktori",
    "guest_editors_science": "/home/gabriell/public_html/spisanie/gost-redaktori/nauka",
    "e_library": "/home/gabriell/public_html/subdomains/e-library/authors",
    "e_gallery": "/home/gabriell/public_html/subdomains/e-gallery/authors/e-gallery",
    "e_gallery_illustrators": "/home/gabriell/public_html/subdomains/e-gallery/authors/gabriell-e-lit",
    "e_gallery_magazine": "/home/gabriell/public_html/subdomains/e-gallery/authors/kartini-s-dumi-i-bagri"
}

# ============================
# 3) ПЪТ ДО PHP ШАБЛОНА
# ============================

TEMPLATE_FILE = "templates/author_template.php"

# ============================
# 4) ФУНКЦИЯ ЗА СЪЗДАВАНЕ НА PHP ФАЙЛ
# ============================

def generate_page(json_path, output_dir):
    slug = os.path.splitext(os.path.basename(json_path))[0]
    output_file = os.path.join(output_dir, f"{slug}.php")

    # Копираме шаблона
    shutil.copy(TEMPLATE_FILE, output_file)

    print(f"✔ Създадена страница: {output_file}")

# ============================
# 5) ГЕНЕРИРАНЕ НА СТРАНИЦИ ЗА ВСЯКА ГРУПА
# ============================

for group, json_dir in JSON_DIRS.items():
    output_dir = OUTPUT_DIRS[group]

    print(f"\n=== Група: {group} ===")
    print(f"JSON директория: {json_dir}")
    print(f"PHP директория: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(json_dir, filename)
            generate_page(json_path, output_dir)

print("\nГотово! Всички статични страници са генерирани.")
