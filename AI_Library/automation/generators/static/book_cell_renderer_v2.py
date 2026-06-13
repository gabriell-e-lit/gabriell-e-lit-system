# BookCellModel v2.0 – рендериране на книга-клетка (UI компонент)

from dataclasses import asdict
from typing import Dict, Any
import pystache

from system.models.book_cell.BookCellModel_v2_0 import BookCellModel


class BookCellRendererV2:
    def __init__(self, template_path: str):
        """
        template_path: път към book_cell.php.mustache
        """
        self.template_path = template_path

    def load_template(self) -> str:
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    def render(self, model: BookCellModel) -> str:
        template = self.load_template()
        context: Dict[str, Any] = asdict(model)
        return pystache.render(template, context)
