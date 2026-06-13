"""
StaticPageGenerator v2.0 — реален генератор на статични авторски страници.

Разлики спрямо v1.0:
- Поддръжка на категории (publisher / gallery / guest_editor / library).
- Избор на шаблон според static_page_category.
- Поддръжка на loops ({{#books_publisher}} ... {{/books_publisher}}, {{#formats}}, {{#publications}}).
- Flatten на вложени структури (origin, sources, gallery).
- Поддръжка на fallback-и и пропускане на празни секции.
"""

import os
import json
from typing import Dict, Any, Optional, List

from AI_Library.utils.logging import Logger


CATEGORY_TEMPLATE_MAP = {
    "publisher": "publisher_template.php",
    "gallery_e_gallery": "gallery_template.php",
    "gallery_magazine": "gallery_template.php",
    "gallery_illustrator": "gallery_template.php",
    "guest_editor": "guest_editor_template.php",
    "library": "library_template.php",
}

CATEGORY_OUTPUT_DIR_MAP = {
    "publisher": "p-izdatelstvo/authors",
    "gallery_e_gallery": "e-gallery/authors/e-gallery",
    "gallery_magazine": "e-gallery/authors/magazine",
    "gallery_illustrator": "e-gallery/authors/illustrators",
    "guest_editor": "p-izdatelstvo/guest-editors",
    "library": "e-library/authors",
}


