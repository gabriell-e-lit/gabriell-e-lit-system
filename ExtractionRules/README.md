# ExtractionRules (v1.0) 

## Нормативен слой за правилата на екстрактора в платформата gabriell‑e‑lit

Папката **ExtractionRules/** съдържа официалните, нормативни правила, които управляват
поведението на екстрактора при извличане, нормализация и изграждане на структурирани
обекти (Author, Book, Issue, Artwork, Exhibition, Post, Section, EBookFile).

Това е **редакторският договор** между канона, архитектурата и автоматизацията.

---

# ## 1. Роля на ExtractionRules слоя

ExtractionRules определят:

- как екстракторът чете HTML, WordPress и статичния сайт  
- какви източници са канон и кои са допълващи  
- как се извличат имена, биографии, портрети, роли  
- как се определя идентичността на автора  
- как се прилагат приоритети между източници  
- как се откриват нови автори  
- как се обработват конфликти  
- как се изгражда финалният модел (Author v2.3 и др.)

Това е **единственият източник на истина** за поведението на екстрактора.

---

# ## 2. Структура на папката

```
ExtractionRules/
│
├── README.md
│
├── authors/
│   └── ExtractionRules‑Authors‑v1.0.txt
│
├── identity/
│   └── ExtractionRules‑Identity‑v1.0.txt
│
├── architecture/
│   └── Extractor-Architecture-v1.0.txt
│
├── fundamentals/
│   └── Extractor-Fundamentals-v1.0.txt
│
└── priorities/
    └── Extractor-PriorityRules-v1.0.txt
```

Всеки модул е самостоятелен и описва отделен аспект от екстракцията.

---

# ## 3. Описание на модулите

### ### 3.1 `authors/`
**ExtractionRules‑Authors‑v1.0.txt**  
Правила за извличане на автори от всички източници:

- статичен сайт  
- wp_structural  
- WP тагове  
- WP публикации  
- H2/H3 структурни страници  
- ebooks  

Определя как се извличат:  
canonical_name, biography, portrait, roles, gallery_subcategory, static_page_url.

---

### ### 3.2 `identity/`
**ExtractionRules‑Identity‑v1.0.txt**  
Правила за идентичност:

- canonical_name  
- display_name  
- native_name  
- identity_key  
- нормализация  
- поведение при колизии  
- различаване на автори  

Това е основата на стабилната идентификация.

---

### ### 3.3 `architecture/`
**Extractor-Architecture-v1.0.txt**  
Архитектура на екстрактора:

- Raw Extraction  
- Model Alignment  
- Cross-Source Enrichment  
- Merge  
- Build  

Определя слоевете и тяхното взаимодействие.

---

### ### 3.4 `fundamentals/`
**Extractor-Fundamentals-v1.0.txt**  
Основни принципи:

- канонът не се редактира автоматично  
- екстракторът предлага, редакторът решава  
- статичният сайт е канон за ключови полета  
- wp_structural е канон за роли и галерийни подкатегории  
- ролите се обединяват, не се премахват  

---

### ### 3.5 `priorities/`
**Extractor-PriorityRules-v1.0.txt**  
Приоритети на източниците за всяко поле:

- canonical_name  
- display_name  
- biography  
- portrait  
- roles  
- gallery_subcategory  
- static_page_url  
- source_urls  

Това е „решаващият слой“, който определя кое е водещо при конфликт.

---

# ## 4. Връзка с останалите слоеве

ExtractionRules работи в синхрон с:

- **dataflow/** → откъде идват данните  
- **models/datatypes/** → как изглеждат финалните обекти  
- **architecture/** → глобалните принципи на платформата  

Връзката е:

```
dataflow/  →  ExtractionRules/  →  extractor  →  datatypes/
```

---

# ## 5. Актуална версия

Всички правила в тази папка са **v1.0** и са съвместими с:

- Author v2.3  
- Issue v2.1  
- EBookFile v2  
- Post v1.2  
- Section v1.0  
- Exhibition v1.1  
- Artwork v2.1  

---

# ## 6. Какво следва

- добавяне на README.md във всяка подпапка  
- създаване на диаграма на екстрактора  
- автоматично генериране на тестове за правилата  
- интеграция с DataFlow v1.0  

---

Това е **официалната библиотека с правила на екстрактора** за платформата gabriell‑e‑lit.
