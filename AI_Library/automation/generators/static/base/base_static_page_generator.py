"""
StaticPageGenerator (v1.0 — архитектурна версия)

Този модул съдържа основната архитектура за генериране на статични авторски страници.
Това е първата реална версия на генератора — минимално работеща, без зависимост от
конкретни шаблони или реални пътища. Тя ще бъде разширена във v2.0 и v3.0.

Основни цели на StaticPageGenerator v1.0:

1) Да зарежда JSON данни за авторите.
2) Да подготвя контекст за шаблона.
3) Да рендерира шаблон чрез прост placeholder engine.
4) Да записва генерираната страница в изходна директория.
5) Да бъде напълно независим от реалната структура на сайта.
6) Да бъде лесно разширяем в следващите версии.

Тази версия е архитектурно ядро — без реални шаблони, без реални пътища.
"""

import os
import json
from typing import Dict, Any, Optional, List

from AI_Library.utils.logging import Logger


class StaticPageGenerator:
    """
    StaticPageGenerator v1.0 — минимално работещ генератор на статични страници.
    """

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        template_file: str,
        logger: Optional[Logger] = None,
    ):
        """
        :param input_dir: Директория с JSON файлове за авторите.
        :param output_dir: Директория, в която ще се записват статичните страници.
        :param template_file: Път до шаблона (PHP/HTML).
        :param logger: Централен логер.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.template_file = template_file
        self.logger = logger or Logger("StaticPageGenerator")

        os.makedirs(self.output_dir, exist_ok=True)

    # ---------------------------------------------------------
    # 1) Зареждане на JSON файл
    # ---------------------------------------------------------
    def load_json(self, path: str) -> Dict[str, Any]:
        self.logger.info(f"Зареждам JSON: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # 2) Зареждане на шаблон
    # ---------------------------------------------------------
    def load_template(self) -> str:
        self.logger.info(f"Зареждам шаблон: {self.template_file}")

        with open(self.template_file, "r", encoding="utf-8") as f:
            return f.read()

    # ---------------------------------------------------------
    # 3) Рендериране на шаблон (placeholder engine)
    # ---------------------------------------------------------
    def render_template(self, template: str, context: Dict[str, Any]) -> str:
        """
        Прост placeholder engine:
        {{key}} се заменя със стойността от context[key]
        """
        rendered = template
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
        return rendered

    # ---------------------------------------------------------
    # 4) Генериране на една страница
    # ---------------------------------------------------------
    def generate_page(self, author_data: Dict[str, Any]):
        slug = author_data.get("slug")
        if not slug:
            self.logger.error("Липсва slug в JSON данните — пропускам.")
            return

        output_path = os.path.join(self.output_dir, f"{slug}.php")

        template = self.load_template()
        content = self.render_template(template, author_data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"✔ Генерирана страница: {output_path}")

    # ---------------------------------------------------------
    # 5) Главен метод — обхожда всички JSON файлове
    # ---------------------------------------------------------
    def run(self):
        self.logger.info("Започвам генериране на статични страници...")

        for filename in os.listdir(self.input_dir):
            if not filename.endswith(".json"):
                continue

            json_path = os.path.join(self.input_dir, filename)
            author_data = self.load_json(json_path)

            self.generate_page(author_data)

        self.logger.info("Готово — всички статични страници са генерирани.")