class StaticPageGeneratorV2:
    """
    StaticPageGenerator v2.0 — генератор на статични страници с категории и loops.
    """

    def __init__(
        self,
        input_dir: str,
        templates_dir: str,
        base_output_root: str,
        logger: Optional[Logger] = None,
    ):
        """
        :param input_dir: Директория с JSON файлове за авторите.
        :param templates_dir: Директория с PHP шаблони.
        :param base_output_root: Коренова директория за изходните PHP файлове.
        :param logger: Централен логер.
        """
        self.input_dir = input_dir
        self.templates_dir = templates_dir
        self.base_output_root = base_output_root
        self.logger = logger or Logger("StaticPageGeneratorV2")

    # ---------------------------------------------------------
    # 1) Зареждане на JSON файл
    # ---------------------------------------------------------
    def load_json(self, path: str) -> Dict[str, Any]:
        self.logger.info(f"Зареждам JSON: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # 2) Избор на шаблон според категория
    # ---------------------------------------------------------
    def select_template_file(self, author_data: Dict[str, Any]) -> Optional[str]:
        category = author_data.get("static_page_category", "").strip()
        if not category:
            self.logger.warning("Липсва static_page_category — няма да генерирам страница.")
            return None

        template_name = CATEGORY_TEMPLATE_MAP.get(category)
        if not template_name:
            self.logger.warning(f"Непозната категория '{category}' — няма шаблон.")
            return None

        template_path = os.path.join(self.templates_dir, template_name)
        if not os.path.isfile(template_path):
            self.logger.error(f"Шаблонът не съществува: {template_path}")
            return None

        return template_path

    # ---------------------------------------------------------
    # 3) Зареждане на шаблон
    # ---------------------------------------------------------
    def load_template(self, template_path: str) -> str:
        self.logger.info(f"Зареждам шаблон: {template_path}")
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    # ---------------------------------------------------------
    # 4) Flatten на вложени структури към context
    # ---------------------------------------------------------
    def build_context(self, author_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Превръща AuthorModel_v4.2 в плосък context за шаблона.
        """
        ctx: Dict[str, Any] = {}

        # Основни полета
        ctx["name"] = author_data.get("name", "")
        ctx["slug"] = author_data.get("slug", "")
        ctx["biography"] = author_data.get("biography", "")
        ctx["photo"] = author_data.get("photo", "")
        ctx["photo_alt"] = author_data.get("photo_alt", "")

        # Origin
        origin = author_data.get("origin", {})
        ctx["origin_country"] = origin.get("country", "")
        ctx["origin_city"] = origin.get("city", "")
        ctx["origin_birth"] = origin.get("year_of_birth", "")
        ctx["origin_death"] = origin.get("year_of_death", "")

        # Sources
        sources = author_data.get("sources", {})
        ctx["tag_page"] = sources.get("tag_page", "")
        ctx["wikipedia"] = sources.get("wikipedia", "")
        ctx["static_page"] = sources.get("static_page", "")

        # Gallery
        gallery = author_data.get("gallery", {})
        ctx["gallery_subcategory"] = gallery.get("subcategory", "")
        ctx["gallery_url"] = gallery.get("url", "")

        # Roles
        ctx["roles"] = author_data.get("roles", [])

        # Books & publications — оставяме ги като списъци, за да ги обработим през loops
        ctx["books_publisher"] = author_data.get("books_publisher", [])
        ctx["books_library"] = author_data.get("books_library", [])
        ctx["publications"] = author_data.get("publications", [])

        return ctx

    # ---------------------------------------------------------
    # 5) Прост template engine с loops и прости променливи
    # ---------------------------------------------------------
    def render_template(self, template: str, context: Dict[str, Any]) -> str:
        """
        Поддържа:
        - {{key}} → context[key]
        - {{#list}} ... {{/list}} → повторение за всеки елемент
        - вложени {{field}} вътре в loops
        """
        rendered = template

        # 5.1. Обработка на loops
        rendered = self._render_loops(rendered, context)

        # 5.2. Обработка на прости променливи
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                continue
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))

        return rendered

    def _render_loops(self, template: str, context: Dict[str, Any]) -> str:
        """
        Намира блокове от вида {{#key}} ... {{/key}} и ги рендерира
        според context[key], ако е списък.
        """
        rendered = template

        # Списъци, които очакваме да имат loops
        loop_keys = ["books_publisher", "books_library", "publications", "formats"]

        for key in loop_keys:
            start_tag = f"{{{{#{key}}}}}"
            end_tag = f"{{{{/{key}}}}}"

            while start_tag in rendered and end_tag in rendered:
                start_idx = rendered.index(start_tag)
                end_idx = rendered.index(end_tag, start_idx)
                block = rendered[start_idx + len(start_tag):end_idx]

                items = context.get(key, [])
                if not isinstance(items, list) or len(items) == 0:
                    # Ако няма елементи → премахваме целия блок
                    rendered = rendered[:start_idx] + rendered[end_idx + len(end_tag):]
                    break

                # Рендерираме блок за всеки елемент
                repeated = []
                for item in items:
                    item_block = block
                    if isinstance(item, dict):
                        for sub_key, sub_val in item.items():
                            sub_placeholder = f"{{{{{sub_key}}}}}"
                            item_block = item_block.replace(sub_placeholder, str(sub_val))
                    else:
                        # Ако е прост тип, използваме {{value}}
                        item_block = item_block.replace("{{value}}", str(item))
                    repeated.append(item_block)

                rendered = rendered[:start_idx] + "".join(repeated) + rendered[end_idx + len(end_tag):]

        return rendered

    # ---------------------------------------------------------
    # 6) Определяне на изходен път според категория + page_filename
    # ---------------------------------------------------------
    def get_output_path(self, author_data: Dict[str, Any]) -> Optional[str]:
        category = author_data.get("static_page_category", "").strip()
        slug = author_data.get("slug", "").strip()
        page_filename = author_data.get("page_filename", "").strip()

        if not category or not slug or not page_filename:
            self.logger.error("Липсват category/slug/page_filename — не мога да определя изходен път.")
            return None

        rel_dir = CATEGORY_OUTPUT_DIR_MAP.get(category)
        if not rel_dir:
            self.logger.error(f"Непозната категория '{category}' — няма директория.")
            return None

        output_dir = os.path.join(self.base_output_root, rel_dir)
        os.makedirs(output_dir, exist_ok=True)

        return os.path.join(output_dir, page_filename)

    # ---------------------------------------------------------
    # 7) Генериране на една страница
    # ---------------------------------------------------------
    def generate_page(self, author_data: Dict[str, Any]):
        if not author_data.get("static_page_required", False):
            self.logger.info(f"Автор '{author_data.get('name', '')}' няма статична страница — пропускам.")
            return

        template_path = self.select_template_file(author_data)
        if not template_path:
            return

        output_path = self.get_output_path(author_data)
        if not output_path:
            return

        template = self.load_template(template_path)
        context = self.build_context(author_data)
        content = self.render_template(template, context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"✔ Генерирана страница: {output_path}")

    # ---------------------------------------------------------
    # 8) Главен метод — обхожда всички JSON файлове
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("Започвам генериране на статични страници (v2.0)...")

        for filename in os.listdir(self.input_dir):
            if not filename.endswith(".json"):
                continue

            json_path = os.path.join(self.input_dir, filename)
            author_data = self.load_json(json_path)

            self.generate_page(author_data)

        self.logger.info("Готово — всички статични страници (v2.0) са генерирани.")
        
if __name__ == "__main__":
    input_dir = r"C:\Users\gabri\OneDrive\Desktop\gabriell-e-lit-system\AI_Library\system\data\authors"
    templates_dir = r"C:\Users\gabri\OneDrive\Desktop\gabriell-e-lit-system\AI_Library\automation\generators\static\templates"
    base_output_root = r"C:\Users\gabri\OneDrive\Desktop\gabriell-e-lit-system"

    generator = StaticPageGeneratorV2(
        input_dir=input_dir,
        templates_dir=templates_dir,
        base_output_root=base_output_root
    )

    generator.run()
