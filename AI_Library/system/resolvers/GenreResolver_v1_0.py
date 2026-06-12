# GenreResolver_v1_0.py

from urllib.parse import urlparse
import re


class GenreResolverV1_0:
    """
    Определя жанра на книга според:
      - директорията на PDF/EPUB (най-силен сигнал)
      - директорията на корицата
      - URL на витрината (p-izdatelstvo или e-books)
      - допълнителни витрини (книга може да е в повече от един жанр)
    """

    # Каноничните жанрове на издателството
    GENRES = {
        "poezia",
        "beletristika",
        "dokumentalnaproza",
        "publicistika",
        "sbornici",
        "childrensbooks",
        "art",
        "nliteratura",
    }

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Публичен метод
    # ---------------------------------------------------------

    def resolve(self, source_url: str, cover_url: str, pdf_url: str) -> dict:
        """
        Връща:
        {
            "primary_genre": "publicistika",
            "all_genres": ["publicistika", "sbornici"]
        }
        """

        genres = set()

        # 1) Най-силен сигнал → PDF/EPUB директория
        pdf_genre = self._extract_genre_from_url(pdf_url)
        if pdf_genre:
            genres.add(pdf_genre)

        # 2) Втори сигнал → корица
        cover_genre = self._extract_genre_from_url(cover_url)
        if cover_genre:
            genres.add(cover_genre)

        # 3) Трети сигнал → витрина (source_url)
        source_genre = self._extract_genre_from_url(source_url)
        if source_genre:
            genres.add(source_genre)

        # Ако няма нито един жанр → fallback
        if not genres:
            genres.add("poezia")  # безопасен fallback

        # Основният жанр е:
        # 1) pdf_genre
        # 2) cover_genre
        # 3) source_genre
        primary_genre = (
            pdf_genre
            or cover_genre
            or source_genre
            or "poezia"
        )

        return {
            "primary_genre": primary_genre,
            "all_genres": list(genres),
        }

    # ---------------------------------------------------------
    # Вътрешни помощни методи
    # ---------------------------------------------------------

    def _extract_genre_from_url(self, url: str) -> str:
        """
        Извлича жанра от URL, ако съдържа директория от GENRES.
        Пример:
          https://e-books.gabriell-e-lit.com/publicistika/Book.pdf → publicistika
          https://gabriell-e-lit.com/p-izdatelstvo/poezia.php → poezia
        """
        if not url:
            return ""

        parsed = urlparse(url)
        path = parsed.path.lower()

        # Търсим директория от жанровете
        for genre in self.GENRES:
            pattern = rf"/{genre}(/|\.php|$)"
            if re.search(pattern, path):
                return genre

        return ""
