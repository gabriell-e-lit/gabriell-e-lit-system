# DataFlow – E‑Books → DataTypes – v1.0

## Версия: 1.0 (официална)
Категория: DataFlow / E‑Books
Статус: Завършен документ
Зависимости:
- Book v2
- EBookFile v2
- Artwork v2
- DataFlow – Static Site → DataTypes
- DataFlow – WordPress Posts → DataTypes

---------------------------------------------------------------------

### I. ОБХВАТ НА ДОКУМЕНТА
Този документ описва как екстракторът обработва поддомейна
e‑books.gabriell-e-lit.com, за да създаде и обогати:

- Book v2 (електронни издания)
- EBookFile v2 (файлове)
- Artwork v2 (корици)
- връзки между книги, автори и файлове

Поддомейнът e‑books е:
- файлов архив
- навигационен слой
- вторичен източник на метаданни
- първичен източник на файлове и корици

Описанията на книги и биографии НЕ се намират тук.

---------------------------------------------------------------------

### II. ОСНОВНИ ПРИНЦИПИ

#### 2.1 e‑books е източник на истина за:
- PDF/EPUB файлове
- корици (cover.jpg)
- налични формати
- азбучни списъци
- жанрови списъци
- връзки към файловете
- сезонни броеве (PDF + full cover)

#### 2.2 e‑books НЕ е източник на истина за:
- описания на книги
- биографии
- роли
- ISBN
- година на издаване
- авторски списъци

#### 2.3 e‑books е вторичен спрямо p‑izdatelstvo за:
- описание на книгата
- автори
- ISBN
- година
- жанр

#### 2.4 e‑books е първичен за:
- файлове
- корици
- формати
- print‑on‑demand корици (само за списанието)

---------------------------------------------------------------------

### III. СТРУКТУРА НА ПОДДОМЕЙНА E‑BOOKS

#### 3.1 Коренова директория
Съдържа:
- index.php (навигационен хъб)
- жанрови файлове (poezia.php, beletristika.php…)
- директории за жанрове
- директория /books (азбучни списъци)
- директория /spisanie (броеве)
- /blocks и /includes (игнорират се)

#### 3.2 index.php – НАВИГАЦИОНЕН ХЪБ
Съдържа три секции:
- търсене по жанр → root жанрови файлове
- търсене по заглавие → /books/1.php … /books/29.php
- търсене по автор → линкове към p‑izdatelstvo/authors/

#### 3.3 Жанрови root‑файлове
Съдържат:
- списъци с книги
- корици
- PDF/EPUB линкове
- линкове към p‑izdatelstvo (описания)

#### 3.4 Жанрови директории
Съдържат:
- поддиректории за книги
- PDF/EPUB файлове
- корици (cover.jpg)

#### 3.5 Директории на книги (НЕСТАНДАРТИЗИРАНИ)
Възможни структури:

A) Всичко в една папка:
    /<genre>/<book>/
        cover.jpg
        Author-Book.pdf или Book-Author.pdf
        Author-Book.epub или Book-Author.epub

B) Отделни поддиректории:
    /<genre>/<book>/
        <book>-pdf/
            cover-for-pdf.jpg
            Author-Book.pdf или Book-Author.pdf
        <book>-epub/
            cover.jpg
            meta
            Author-Book.epub или Book-Author.epub

C) Смесени:
    /<genre>/<book>/
        cover.jpg
        Author-Book.pdf
        <book>-epub/
            Author-Book.epub

ВАЖНО:
За всеки формат (PDF, EPUB) има точно един файл.
Името е или Author-Book, или Book-Author.

#### 3.6 Директория /books (азбучни списъци)
Съдържа:
- 1.php … 29.php
- списъци с книги по буква
- корици
- PDF/EPUB линкове

#### 3.7 Директория /spisanie
Съдържа:
- PDF файлове на сезонните броеве
- /covers с двойни корици (full cover spreads)

