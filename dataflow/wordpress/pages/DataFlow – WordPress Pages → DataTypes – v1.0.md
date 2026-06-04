# DataFlow – WordPress Pages → DataTypes – v1.0  
**Версия:** 1.0  
**Категория:** DataFlow / WordPress  
**Статус:** Официален документ  
**Зависимости:**  
- DataFlow – Overview – v1.0  
- StructuralAuthorPages v1.1  
- Author v2.3  
- AuthorPriorityRules v1  

---

## 1. Обхват на документа
Този документ описва как екстракторът обработва **WordPress Pages**, за да създаде и обогати обектите от DataTypes v2:

- Author  
- Issue  
- Book  
- Exhibition  
- Artwork  

Документът покрива само **WordPress Pages** (не Posts, не Tags, не Categories).

---

## 2. Основни типове WordPress Pages
WordPress страниците, които участват в екстракцията, са дефинирани в StructuralAuthorPages v1.1:

1. **Автори в брой X**  
2. **Автори на издателство gabriell-e-lit**  
3. **Автори в е-библиотека**  
4. **Автори в е-галерия gabriell-e-lit**  
5. **Гост редактори**

Всеки тип страница има различна семантика и различни правила за екстракция.

---

## 3. Общи принципи на екстракцията от WordPress Pages

### 3.1 HTML заглавията определят семантиката
- В страниците „Автори в брой X“ → **H2 = автор**  
- В останалите 4 страници →  
  **H2 = структурна група (H2-група)**  
  **H3 = автор**

### 3.2 Данните се извличат само от структурни елементи
Екстракторът използва:

- заглавия (H2/H3)  
- параграфи след заглавия  
- изображения в блока на автора  
- линкове към статични страници  
- вътрешни WordPress линкове  

### 3.3 Данните се нормализират към DataTypes v2
Всяко открито лице се превръща в:

```
Author {
    id,
    name,
    biography,
    portrait,
    structural_pages_h2,
    structural_pages_h3,
    gallery_subcategory,
    must_have_wp_tag,
    must_have_static_page,
    first_appearance,
    source_urls
}
```

---

## 4. Поток: „Автори в брой X“ → Author

### 4.1 Разпознаване на автори
```
selector: h2
```

### 4.2 Данни, които се извличат
- **name** → текстът на H2  
- **biography** → първият параграф след H2 (ако има)  
- **portrait** → първото изображение след H2 (ако има)  
- **issue_id** → от URL или заглавие на страницата  
- **source_url** → URL на страницата  

### 4.3 Ефекти върху Author
```
must_have_wp_tag = true
must_have_static_page = false
biography_priority = H2
portrait_priority = H2
first_appearance = тази страница или Issue
structural_pages_h2 += тази страница
```

---

## 5. Поток: „Автори на издателство gabriell-e-lit“ → Author

### 5.1 Разпознаване
```
H2 = структурна група (H2-група)
H3 = автор
```

### 5.2 Данни, които се извличат
- **name** → текстът на H3  
- **biography** → параграф след H3  
- **portrait** → изображение след H3  
- **structural_group** → текстът на H2 (не е автор!)  

### 5.3 Ефекти върху Author
```
must_have_static_page = true
must_have_wp_tag = false
biography_priority = H3_if_no_H2
portrait_priority = H3_if_no_H2
structural_pages_h3 += тази страница
```

---

## 6. Поток: „Автори в е-библиотека“ → Author

### 6.1 Разпознаване
```
H2 = структурна група (H2-група)
H3 = автор
```

### 6.2 Ефекти върху Author
```
must_have_static_page = true
structural_pages_h3 += тази страница
```

---

## 7. Поток: „Автори в е-галерия gabriell-e-lit“ → Author

### 7.1 Разпознаване
```
H2 = структурна група (подкатегория художници)
H3 = автор
```

### 7.2 Подкатегории (от H2-групата)
```
"Автори с изложби" → exhibition_artist
"Илюстратори на книги" → illustrator
"Художници в списанието" → magazine_artist
```

### 7.3 Ефекти върху Author
```
must_have_static_page = true
gallery_subcategory = от H2-групата
structural_pages_h3 += тази страница
```

---

## 8. Поток: „Гост редактори“ → Author

### 8.1 Разпознаване
```
H2 = структурна група (година)
H3 = автор
```

### 8.2 Ефекти върху Author
```
must_have_static_page = true
roles += "guest_editor"
structural_pages_h3 += тази страница
```

---

## 9. Конфликти и приоритети

### 9.1 Ако автор е H2 в една страница и H3 в друга
```
H2 има абсолютен приоритет.
must_have_wp_tag = true
must_have_static_page = true (ако има H3)
```

### 9.2 Ако има две биографии
```
H2 > H3 > wp_tag > wp_posts > static_site > ebooks
```

---

## 10. Финален резултат
След обработка на всички WordPress Pages, екстракторът има:

- пълен списък с автори  
- първа поява  
- биографии  
- портрети  
- подкатегории художници  
- задължителни тагове  
- задължителни статични страници  
- структурни връзки  

Това е основата за следващите потоци.
