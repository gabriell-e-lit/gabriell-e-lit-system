# AuthorPageModel v4.3  
Пълен модел за авторска страница.

## Предназначение
Използва се за генериране на:
- статични авторски страници
- SEO блокове
- биография
- списъци с книги (BookCellModel)
- публикации
- галерии
- структурни страници

---

## Структура

### SEO
- `seo.title`
- `seo.description`
- `seo.canonical_url`

### Identity
- `identity.author_id`
- `identity.slug`
- `identity.name_original`
- `identity.name_display`

### Biography
- `biography.short`
- `biography.long`
- `biography.quote`

### Photo
- `photo.url`
- `photo.alt`

### Origin
- `origin.country`
- `origin.city`
- `origin.birth_year`
- `origin.death_year`

### Links
- `links.tag_url`
- `links.gallery_subcategory`
- `links.gallery_url`
- `links.library_url`

### Structure
- `structural_pages_h2`
- `structural_pages_h3`
- `first_appearance`

### Content Lists
- `books` — списък от BookCellModel
- `publications`
- `magazine_issues`
- `exhibitions`
- `collections`

### Navigation
- `navigation.alphabetical`

### Visual
- `visual.show_quote`
- `visual.show_origin`
- `visual.show_gallery`
- `visual.show_publications`

---

## Бележки
- `books` съдържа **BookCellModel**, не сурови книги.
- `quote` е опционално поле.
- `origin` може да бъде частично попълнено.
