# DataFlow – Static Site → DataTypes – v1.0  
**Версия:** 1.0  
**Категория:** DataFlow / Static Site  
**Статус:** Официален документ  
**Зависимости:**  
- Author v2.3  
- Book v2  
- Artwork v2  
- Exhibition v1.1  
- DataFlow – WordPress Posts → DataTypes – v1.0  
- DataFlow – WordPress Structural Pages → DataTypes – v1.0  

---

## 1. Обхват на документа
Този документ описва как екстракторът обработва **статичния сайт gabriell‑e‑lit.com**, за да обедини неговите данни с WordPress и да създаде единна, консистентна база от DataTypes v2.

Статичният сайт и динамичният WordPress сайт:

- възникват едновременно  
- развиват се паралелно  
- съдържат различни, но взаимно допълващи се слоеве  
- са равнопоставени източници на истина  

Статичният сайт е **архив в смисъла на библиотека**:  
устойчив, подреден, висококачествен слой, който съдържа:

- най-пълните биографии  
- най-качествените изображения  
- официалните страници на автори, книги, изложби  
- дългосрочната памет на платформата  

Не всеки автор от WordPress има статична страница.  
Не всяка изложба от списанието има статична страница.  
Но **всичко, което има статична страница, е канон**.

---

## 2. Основни принципи

### ✔ 2.1 Статичният сайт и WordPress са двупосочно свързани
Примери:

- **Нова книга** → статична страница + e‑books + WordPress рецензия  
- **Нова изложба в галерията** → представяне в списанието  
- **Коментарна статия за изложба** → статична страница на изложбата  
- **Нов автор в статичния сайт** → получава WordPress таг само когато има публикация  
- **Гост‑редактор в WordPress** → винаги получава статична страница  

### ✔ 2.2 Приоритетите са ясни и стабилни
```
H2 > H3 > wp_tag > wp_posts > static_site > ebooks
```

### ✔ 2.3 Статичният сайт е канон за:
- книги на издателството  
- изложби  
- галерии  
- авторски страници  
- официални биографии  
- официални портрети  
- **гост‑редактори**  

---

## 3. Поток: Static Site → Author

### 3.1 Разпознаване
Автор се разпознава по:

- статична страница в /authors/  
- статична страница в /gallery/  
- статична страница в /library/  
- **статична страница в /guest-editors/** (ако съществува)  

### 3.2 Данни, които се извличат
```
Author {
    biography (ако липсва в WordPress),
    portrait (ако липсва в WordPress),
    wikipedia_links[],
    static_page_url,
    artworks[],
    exhibitions[],
    roles[]
}
```

### 3.3 Ефекти върху Author
```
Author.biography = static_site_bio (ако няма H2/H3/wp_tag/wp_post)
Author.portrait = static_site_portrait (ако няма H2/H3/wp_tag/wp_post)
Author.wikipedia_links += links_from_static_page
Author.must_have_static_page = true (ако е в канон)
```

### 3.4 Специално правило: Гост‑редактори
```
Author.roles += "guest_editor"
Author.must_have_static_page = true
Author.static_page_url = /guest-editors/<slug>.php
```

Имената им се извличат от динамичната страница:
**„Гост редактори“ в раздел Изкуство**.

---

## 4. Поток: Static Site → Book

### 4.1 Разпознаване
Книга се разпознава по:

- страница в /books/  
- страница в /ebooks/  
- страница в /library/  

### 4.2 Данни, които се извличат
```
Book {
    title,
    authors[],
    cover_image,
    description,
    publication_year,
    isbn,
    static_page_url
}
```

### 4.3 Ефекти върху Book
```
Book.cover = static_cover (ако липсва WordPress корица)
Book.description = static_description (ако липсва WordPress описание)
Book.publication_year = static_year (ако липсва WordPress година)
Book.isbn = static_isbn (ако липсва WordPress ISBN)
```

---

## 5. Поток: Static Site → Artwork

### 5.1 Разпознаване
Artwork се разпознава по:

- страници в /gallery/  
- изображения в статични изложби  
- изображения в статични авторски страници  

### 5.2 Данни, които се извличат
```
Artwork {
    image_url,
    caption,
    artist,
    exhibition,
    static_page_url
}
```

### 5.3 Ефекти върху Artwork
```
Artwork.image = static_image
Artwork.caption = static_caption
Artwork.artist = static_artist
Artwork.exhibition = static_exhibition
```

---

## 6. Поток: Static Site → Exhibition

### 6.1 Разпознаване
Изложба се разпознава по:

- страници в /exhibitions/  
- страници в /gallery/  
- страници в /authors/ (ако съдържат изложбени блокове)  

### 6.2 Данни, които се извличат
```
Exhibition {
    title,
    artworks[],
    artists[],
    description,
    static_page_url
}
```

### 6.3 Ефекти върху Exhibition
```
Exhibition.artworks += artworks_from_static_page
Exhibition.artists += artists_from_static_page
Exhibition.description = static_description (ако липсва WordPress описание)
```

---

## 7. Двупосочни синхронизации

### 7.1 WordPress → Static Site
Статични страници се създават **само за каноничните групи**:

- автори на издателството  
- автори с книги в библиотеката  
- художници на издателството  
- художници в галерията  
- избрани художници от „Автори на е‑галерия gabriell‑e‑lit“  
- **гост‑редактори на списанието**

Примери:
- нова книга → статична страница + e‑books  
- статия за изложба → статична страница на изложбата  
- представяне на художник → обновяване на статичната страница  

### 7.2 Static Site → WordPress
Статичният сайт се отразява в WordPress **само когато има публикация**:

- нова книга → рецензия в списанието  
- нова изложба → представяне в списанието  
- нов автор → получава WordPress таг само при публикация  
- **гост‑редактор → винаги присъства в структурната страница „Гост редактори“**

---

## 8. Несъответствия и пропуски

### 8.1 Автор има статична страница, но липсва в структурните WordPress страници
```
WARNING: Author exists in static site but is missing from structural WordPress pages.
```

### 8.2 Книга съществува в статичния сайт, но няма WordPress публикации
Това е нормално.

### 8.3 Изложба съществува в статичния сайт, но няма WordPress следи
Това е нормално.

### 8.4 Artwork в статичния сайт няма автор
```
WARNING: Static artwork missing artist attribution.
```

---

## 9. Финален резултат
След обработка на статичния сайт екстракторът има:

- пълна, канонична база от автори  
- пълна база от книги на издателството  
- пълна база от изложби и произведения  
- двупосочна синхронизация между WordPress и статичния сайт  
- устойчив, библиотечен слой от висококачествени данни  
- **гост‑редакторите са гарантирано представени и в двата слоя**  

Това е шестият и последен слой от DataFlow.
