# NavigationMap – Magazine – v1.0

## Списание „Картини с думи и багри“ — WordPress динамичен сайт  
**Официална версия (готова за библиотеката)**

Този документ описва навигационната архитектура на WordPress списанието — всички
страници, категории, теми, рубрики, архиви и системни елементи, които формират
динамичния слой на списанието gabriell‑e‑lit.

---

# 🟦 I. ROOT  
Главна категория на списанието.

```
/izdatelstvo/spisanie-kartini-s-dumi-i-bagri/   | WPCategory | Magazine root
```

---

# 🟩 II. WP_PAGE  
Описателни WordPress страници на списанието.

```
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/abonament/                     | WP_PAGE | Subscription
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/ekip-spisanie/                 | WP_PAGE | Editorial team
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/ekip-spisanie/gost-redaktori/  | WP_PAGE | Guest editors index
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/ekip-spisanie/gost-redaktori-razdel-nauka/ | WP_PAGE | Guest editors (science)
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie-authors-spisanie/              | WP_PAGE | Issue authors index
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/arhiv-broi/                    | WP_PAGE | Issues archive
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/razdel-izkustvo/               | WP_PAGE | Theme description: Art
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/razdel-nauka-za-izkustvoto/    | WP_PAGE | Theme description: Art science
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/razdel-nauka/                  | WP_PAGE | Theme description: Science
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/razdel-nauka-za-izkustvoto/vidove-nauchni-publikatsii-i-kriterii-za-nauchnost/ | WP_PAGE | Scientific criteria
/izdatelstvo/kartini-s-dumi-i-bagri-spisanie/dobaviane-na-publikatsia/      | WP_PAGE | Frontend submission
```

---

# 🟧 III. THEMES (основни теми)  
Трите основни тематични категории.

```
/izdatelstvo/spisanie-kartini-s-dumi-i-bagri/kartini-s-dumi-i-bagri-izkustvo/     | WPCategory | Theme: Art
/izdatelstvo/spisanie-kartini-s-dumi-i-bagri/nauka-za-izkustvoto/                 | WPCategory | Theme: Art science
/izdatelstvo/spisanie-kartini-s-dumi-i-bagri/kartini-s-dumi-i-bagri-nauka/        | WPCategory | Theme: Science
```

---

# 🟫 IV. SECTIONS & DIRECTIONS  
Рубрики и направления под темите.

### **Под „Изкуство“**
```
.../akcenti/                                   | WPCategory | Section: Accents
.../akcenti/za-art-platforma-gabriell-e-lit/   | WPCategory | Subsection
.../poezia/                                    | WPCategory | Section: Poetry
.../proza/                                     | WPCategory | Section: Prose
```

### **Под „Наука за изкуството“**
```
.../napravlenie-literatura/                    | WPCategory | Direction: Literature
.../napravlenie-vizualni-izkustva/             | WPCategory | Direction: Visual arts
```

### **Под „Наука“**
(ще се добави при следващата стъпка)

---

# 🟪 V. ARCHIVES  
Годишни архиви и броеве.

### **Годишни архиви**
```
/arhiv-2026/   | WPCategory | Year archive 2026
/arhiv-2025/   | WPCategory | Year archive 2025
/arhiv-2024/   | WPCategory | Year archive 2024
/arhiv-2023/   | WPCategory | Year archive 2023
/arhiv-2022/   | WPCategory | Year archive 2022
/arhiv-2021/   | WPCategory | Year archive 2021
/arhiv-2020/   | WPCategory | Year archive 2020
/arhiv-2019/   | WPCategory | Year archive 2019
```

### **Броеве**
```
/arhiv-2026/1-2026/   | WPCategory | Issue 1/2026
/arhiv-2019/4-2019/   | WPCategory | Issue 4/2019
/arhiv-2019/1-2019/   | WPCategory | Issue 1/2019
/0-2018/              | WPCategory | Issue 0/2018
```

### **Автори в брой**
```
/authors-1-2026-30/   | WP_PAGE | Issue authors (1/2026)
```

---

# 🟧 VI. SPECIAL CATEGORIES  
Системни динамични категории.

```
/aktualno/   | WPCategory | Latest posts
```

---

# 🟦 VII. SYSTEM PAGES  
Задължителни системни страници.

```
/privacy-policy/             | WP_PAGE | Privacy policy
/politika-za-biskvitki-es/   | WP_PAGE | Cookies policy
```

---

# ⭐ Финална структура (обобщение)

## **WPCategory**
- magazine root  
- themes  
- sections  
- directions  
- year archives  
- issues  
- special categories  

## **WP_PAGE**
- subscription  
- editorial team  
- guest editors  
- issue authors index  
- issues archive  
- theme descriptions  
- submission page  
- system pages  

---

# ⭐ Финал

Това е **NavigationMap – Magazine – v1.0**  
Официалната навигационна карта на WordPress списанието „Картини с думи и багри“.
