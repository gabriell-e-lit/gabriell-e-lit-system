# SlugifyService_v1_0.py

import re

class SlugifyServiceV1_0:
    """
    Централизиран механизъм за латинизация и нормализация на slug-ове.
    Поддържа:
      - българска транслитерация
      - премахване на тирета
      - нормализация на заглавия
      - нормализация на авторски имена
      - специални правила за slug-ове на книги
    """

    # Българска транслитерация (официална + твоята система)
    BG_MAP = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ж':'j','з':'z','и':'i',
        'й':'j','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s',
        'т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sht',
        'ъ':'a','ь':'','ю':'iu','я':'ia',

        'А':'a','Б':'b','В':'v','Г':'g','Д':'d','Е':'e','Ж':'j','З':'z','И':'i',
        'Й':'j','К':'k','Л':'l','М':'m','Н':'n','О':'o','П':'p','Р':'r','С':'s',
        'Т':'t','У':'u','Ф':'f','Х':'h','Ц':'ts','Ч':'ch','Ш':'sh','Щ':'sht',
        'Ъ':'a','Ь':'','Ю':'iu','Я':'ia'
    }

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Публични методи
    # ---------------------------------------------------------

    def from_title(self, title: str) -> str:
        """
        Генерира slug от заглавие на книга.
        Пример:
          "Балкан" → "balkan"
          "Сънят на разума" → "saniatarazuma"
        """
        if not title:
            return ""

        translit = self._transliterate(title)
        cleaned = self._normalize(translit)
        return cleaned

    def from_author(self, name: str) -> str:
        """
        Генерира slug за автор.
        Пример:
          "Димитър Анакиев" → "dimitaranakiev"
        """
        if not name:
            return ""

        translit = self._transliterate(name)
        cleaned = self._normalize(translit)
        return cleaned

    def remove_dashes(self, slug: str) -> str:
        """
        Премахва тирета от slug.
        """
        return slug.replace("-", "")

    # ---------------------------------------------------------
    # Вътрешни помощни методи
    # ---------------------------------------------------------

    def _transliterate(self, text: str) -> str:
        """
        Транслитерация на български → латиница.
        """
        result = []
        for ch in text:
            if ch in self.BG_MAP:
                result.append(self.BG_MAP[ch])
            else:
                result.append(ch)
        return "".join(result)

    def _normalize(self, text: str) -> str:
        """
        Премахва всичко, което не е буква или цифра.
        """
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", "", text)
        return text
