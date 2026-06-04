# NavigationMaps (v1.0)

## Обединена архитектурна навигация на платформата gabriell‑e‑lit

Папката **NavigationMaps/** съдържа официалните, финални навигационни карти на всички
слоеве на платформата gabriell‑e‑lit. Това са **архитектурни документи**, които описват
реалната структура на сайта, поддомейните, WordPress проектите и статичните ресурси.

NavigationMaps е **нормативният слой**, който определя:

- как е организирана платформата като навигационна система  
- кои са входните точки  
- какви са връзките между слоевете  
- какви са реалните URL-и  
- как се подреждат динамичните и статичните части  
- как се изгражда Master Navigation Map  

Това е **единственият източник на истина** за навигационната архитектура.

---

# ## 1. Роля на NavigationMaps слоя

NavigationMaps:

- описва реалната структура на сайта  
- дефинира навигационните пътеки  
- показва връзките между WordPress, статичния сайт и поддомейните  
- служи като основа за:
  - sitemap модели  
  - навигационни JSON-и  
  - автоматично генериране на менюта  
  - AI‑базирана навигационна логика  
  - екстракция на структурни страници  
  - интеграция между слоевете  

NavigationMaps е **архитектурен документ**, а не технически модел.

---

# ## 2. Структура на папката

```
NavigationMaps/
│
├── README.md
│
├── NavigationMap – Master – v1.0.md
├── NavigationMap – Publisher – v1.0.md
├── NavigationMap – Magazine – v1.0.md
└── NavigationMap – StaticSite+Subdomains – v1.0.md
```

Всеки документ описва отделен навигационен слой.

---

# ## 3. Описание на документите

### ### 3.1 `NavigationMap – Master – v1.0.md`
Обединена архитектурна карта на цялата платформа.

Съдържа:

- ROOT layer  
- Project layer  
- Dynamic layers (Publisher + Magazine)  
- Static layer  
- Subdomain layer  
- Dependencies между слоевете  
- Master структура на платформата  

Това е **главният документ**, който обединява всички останали.

---

### ### 3.2 `NavigationMap – Publisher – v1.0.md`
Официалната навигационна карта на WordPress издателството.

Съдържа:

- WP Pages  
- WP Categories  
- Publisher genres  
- AuthorIndex  
- External links  
- Финална структура  

---

### ### 3.3 `NavigationMap – Magazine – v1.0.md`
Официалната навигационна карта на WordPress списанието.

Съдържа:

- ROOT категория  
- WP Pages  
- Themes  
- Sections & Directions  
- Archives  
- Issues  
- Special categories  
- System pages  

---

### ### 3.4 `NavigationMap – StaticSite+Subdomains – v1.0.md`
Навигационна карта на:

- статичния сайт  
- статичното издателство  
- статичното списание  
- статичната галерия  
- трите поддомейна:
  - e-library  
  - e-gallery  
  - e-books  

Съдържа:

- STATIC_FILE  
- STATIC_DIR  
- STATIC_AUTHOR  
- STATIC_EXHIBITION  
- STATIC_ARTWORK  
- STATIC_SUBDOMAIN  
- STATIC_SUBDOMAIN_LINK  

---

# ## 4. Връзка с останалите слоеве

NavigationMaps работи в синхрон с:

- **navigation/** → навигационни модели и JSON структури  
- **models/sitemap/** → sitemap модели  
- **architecture/** → глобални принципи  
- **dataflow/** → структурни страници (H2/H3)  
- **ExtractionRules/** → правила за извличане на навигационни елементи  

Връзката е:

```
NavigationMaps/  →  navigation/  →  models/sitemap/
```

---

# ## 5. Версии

Всички документи в тази папка са **v1.0**, финални и стабилни.

Следващи версии ще бъдат:

- v1.1 → добавяне на нови URL-и  
- v2.0 → реорганизация на навигационните слоеве  
- v3.0 → автоматично генериране от екстрактора  

---

# ## 6. Какво следва

- добавяне на визуална диаграма на Master Navigation Map  
- автоматично генериране на sitemap.json от NavigationMaps  
- интеграция с навигационните модели  
- създаване на NavigationFlow (аналог на DataFlow)  

---

Това е **официалната библиотека с навигационни карти** на платформата gabriell‑e‑lit.
