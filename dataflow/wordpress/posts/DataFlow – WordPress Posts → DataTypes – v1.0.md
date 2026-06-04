# DataFlow – WordPress Posts → DataTypes – v1.0  
**Версия:** 1.0  
**Категория:** DataFlow / WordPress  
**Статус:** Официален документ  
**Зависимости:**  
- DataFlow – Overview – v1.0  
- Issue v2  
- Author v2.3  
- Book v2  
- Artwork v2  
- StructuralAuthorPages v1.1  
- DataFlow – WordPress Categories → DataTypes – v1.0  
- DataFlow – WordPress Tags → DataTypes – v1.0  

---

## 1. Обхват на документа
Този документ описва как екстракторът обработва **WordPress Posts**, за да създаде и обогати обектите от DataTypes v2:

- Issue  
- Author  
- Book  
- Artwork  

Постовете са основният източник на съдържание в списанието.

---

## 2. Роля на WordPress постовете в системата

WordPress постовете имат пет основни роли:

### ✔ 1) Да свързват автори с броеве  
### ✔ 2) Да определят жанровата принадлежност на публикациите  
### ✔ 3) Да съдържат художествени изображения (Artwork)  
### ✔ 4) Да съдържат рецензии и представяния на книги на издателството  
### ✔ 5) Да предоставят биографична информация (ако липсва другаде)

---

## 3. Данни, които се извличат от всеки пост

```
PostData {
    id,
    title,
    content_html,
    content_text,
    authors[],
    categories[],
    tags[],
    images[],
    publication_date,
    source_url
}
```

---

## 4. Поток: Post → Author

### 4.1 Разпознаване на автори
Авторите се извличат от:

- WordPress тагове  
- мета-полета (ако има)  
- структурни елементи в съдържанието (рядко)  

### 4.2 Ефекти върху Author
```
Author.posts += post
Author.sections += жанрови категории на поста
Author.issues += issue_category_of_post
Author.years += year_of_post
```

### 4.3 Биография от пост
Ако постът съдържа биографичен блок:

```
Author.biography = biography_from_post (ако няма H2/H3/wp_tag биография)
```

---

## 5. Поток: Post → Issue

### 5.1 Разпознаване
Issue се определя от:

- Issue категорията на поста  
- годината на поста (потвърждение)  

### 5.2 Ефекти върху Issue
```
Issue.posts += post
Issue.authors += authors_of_post
Issue.artworks += artworks_in_post
Issue.sections += жанрови категории на поста
```

---

## 6. Поток: Post → Artwork

### 6.1 Разпознаване
Artwork се извлича **само от изображения в съдържанието**:

- изображения в content HTML  
- изображения в галерии, вмъкнати в съдържанието  

**Featured image никога не се счита за Artwork.**  
Неговата роля е на корица на електронния брой или визуален маркер на категория.

### 6.2 Данни, които се извличат
```
Artwork {
    image_url,
    caption,
    artist,
    source_post,
    issue,
    year
}
```

### 6.3 Ефекти върху Artwork
```
Artwork.image = image_url
Artwork.caption = caption
Artwork.artist = author_of_post (ако е художествен пост)
Artwork.issue = issue_of_post
Artwork.year = year_of_post
```

---

## 7. Поток: Post → Book

### 7.1 Разпознаване
Пост е свързан с книга на издателството, ако:

- е в категория **р‑Книги gabriell‑e‑lit**
- или е в категория **е‑Книги gabriell‑e‑lit**
- или съдържа корица на книга на издателството
- или съдържа ISBN на книга на издателството
- или съдържа ключови думи („роман“, „поетична книга“, „сборник“) **и е за книга на издателството**
- или е рецензия или представяне на книга на издателството

Категория „Книги“ не съществува и не се използва.

### 7.2 Данни, които се извличат
```
Book {
    title,
    authors[],
    cover_image,
    description,
    review_post,
    publication_year
}
```

**Само книги на издателството gabriell‑e‑lit се превръщат в Book обекти.**  
**Постове в категориите „р‑Книги gabriell‑e‑lit“ и „е‑Книги gabriell‑e‑lit“ винаги създават Book обект.**

### 7.3 Ефекти върху Book
```
Book.reviews += post
Book.cover = first_image_in_post (ако е корица)
Book.description = excerpt_of_post
Book.authors += authors_of_post
Book.source_category = "р‑Книги gabriell‑e‑lit" или "е‑Книги gabriell‑e‑lit"
```

---

## 8. Поток: Post → Genre / Editorial Classification

### 8.1 Жанрови категории
Пример:
- Поезия  
- Проза  
- Есеистика  
- Критика  

Ефект:
```
Post.genre = genre_category
Author.sections += genre_category
Issue.sections += genre_category
```

### 8.2 Редакционни категории
Пример:
- Коментар  
- Анонс  

Ефект:
```
Post.editorial_type = editorial_category
```

---

## 9. Несъответствия и пропуски

### 9.1 Пост има автори, но няма тагове
```
WARNING: Post has authors but no WordPress tags.
```

### 9.2 Пост е в Issue категория, но датата му е извън периода на броя
```
WARNING: Post date is outside the Issue date range.
```

### 9.3 Пост е в годишна категория, но годината му е различна
```
WARNING: Post year does not match the year category.
```

### 9.4 Пост съдържа изображения, но не са художествени
Това е нормално.

### 9.5 Пост съдържа художествени изображения, но няма автор
```
WARNING: Artwork found in post without identifiable artist.
```

---

## 10. Финален резултат
След обработка на всички WordPress постове, екстракторът има:

- пълна връзка между автори и публикации  
- пълна структура на броевете  
- жанрови и редакционни секции  
- художествени произведения (Artwork)  
- рецензии и представяния на книги на издателството  
- диагностика за времеви и структурни несъответствия  

Това е четвъртият слой от WordPress екстракцията и основа за част 5.
