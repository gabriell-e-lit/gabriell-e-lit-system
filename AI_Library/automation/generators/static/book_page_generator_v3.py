# BookPageModel v3.0 – генератор на статична страница на книга

from dataclasses import asdict
from typing import Dict, Any
import pystache
import os

from system.models.book.BookPageModel_v3_0 import BookPageModel
from automation.generators.static.book_cell_renderer_v2 import BookCellRendererV2


class BookPageGeneratorV3:
    def __init__(self, template_path: str, book_cell_template_path: str):
        """
        template_path: book_template.php.mustache
        book_cell_template_path: book_cell.php.mustache
        """
        self.template_path = template_path
        self.book_cell_renderer = BookCellRendererV2(book_cell_template_path)

    def load_template(self) -> str:
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    def render_reviews(self, model: BookPageModel) -> list:
        """
        Превръща списъка от рецензии в Mustache-friendly структура
        """
        return [asdict(r) for r in model.reviews]

    def render(self, model: BookPageModel) -> str:
        template = self.load_template()

        context: Dict[str, Any] = asdict(model)
        context["reviews_rendered"] = self.render_reviews(model)

        return pystache.render(template, context)

    def save(self, model: BookPageModel, output_path: str):
        html = self.render(model)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
