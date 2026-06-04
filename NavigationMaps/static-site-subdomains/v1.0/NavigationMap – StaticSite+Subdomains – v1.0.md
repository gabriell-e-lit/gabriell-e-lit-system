# NavigationMap – StaticSite+Subdomains – v1.0

## Статичен сайт + поддомейни (gabriell‑e‑lit.com)  
**Официална версия (готова за библиотеката)**

Този документ описва навигационната архитектура на статичния слой на платформата
gabriell‑e‑lit, както и трите основни поддомейна: e‑library, e‑gallery и e‑books.

Това е архивният, но структурно най‑стабилен слой, който съдържа реални авторски страници,
книги, изложби, картини и файлове.

---

# 🟦 I. STATIC ROOT  
Основни статични страници на главния сайт.

```
/             | STATIC_FILE | Root page
/index.php    | STATIC_FILE | Root page (duplicate)
/zanas.php    | STATIC_FILE | About
/mission.php  | STATIC_FILE | Mission
/uslugi.php   | STATIC_FILE | Services
/ekip.php     | STATIC_FILE | Team
```

---

# 🟩 II. PROJECT LINKS  
Връзки от статичния сайт към динамичните WordPress проекти.

```
/izdatelstvo/gabriell-e-lit/   | PROJECT_LINK | Publishing house (WordPress)
/izdatelstvo/                  | PROJECT_LINK | Magazine (WordPress)
```

---

# 🟧 III. STATIC SUBDOMAINS (root level)  
Трите основни поддомейна.

```
https://e-library.gabriell-e-lit.com/   | STATIC_SUBDOMAIN | Elibrary
https://e-gallery.gabriell-e-lit.com/   | STATIC_SUBDOMAIN | Egallery
https://bookstore.gabriell-e-lit.com/   | STATIC_SUBDOMAIN | Bookstore
```

---

# 🟫 IV. STATIC PUBLISHING (pizdatelstvo)  
Статичният слой на издателството.

### **Главни страници**
```
/izdatelstvo.php   | STATIC_FILE  | Publishing root
/aktualno.php      | STATIC_FILE  | New books
/newbooks.php      | STATIC_FILE  | Expected books
/knigi.php         | STATIC_INDEX | Books index
```

### **Азбучни списъци**
```
/p-izdatelstvo/books/1.php   | STATIC_INDEX | Alphabetical list (books)
```

### **Жанрови списъци**
```
/p-izdatelstvo/poezia.php    | STATIC_INDEX | Genre: Poetry
```

### **Автори**
```
/p-izdatelstvo/authors/3.php                     | STATIC_INDEX        | Alphabetical authors
/p-izdatelstvo/authors/valentinagrigorova.php    | STATIC_AUTHOR       | Author page
/authors.php                                     | STATIC_AUTHOR_INDEX | Authors index
```

---

# 🟪 V. STATIC MAGAZINE (spisanie)  
Статичният слой на списанието.

### **Главни страници**
```
/spisanie.php        | STATIC_FILE | Magazine description
/spisanie-new.php    | STATIC_FILE | Magazine overview
```

### **Екип и гостредактори**
```
/spisanie-ekip.php                        | STATIC_FILE        | Editorial team
/spisanie/gost-redaktori/1.php            | STATIC_GUEST_EDITOR | Guest editor
/spisanie/gost-redaktori/dimitaranakiev.php | STATIC_GUEST_EDITOR | Guest editor
```

### **Автори в броеве**
```
/spisanie-authors.php   | STATIC_ISSUE_AUTHORS | Issue authors index
```

### **Архив**
```
/spisanie-arhiv.php     | STATIC_FILE | Issues archive
```

---

# 🟦 VI. STATIC GALLERY (gallery.php, kartini.php)  
Статичният слой на галерията.

### **Главни страници**
```
/gallery.php          | STATIC_FILE | Gallery overview
/kartini.php          | STATIC_FILE | Paintings
/authors-painters.php | STATIC_FILE | Painters index
```

### **Връзки към поддомейна**
```
https://e-gallery.gabriell-e-lit.com/authors/3.php
    | STATIC_SUBDOMAIN_LINK | Painters list

https://e-gallery.gabriell-e-lit.com/authors/kartini-s-dumi-i-bagri/venelinapetkova.php
    | STATIC_SUBDOMAIN_LINK | Painter page
```

---

# 🟫 VII. STATIC SUBDOMAIN STRUCTURE  
Архитектурни директории в поддомейните.

---

## **elibrary**
```
/authors/       | STATIC_DIR | Authors
/books/         | STATIC_DIR | Books
/genres/        | STATIC_DIR | Genres
/alphabetical/  | STATIC_DIR | Alphabetical lists
/files/         | STATIC_DIR | Files
/images/        | STATIC_DIR | Covers / images
```

---

## **egallery**
```
/authors/                         | STATIC_DIR        | Artist groups
/authors/<group>/                 | STATIC_DIR        | Group
/authors/<group>/<author>/        | STATIC_DIR        | Artist
/authors/<group>/<author>/<exhibition>.php | STATIC_EXHIBITION | Exhibition
/authors/<group>/<author>/images/*.jpg     | STATIC_ARTWORK    | Artwork
```

---

## **ebooks**
```
/authors/       | STATIC_DIR | Authors
/books/         | STATIC_DIR | Books
/files/         | STATIC_DIR | Ebook files
/genres/        | STATIC_DIR | Genres
/alphabetical/  | STATIC_DIR | Alphabetical lists
```

---

# ⭐ Финална структура (обобщение)

## **STATIC_FILE**
- root pages  
- publishing pages  
- magazine pages  
- gallery pages  

## **STATIC_DIR**
- authors  
- books  
- genres  
- alphabetical  
- images  
- files  

## **STATIC_AUTHOR / STATIC_AUTHOR_INDEX**
- author pages  
- author lists  

## **STATIC_EXHIBITION / STATIC_ARTWORK**
- exhibitions  
- artworks  

## **STATIC_INDEX**
- alphabetical lists  
- genre lists  
- book index  

## **STATIC_SUBDOMAIN / STATIC_SUBDOMAIN_LINK**
- elibrary  
- egallery  
- bookstore  

---

# ⭐ Финал

Това е **NavigationMap – StaticSite+Subdomains – v1.0**  
Официалната навигационна карта на статичния сайт и поддомейните на gabriell‑e‑lit.
