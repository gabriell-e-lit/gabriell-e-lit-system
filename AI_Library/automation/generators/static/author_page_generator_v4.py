# AuthorPageModel v4.3 – генератор на статична авторска страница

from dataclasses import asdict
from typing import Dict, Any
import pystache
import os

from system.models.author.AuthorPageModel_v4_3 import AuthorPageModel
from automation.generators.static.book_cell_renderer_v2 import BookCellRendererV2


class AuthorPageGeneratorV4:
    def __init__(self, template_path: str, book_cell_template_path: str):
        """
        template_path: author_template.php.mustache
        book_cell_template_path: book_cell.php.mustache
        """
        self.template_path = template_path
        self.book_cell_renderer = BookCellRendererV2(book_cell_template_path)

    def load_template(self) -> str:
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    def flatten_books(self, model: AuthorPageModel) -> list:
        """
        Превръща BookCellModel[] → HTML блокове
        """
        rendered = []
        for book in model.books:
            html = self.book_cell_renderer.render(book)
            rendered.append({"book_cell_html": html})
        return rendered

    def render(self, model: AuthorPageModel) -> str:
        template = self.load_template()

        context: Dict[str, Any] = asdict(model)
        context["books_rendered"] = self.flatten_books(model)

        return pystache.render(template, context)

    def save(self, model: AuthorPageModel, output_path: str):
        html = self.render(model)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
