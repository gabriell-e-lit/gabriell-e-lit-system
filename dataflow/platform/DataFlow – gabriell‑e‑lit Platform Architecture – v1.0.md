#DataFlow – gabriell‑e‑lit Platform Architecture – v1.0
##Unified Architectural Document
Human Layer + Normative Layer + Technical Layer
###I. EXECUTIVE SUMMARY (HUMAN LAYER)
За редактори, читатели, бъдещи сътрудници, за теб самата
####1. Философия на платформата
gabriell‑e‑lit е двупластова литературно‑издателска екосистема, съставена от:

динамичен WordPress сайт (списание, броеве, публикации, автори, рецензии)

статичен сайт (канон, библиотека, галерия, книги, изложби, авторски страници)

e‑books поддомейн (пълни текстове на книги на издателството)

Тези три слоя:

възникват едновременно

развиват се паралелно

допълват се взаимно

никой не е „по‑стар“ или „по‑нов“

никой не е „вторичен“

всеки е източник на истина за различни типове данни

Платформата е едновременно:

списание

издателство

библиотека

галерия

архив

литературна карта

художествена екосистема

#### 2. Източници на истина
WordPress е източник на истина за:
публикации

броеве

жанрови категории

авторски тагове

динамични събития (рецензии, анонси, представяния)

художествени изображения в публикации

Статичният сайт е източник на истина за:
автори на издателството

автори с книги в библиотеката

художници на издателството

художници в галерията

избрани художници

гост‑редактори

книги на издателството

изложби

канонични биографии

канонични портрети

e‑books поддомейн е източник на истина за:
пълни текстове на книги

метаданни за книги

корици

структурирани описания

#### 3. Как работи системата (високо ниво)
WordPress предоставя динамичния слой: публикации, броеве, автори, рецензии.

Статичният сайт предоставя каноничния слой: автори, книги, изложби, галерии.

e‑books предоставя пълните текстове и метаданни за книгите.

Екстракторът обединява данните в единна структура DataTypes v2.

Приоритетите определят кое е водещо при конфликт.

Синхронизациите определят кога единият слой създава или обновява другия.

#### 4. Канон срещу динамика
WordPress е динамика — живо списание, публикации, броеве.

Статичният сайт е канон — библиотека, архив, официални страници.

Всичко, което има статична страница, е канонично.
Всичко, което е само в WordPress, е динамично.

#### 5. Ролята на двата сайта
WordPress:
публикува

представя

рецензира

анонсира

свързва автори с броеве

съдържа художествени изображения

Статичният сайт:
съхранява

подрежда

архивира

представя канона

съдържа официалните страници

### II. NORMATIVE SPECIFICATION (ARCHITECTURAL LAYER)
Строг, нормативен, стандартизиращ слой
1. Дефиниции
Източник на истина (Source of Truth):  
Слой, който съдържа най‑авторитетната версия на даден тип данни.

Канон:  
Съдържание, което има статична страница и е част от дългосрочния архив.

Динамика:  
Съдържание, което съществува само в WordPress.

Екстрактор:  
Система, която обединява данните от всички слоеве в DataTypes v2.

#### 2. Sources of Truth (Normative)
2.1 WordPress ТРЯБВА да бъде източник на истина за:
публикации

броеве

жанрови категории

авторски тагове

изображения в публикации

2.2 Статичният сайт ТРЯБВА да бъде източник на истина за:
автори на издателството

автори с книги в библиотеката

художници на издателството

художници в галерията

избрани художници

гост‑редактори

книги на издателството

изложби

канонични биографии

канонични портрети

2.3 e‑books ТРЯБВА да бъде източник на истина за:
пълни текстове на книги

корици

метаданни

#### 3. WordPress Layer (Normative)
3.1 Categories → Issue / Year / Genre
Issue категории ТРЯБВА да определят броя.

Годишни категории ТРЯБВА да определят годината.

Жанрови категории ТРЯБВА да определят жанра.

3.2 Posts → Author / Artwork / Book
Пост ТРЯБВА да свързва автори с броеве.

Artwork ТРЯБВА да се извлича само от изображения в съдържанието.

Пост ТРЯБВА да създава Book само ако книгата е на издателството.

3.3 Tags → Author Metadata
Таг ТРЯБВА да съдържа авторско име.

