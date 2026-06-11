# BookPageModel v3.0  
Пълен модел за страница на книга.

## Предназначение
Използва се за:
- статични страници на книги
- SEO
- метаданни
- корици
- формати
- рецензии
- връзки към автора и каталози

---

## Структура

### SEO
- `seo.title`
- `seo.description`
- `seo.canonical_url`

### Metadata
- `metadata.title`
- `metadata.author`
- `metadata.genre`
- `metadata.year`
- `metadata.pages`
- `metadata.binding_print`
- `metadata.format_print`
- `metadata.isbn_print`
- `metadata.isbn_pdf`
- `metadata.isbn_epub`

### Cover
- `cover.ebook_url`
- `cover.ebook_alt`
- `cover.print_url`
- `cover.print_alt`

### Formats
- `formats.pdf_url`
- `formats.epub_url`
- `formats.pbook_url`
- `formats.audio_url`

### Links
- `links.author_page_url`
- `links.tag_url`
- `links.registry_url`
- `links.goodreads_url`
- `links.bookstore_url`

### Texts
- `intro`
- `description`

### Reviews
Списък от:
- `text`
- `source_url`
- `source_label`

### Navigation
- `navigation.alphabetical`
- `navigation.genre`

### Visual
- `visual.include_book_cell`

---

## Бележки
- Всички полета са опционални.
- `reviews` може да бъде празен списък.
- `formats` може да съдържа само някои формати.
