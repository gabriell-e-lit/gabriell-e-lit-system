# BookCellModel v2.0  
Модел за визуална клетка на книга (UI компонент).

## Предназначение
Използва се в:
- авторски страници
- каталози
- списъци с книги
- галерии
- блокове „още книги“

Не е страница. Не съдържа метаданни. Само визуални елементи.

---

## Структура

### Основни връзки
- `book_page_url` — URL към страницата на книгата
- `title` — заглавие
- `author_name` — име на автора
- `author_page_url` — URL към страницата на автора

### Корици
- `covers.ebook_url`
- `covers.ebook_alt`
- `covers.print_url`
- `covers.print_alt`

### Формати
- `formats.pdf_url`
- `formats.epub_url`
- `formats.pbook_url`
- `formats.audio_url`

### Display (UX)
- `display.show_author`
- `display.show_formats`
- `display.show_double_cover`

---

## Бележки
- Всички URL полета могат да бъдат празни.
- Ако даден формат липсва, той не се визуализира.
- `show_double_cover` контролира дали да се показват две корици (ebook + print).