Таг МОЖЕ да съдържа биография.

Таг МОЖЕ да съдържа портрет.

Таг МОЖЕ да съдържа Wikipedia линкове.

3.4 Structural Pages → Canonical Authors
H2 ТРЯБВА да означава автор в „Автори в брой X“.

H3 ТРЯБВА да означава автор в останалите страници.

Гост‑редакторите ТРЯБВА да бъдат извлечени от динамичната страница „Гост редактори“.

Гост‑редакторите ТРЯБВА да имат статична страница.

#### 4. Static Site Layer (Normative)
4.1 Authors
Автор ТРЯБВА да има статична страница ако е:

автор на издателството

автор с книга в библиотеката

художник на издателството

художник в галерията

избран художник

гост‑редактор

4.2 Books
Книга ТРЯБВА да има статична страница ако е:

издадена от издателството

включена в библиотеката

включена в e‑books

4.3 Exhibitions
Изложба ТРЯБВА да има статична страница ако:

е представена в галерията

е представена в списанието

4.4 Artworks
Artwork ТРЯБВА да бъде извлечен от:

статични изложби

статични авторски страници

статични галерии

#### 5. DataTypes (Normative)
5.1 Author v2.3
Автор ТРЯБВА да съдържа:

name

biography

portrait

roles[]

gallery_subcategory

static_page_url

source_urls[]

5.2 Book v2
Книга ТРЯБВА да съдържа:

title

authors[]

cover_image

description

publication_year

isbn

5.3 Artwork v2
Artwork ТРЯБВА да съдържа:

image_url

caption

artist

exhibition

5.4 Exhibition v1.1
Изложба ТРЯБВА да съдържа:

title

artworks[]

artists[]

description

#### 6. Priority Rules (Normative)
6.1 Biography Priority
Код
H2 > H3 > wp_tag > wp_posts > static_site > ebooks
6.2 Portrait Priority
Код
H2 > H3 > wp_tag > wp_posts > static_site
6.3 Category Priority
Issue > Year > Genre

6.4 Canonical vs Dynamic
Канонът НЕ ТРЯБВА да бъде отменян от динамични данни.

#### 7. Synchronization Rules (Normative)
7.1 WordPress → Static Site
Статични страници ТРЯБВА да се създават само за канонични групи.

7.2 Static Site → WordPress
WordPress ТРЯБВА да създава тагове само при публикации.

7.3 Special Rules
Гост‑редакторите ТРЯБВА да имат статична страница.

Гост‑редакторите ТРЯБВА да бъдат извлечени от динамичната страница.

### III. TECHNICAL IMPLEMENTATION NOTES (DEVELOPER LAYER)
Технически, кратък, функционален слой
#### 1. Data Extraction Pipelines
WordPress Pipeline
Код
categories → issue/year/genre
tags → author metadata
posts → authors, artworks, books
structural pages → canonical authors
Static Site Pipeline
Код
authors → canonical metadata
books → canonical metadata
exhibitions → artworks + artists
gallery → artworks + artists
#### 2. JSON Models
Author
Код
{
  "name": "",
  "biography": "",
  "portrait": "",
  "roles": [],
  "gallery_subcategory": "",
  "static_page_url": "",
  "source_urls": []
}
Book
Код
{
  "title": "",
  "authors": [],
  "cover_image": "",
  "description": "",
  "publication_year": "",
  "isbn": ""
}
Artwork
Код
{
  "image_url": "",
  "caption": "",
  "artist": "",
  "exhibition": ""
}
Exhibition
Код
{
  "title": "",
  "artworks": [],
  "artists": [],
  "description": ""
}
#### 3. Algorithmic Flow
Author Extraction
Код
if H2: use H2 data
else if H3: use H3 data
else if wp_tag: use tag data
else if wp_posts: use post data
else if static_site: use static data
Artwork Extraction
Код
from wp_posts: images in content only
from static_site: gallery + exhibitions
Book Extraction
Код
if category in {р-Книги, е-Книги}: create Book
else if ISBN + publisher = gabriell-e-lit: create Book
#### 4. Conflict Resolution Logic
Код
if conflict(biography):
    use highest priority source
if conflict(portrait):
    use highest priority source
if conflict(book metadata):
    prefer static_site over wp_posts
