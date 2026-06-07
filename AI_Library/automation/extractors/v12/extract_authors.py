import json
from pathlib import Path
from bs4 import BeautifulSoup

class AuthorExtractor:
    """
    AuthorExtractor v3.0
    Работи с AuthorModel-v3.0.json
    """

    def __init__(self, html_content: str, model_path: str):
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.model = self.load_model(model_path)
        self.data = self.initialize_output_structure()

    # ---------------------------------------------------------
    # MODEL LOADING
    # ---------------------------------------------------------
    def load_model(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # INITIALIZE OUTPUT
    # ---------------------------------------------------------
    def initialize_output_structure(self) -> dict:
        """
        Създава празна структура според AuthorModel v3.0
        """
        return {
            "seo": {
                "title": "",
                "description": "",
                "canonical_url": ""
            },
            "identity": {
                "author_id": "",
                "slug": "",
                "name_original": "",
                "name_display": ""
            },
            "biography": {
                "short": "",
                "long": "",
                "quote": ""
            },
            "photo": {
                "url": "",
                "alt": ""
            },
            "origin": {
                "country": "",
                "city": "",
                "birth_year": "",
                "death_year": ""
            },
            "links": {
                "tag_url": "",
                "gallery_subcategory": "",
                "gallery_url": "",
                "library_url": ""
            },
            "structure": {
                "structural_pages_h2": [],
                "structural_pages_h3": [],
                "first_appearance": ""
            },
            "books": [],
            "publications": [],
            "magazine_issues": [],
            "exhibitions": [],
            "collections": [],
            "navigation": {
                "alphabetical": True
            },
            "visual": {
                "show_quote": True,
                "show_origin": True,
                "show_gallery": True,
                "show_publications": True
            }
        }

    # ---------------------------------------------------------
    # REAL EXTRACTION FUNCTIONS (Variant C)
    # ---------------------------------------------------------

    # 1) Extract name_display
    def extract_name_display(self):
        """
        Извлича името, което се вижда на страницата.
        Най-често е в <h1> или в заглавието на публикацията.
        """
        h1 = self.soup.find("h1")
        if h1:
            self.data["identity"]["name_display"] = h1.get_text(strip=True)

    # 2) Extract name_original
    def extract_name_original(self):
        """
        Ако авторът е български → name_original = name_display.
        Ако е чужд → ще добавим логика по-късно.
        """
        self.data["identity"]["name_original"] = self.data["identity"]["name_display"]

    # 3) Extract slug
    def extract_slug(self, url: str):
        """
        Извлича slug от URL.
        Пример:
        https://gabriell-e-lit.com/izdatelstvo/tag/zad-garba-gabriela-zaneva
        → slug = zad-garba-gabriela-zaneva
        """
        slug = url.rstrip("/").split("/")[-1]
        self.data["identity"]["slug"] = slug

    # 4) Extract author_id
    def extract_author_id(self):
        """
        Генерира author_id от slug.
        Пример:
        slug = zad-garba-gabriela-zaneva
        → author_id = author_zad_garba_gabriela_zaneva
        """
        slug = self.data["identity"]["slug"]
        author_id = "author_" + slug.replace("-", "_")
        self.data["identity"]["author_id"] = author_id

    # ---------------------------------------------------------
    # MAIN PIPELINE
    # ---------------------------------------------------------
    def run(self, url: str) -> dict:
        self.extract_name_display()
        self.extract_name_original()
        self.extract_slug(url)
        self.extract_author_id()
        return self.data
