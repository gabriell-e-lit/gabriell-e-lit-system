# NavigationMap – Publisher – v1.0

## Издателство gabriell‑e‑lit — WordPress динамичен сайт  
**Официална версия (готова за библиотеката)**

Този документ описва навигационната архитектура на WordPress издателството — всички
страници, категории, индекси и външни връзки, които формират динамичния слой на
издателството gabriell‑e‑lit.

---

# 🟦 I. WP_PAGE  
Статични WordPress страници, които участват в навигацията на издателството.

```
/izdatelstvo/gabriell-e-lit/                           | WP_PAGE | Root page
/izdatelstvo/gabriell-e-lit/ekip-gabriell-e-lit/       | WP_PAGE | Team
/izdatelstvo/gabriell-e-lit/uslugi-izdatelstvo/        | WP_PAGE | Services
/izdatelstvo/gabriell-e-lit/konkurs/                   | WP_PAGE | Contest description
/izdatelstvo/gabriell-e-lit/editions/                  | WP_PAGE | Editions overview
/izdatelstvo/gabriell-e-lit/books/                     | WP_PAGE | Books index
/izdatelstvo/gabriell-e-lit/expected-titles/           | WP_PAGE | Expected titles
/izdatelstvo/gabriell-e-lit/e-knigi-gabriell-e-lit/    | WP_PAGE | Ebooks overview
/izdatelstvo/authors-e-library-gabriell-e-lit/         | WP_PAGE | Authors for elibrary
/izdatelstvo/artists-e-gallery-gabriell-e-lit/         | WP_PAGE | Artists for egallery
```

---

# 🟧 II. WPCategory  
Динамични WordPress категории, включени в навигацията на издателството.

```
/izdatelstvo/publishing-house-gabriell-e-lit/                          | WPCategory | Publisher articles
/izdatelstvo/.../akcenti/za-izdatelstvoto-i-spisanieto/                | WPCategory | About publisher & magazine
/izdatelstvo/.../akcenti/novi-knigi/                                   | WPCategory | New books
/izdatelstvo/.../akcenti/ochakvani-zaglavia/                           | WPCategory | Expected titles
/izdatelstvo/publishing-house-gabriell-e-lit/p-knigi-gabriell-e-lit/   | WPCategory | Print books
/izdatelstvo/publishing-house-gabriell-e-lit/e-knigi-gabriell-e-lit/   | WPCategory | Ebooks
/izdatelstvo/publishing-house-gabriell-e-lit/chereshovite-vodi-na-bulgarskata-tanka/ | WPCategory | Contest main
/izdatelstvo/.../chereshovite-vodi-na-bulgarskata-tanka-2023/          | WPCategory | Contest 2023
/izdatelstvo/.../chereshovite-vodi-na-bulgarskata-tanka-2024/          | WPCategory | Contest 2024
/izdatelstvo/.../chereshovite-vodi-na-bulgarskata-tanka-2025/          | WPCategory | Contest 2025
```

---

# 🟩 III. AuthorIndex  
Официалният списък на авторите на издателството.

```
/izdatelstvo/gabriell-e-lit/authors-gabriell-e-lit/   | AuthorIndex | Publisher authors
```

---

# 🟪 IV. ExternalLink  
Външни поддомейни и външни ресурси, свързани с издателството.

```
https://bookstore.gabriell-e-lit.com/     | ExternalLink | Bookstore
https://e-books.gabriell-e-lit.com/       | ExternalLink | Ebooks subdomain
https://gabriell-e-lit.com/               | ExternalLink | Main site
https://e-library.gabriell-e-lit.com/     | ExternalLink | Elibrary subdomain
https://e-gallery.gabriell-e-lit.com/     | ExternalLink | Egallery subdomain
```

---

# ⭐ Финална структура (обобщение)

## **WP_PAGE**
- root  
- team  
- services  
- contest  
- editions  
- books  
- expected titles  
- ebooks  
- authors for elibrary  
- artists for egallery  

## **WPCategory**
- publisher articles  
- about publisher & magazine  
- new books  
- expected titles  
- print books  
- ebooks  
- contest (main + yearly)  

## **AuthorIndex**
- publisher authors  

## **ExternalLink**
- bookstore  
- ebooks  
- main site  
- elibrary  
- egallery  

---

# ⭐ Финал

Това е **NavigationMap – Publisher – v1.0**  
Официалната навигационна карта на WordPress издателството gabriell‑e‑lit.
