# BookPageURLResolver_v1_0.py

class BookPageURLResolverV1_0:
    """
    Генерира каноничния URL за статичната страница на книга.
    Използва:
      - primary_genre (от GenreResolver)
      - slug (от SlugifyService)
    """

    def __init__(self, base_host: str = "https://gabriell-e-lit.com"):
        # Основният домейн на статичните страници
        self.base_host = base_host.rstrip("/")

    # ---------------------------------------------------------
    # Публичен метод
    # ---------------------------------------------------------

    def resolve(self, genre: str, slug: str) -> str:
        """
        Връща пълния URL към статичната страница на книгата.

        Пример:
          genre = "poezia"
          slug = "saniatarazuma"

          → https://gabriell-e-lit.com/p-izdatelstvo/poezia/saniatarazuma.php
        """

        if not genre:
            genre = "poezia"

        if not slug:
            slug = "unknown"

        return f"{self.base_host}/p-izdatelstvo/{genre}/{slug}.php"
