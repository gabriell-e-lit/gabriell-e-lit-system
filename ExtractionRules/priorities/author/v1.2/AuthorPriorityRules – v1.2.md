# AuthorPriorityRules – v1.2
## Приоритетни правила за автори (структурни WordPress страници)  
**Версия 1.2 — разширена и прецизирана**

Този документ описва разширените приоритетни правила за автори, извлечени от
структурните WordPress страници на платформата gabriell‑e‑lit.  
Той определя:

- кой е автор  
- каква роля има  
- дали трябва да има WordPress таг  
- дали трябва да има статична страница  
- първа поява  
- приоритет на биография и портрет  
- подкатегории на художници  

---

# 🟦 1. Основен принцип

Структурните WordPress страници са **най-важният източник на истина** за авторите.

Те определят:

- авторство  
- роля  
- задължителни елементи (wp_tag, static_page)  
- първа поява  
- биография  
- портрет  

---

# 🟩 2. H2 автори → задължителни биографии в WordPress таговете

H2 автори се срещат **само** в страниците „Автори в брой X“.  
Това е **най-високият структурен маркер** за автори в WordPress.

```
if author appears as H2 in "Автори в брой X":
    must_have_wp_tag = true
    must_have_static_page = false
    biography_priority = "H2"
    portrait_priority = "H2"
    first_appearance = this_page_or_issue
```

### ✔ Значение
- Тагът е **задължителен**.  
- Биографията от H2 страницата е **основна**.  
- Портретът от H2 страницата е **основен**.  
- Това е най-ранната и най-важна поява.

---

# 🟧 3. H3 автори → задължителни статични страници

H3 автори се срещат в четири типа структурни страници:

- Автори на издателството  
- Автори в е‑библиотека  
- Автори в е‑галерия  
- Гост‑редактори  

Причината да са H3 е **структурна**, не приоритетна.

```
if author appears as H3 in structural pages:
    must_have_static_page = true
    must_have_wp_tag = false
    biography_priority = "H3" (if no H2 biography)
    portrait_priority = "H3" (if no H2 portrait)
```

### ✔ Значение
- Статичната страница е **задължителна**.  
- Биографията и портретът могат да бъдат взети от H3, ако няма H2.  

---

# 🟪 4. Подкатегории на художници (само от „Автори в е‑галерия“)

H2 заглавията в тази страница определят подкатегорията:

```
if author appears under H2 "Автори с изложби":
    gallery_subcategory = "exhibition_artist"

if author appears under H2 "Илюстратори на книги":
    gallery_subcategory = "illustrator"

if author appears under H2 "Художници в списанието":
    gallery_subcategory = "magazine_artist"
```

### ✔ Значение
Подкатегорията определя:

- ролята в `Author.roles`  
- връзките към Exhibition, Book или Issue  
- поведението на екстрактора  

---

# 🟫 5. Приоритет на източниците за biography и portrait

```
biography_priority_order = [
    "H2",
    "H3",
    "wp_tag",
    "wp_posts",
    "static_site",
    "ebooks"
]

portrait_priority_order = biography_priority_order
```

### ✔ Значение
- H2 е **абсолютен приоритет**.  
- H3 е втори.  
- Всички останали са fallback.  

---

# 🟦 6. Първа поява (first_appearance)

```
first_appearance_priority = [
    "H2_page",
    "H3_page",
    "Issue"
]
```

### ✔ Значение
- Най-ранната H2 страница е първа поява.  
- Ако няма H2 → най-ранната H3.  
- Ако няма H3 → най-ранният Issue.  

---

# ⭐ Финал

Това е **официалната Markdown версия на AuthorPriorityRules – v1.2**.  
Готова е за директно качване в GitHub.