#### 5. Mapping Tables
Gallery Subcategories
Код
"Автори с изложби" → exhibition_artist
"Илюстратори на книги" → illustrator
"Художници в списанието" → magazine_artist

### IV. FULL DATAFLOW DIAGRAM (TEXTUAL)
#### 1. WordPress Flow
Код
categories → issue/year/genre
posts → authors + artworks + books
tags → author metadata
structural pages → canonical authors
#### 2. Static Site Flow
Код
authors → canonical metadata
books → canonical metadata
exhibitions → artworks + artists
gallery → artworks + artists
#### 3. Combined Flow
Код
WordPress + Static Site + e-books
        ↓
   Data Extraction
        ↓
   Priority Rules
        ↓
   Conflict Resolution
        ↓
   DataTypes v2
   
   # DataFlow Diagram – gabriell‑e‑lit Platform (v1.0)

                        ┌──────────────────────────┐
                        │      SOURCES OF TRUTH     │
                        └─────────────┬────────────┘
                                      │
     ┌────────────────────────────────┼────────────────────────────────┐
     │                                │                                │
┌──────────────┐              ┌──────────────┐                ┌────────────────┐
│  WORDPRESS   │              │ STATIC SITE  │                │   E‑BOOKS      │
│ (Dynamic)    │              │ (Canonical)  │                │ (Full Texts)   │
└──────┬───────┘              └──────┬───────┘                └──────┬────────┘
       │                              │                                │
       │                              │                                │
       ▼                              ▼                                ▼

┌──────────────────┐       ┌──────────────────┐         ┌────────────────────┐
│ Categories        │       │ Authors          │         │ Book Metadata       │
│ (Issue/Year/Genre)│       │ (Canonical)      │         │ (ISBN, Year, etc.) │
└─────────┬────────┘       └─────────┬────────┘         └──────────┬─────────┘
          │                            │                             │
          ▼                            ▼                             ▼

┌──────────────────┐       ┌──────────────────┐         ┌────────────────────┐
│ Posts            │       │ Books            │         │ Full Book Texts     │
│ (Authors, Art)   │       │ (Canonical)      │         │ (Chapters, EPUB)    │
└─────────┬────────┘       └─────────┬────────┘         └──────────┬─────────┘
          │                            │                             │
          ▼                            ▼                             ▼

┌──────────────────┐       ┌──────────────────┐
│ Tags             │       │ Exhibitions      │
│ (Author Meta)    │       │ (Canonical)      │
└─────────┬────────┘       └─────────┬────────┘
          │                            │
          ▼                            ▼

───────────────────────────────────────────────────────────────────────────────
                     DATA EXTRACTION & NORMALIZATION
───────────────────────────────────────────────────────────────────────────────

          ┌────────────────────────────────────────────────────────┐
          │   PRIORITY RULES (H2 > H3 > Tag > Post > Static > e‑b) │
          └────────────────────────────────────────────────────────┘

          ┌────────────────────────────────────────────────────────┐
          │   CONFLICT RESOLUTION (Canonical Wins)                 │
          └────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────
                               DATATYPES v2
───────────────────────────────────────────────────────────────────────────────

┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Author      │   │    Book       │   │   Artwork     │   │  Exhibition   │
│  (v2.3)       │   │    (v2)       │   │    (v2)       │   │    (v1.1)     │
└──────┬────────┘   └──────┬────────┘   └──────┬────────┘   └──────┬────────┘
       │                   │                   │                   │
       └───────────────┬───┴───────┬───────────┴───────────┬───────┘
                       ▼           ▼                       ▼

                ┌──────────────────────────────────────────────┐
                │         UNIFIED PLATFORM OUTPUT               │
                └──────────────────────────────────────────────┘

                - Canonical Author Pages  
                - Book Pages (Static + e‑books + WP reviews)  
                - Exhibition Pages  
                - Artwork Collections  
                - Issue Pages  
                - Magazine Structure  
                - Search & Navigation  

### V. APPENDIX

#### 1. Glossary
Канон — съдържание със статична страница.

Динамика — съдържание само в WordPress.

Екстрактор — система за обединяване на данни.

#### 2. Canonical Lists
автори на издателството

автори с книги

художници на издателството

художници в галерията

избрани художници

гост‑редактори

#### 3. Future Extensions
Generator → Static Pages

AI → Classification

e‑books → Automated Metadata
