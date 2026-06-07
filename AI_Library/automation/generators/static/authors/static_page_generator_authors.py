"""
StaticPageGeneratorAuthors (v1.0)

Генератор на статични страници за автори.
Тази версия наследява базовия генератор и добавя специфичен контекст за автори.

Основни цели на StaticPageGeneratorAuthors v1.0:

1) Да зарежда JSON данни за автори.
2) Да подготвя контекст, специфичен за авторски страници.
3) Да използва шаблон за автори.
4) Да генерира статични PHP страници за всеки автор.
5) Да бъде напълно независим от WordPress и реалната структура на сайта.
6) Да бъде разширяем във v2.0 (canonical списъци, снимки, биографии, линкове).

Тази версия е архитектурна — минимално работеща, но чиста и готова за надграждане.
"""

import os
from typing import Dict, Any, Optional

from AI_Library.utils.logging import Logger
from AI_Library.automation.generators.static.base.base_static_page_generator import (
    BaseStaticPageGenerator,
)


class StaticPageGeneratorAuthors(BaseStaticPageGenerator):
    """
    Генератор на статични страници за автори.
    """

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        template_file: str,
        logger: Optional[Logger] = None,
    ):
        super().__init__(input_dir, output_dir, template_file, logger or Logger("StaticPageGeneratorAuthors"))

    # ---------------------------------------------------------
    # 1) Подготовка на контекст за автори
    # ---------------------------------------------------------
    def prepare_context(self, author_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подготвя контекст за шаблона на автори.
        Тук можем да добавяме специфични полета за автори.
        """
        context = {
            "name": author_data.get("name", ""),
            "slug": author_data.get("slug", ""),
            "bio": author_data.get("bio", ""),
            "photo": author_data.get("photo", ""),
            "links": author_data.get("links", []),
        }

        # Място за бъдещи разширения:
        # - списък с книги
        # - Wikipedia
        # - социални мрежи
        # - преводи
        # - награди

        return context

    # ---------------------------------------------------------
    # 2) Генериране на страница за автор
    # ---------------------------------------------------------
    def generate_page(self, author_data: Dict[str, Any]):
        slug = author_data.get("slug")
        if not slug:
            self.logger.error("Липсва slug в JSON данните — пропускам автор.")
            return

        output_path = os.path.join(self.output_dir, f"{slug}.php")

        template = self.load_template()
        context = self.prepare_context(author_data)
        content = self.render_template(template, context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"✔ Генерирана авторска страница: {output_path}")

    # ---------------------------------------------------------
    # 3) Главен метод — обхожда всички JSON файлове
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("Започвам генериране на статични страници за автори...")

        for filename in os.listdir(self.input_dir):
            if not filename.endswith(".json"):
                continue

            json_path = os.path.join(self.input_dir, filename)
            author_data = self.load_json(json_path)

            self.generate_page(author_data)

        self.logger.info("Готово — всички авторски страници са генерирани.")
