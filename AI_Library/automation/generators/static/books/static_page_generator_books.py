"""
StaticPageGeneratorBooks (v1.0 — skeleton)

Този модул е архитектурният скелет на генератора за статични страници на книги.
Той наследява базовия генератор и подготвя структурата за бъдещата реална логика.

Основни цели на StaticPageGeneratorBooks v1.0:

1) Да дефинира мястото на генератора за книги в архитектурата.
2) Да наследи BaseStaticPageGenerator.
3) Да предостави празни методи за prepare_context() и generate_page().
4) Да бъде готов за разширяване във v2.0, когато започнем реалната работа по книгите.
5) Да бъде паралелен на StaticPageGeneratorAuthors, но без да дублира логика.

Тази версия е само скелет — без реална логика, без обработка на JSON, без шаблони.
"""

import os
from typing import Dict, Any, Optional

from AI_Library.utils.logging import Logger
from AI_Library.automation.generators.static.base.base_static_page_generator import (
    BaseStaticPageGenerator,
)


class StaticPageGeneratorBooks(BaseStaticPageGenerator):
    """
    Генератор на статични страници за книги (skeleton).
    Реалната логика ще бъде добавена във v2.0.
    """

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        template_file: str,
        logger: Optional[Logger] = None,
    ):
        super().__init__(input_dir, output_dir, template_file, logger or Logger("StaticPageGeneratorBooks"))

    # ---------------------------------------------------------
    # 1) Подготовка на контекст за книги (skeleton)
    # ---------------------------------------------------------
    def prepare_context(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Празен метод — ще бъде реализиран във v2.0.
        Тук ще подготвяме контекст за шаблона на книги.
        """
        return {}

    # ---------------------------------------------------------
    # 2) Генериране на страница за книга (skeleton)
    # ---------------------------------------------------------
    def generate_page(self, book_data: Dict[str, Any]):
        """
        Празен метод — ще бъде реализиран във v2.0.
        Тук ще генерираме статична страница за книга.
        """
        slug = book_data.get("slug")
        if not slug:
            self.logger.error("Липсва slug в JSON данните за книга — пропускам.")
            return

        output_path = os.path.join(self.output_dir, f"{slug}.php")

        # Реалната логика ще бъде добавена във v2.0
        self.logger.info(f"(skeleton) Генериране на страница за книга: {output_path}")

    # ---------------------------------------------------------
    # 3) Главен метод — обхожда JSON файловете (skeleton)
    # ---------------------------------------------------------
    def run(self):
        """
        Празен метод — ще бъде реализиран във v2.0.
        """
        self.logger.info("StaticPageGeneratorBooks (skeleton) — няма реална логика.")