---------------------------------------------------------------------

### IV. ПОТОК: E‑BOOKS → BOOK

4.1 Разпознаване
Книга се разпознава по:
- присъствие в жанров root‑файл
- присъствие в азбучен файл
- присъствие в директория на книга
- присъствие в /spisanie (за броеве)

4.2 Данни, които се извличат
Book {
    ebook_files[],
    front_cover,
    source_urls[]
}

4.3 Данни, които НЕ се извличат от e‑books
- title
- subtitle
- description
- authors
- isbn
- publication_year

Те идват от p‑izdatelstvo.

4.4 Ефекти върху Book
Book.ebook_files += всички намерени файлове
Book.front_cover = cover.jpg (ако липсва в статичния сайт)
Book.source_urls += всички ebook страници

4.5 Ново правило:
Ако книга има файлове в e‑books, но няма статична страница в p‑izdatelstvo:
    Book.must_have_static_page = true
Екстракторът предлага създаване на нова статична страница.

---------------------------------------------------------------------

### V. ПОТОК: E‑BOOKS → EBOOKFILE

5.1 Разпознаване
Файл се разпознава по:
- разширение (pdf, epub)
- местоположение (root или поддиректория)
- име (Author-Book или Book-Author)

5.2 Данни, които се извличат
EBookFile {
    id,
    book_id,
    format,
    file_url,
    role,
    version,
    source_urls[]
}

5.3 Ефекти върху EBookFile
EBookFile.book_id = inferred_from_directory
EBookFile.format = extension
EBookFile.role = inferred_from_filename
EBookFile.source_urls += file_url

5.4 Ново правило:
За всеки формат (PDF, EPUB) трябва да има точно един файл.
Ако има повече:
    WARNING: Duplicate ebook files detected.

---------------------------------------------------------------------

### VI. ПОТОК: E‑BOOKS → ARTWORK (КОРИЦИ)

6.1 Разпознаване
Корица се разпознава по:
- cover.jpg (root)
- cover.jpg (в EPUB поддиректория)
- cover-for-pdf.jpg (ако съществува)

6.2 Данни, които се извличат
Artwork {
    image_url,
    artwork_type,
    linked_book,
    role,
    source_urls[]
}

6.3 Ефекти върху Artwork
Artwork.artwork_type = front_cover
Artwork.role = cover_front
Artwork.linked_book = Book.id

ВАЖНО:
Електронните книги НЯМАТ full.jpg.
full.jpg се използва САМО за списанието.

---------------------------------------------------------------------

### VII. ПОТОК: E‑BOOKS → AUTHOR

7.1 Разпознаване
Автор НЕ се извлича от e‑books.
Авторите се извличат от p‑izdatelstvo.

7.2 Ефекти върху Author
Author.books += books_found_in_ebooks
Author.source_urls += ebook_pages

---------------------------------------------------------------------

### VIII. НЕСЪОТВЕТСТВИЯ И ПРОПУСКИ

8.1 Книга има файлове, но няма статична страница
WARNING: Missing static page for ebook → static page must be created.

8.2 Файл няма свързана книга
ERROR: Ebook file without identifiable book directory.

8.3 Корица без книга
WARNING: Cover image found without matching Book.

8.4 EPUB-only edition
INFO: EPUB-only edition detected.

8.5 Смесена структура
INFO: Mixed-format directory structure detected.

8.6 Дублирани файлове
WARNING: Duplicate PDF files detected.
WARNING: Duplicate EPUB files detected.

---------------------------------------------------------------------

### IX. ФИНАЛЕН РЕЗУЛТАТ

След обработка на e‑books екстракторът има:
- пълна база от електронни файлове
- пълна база от корици
- пълна връзка между книги и файлове
- информация за налични формати
- информация за сезонни броеве
- диагностика за липси и несъответствия
- предложения за създаване на липсващи статични страници

Това е финалният слой от DataFlow.
