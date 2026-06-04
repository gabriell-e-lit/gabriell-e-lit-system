function run_extractor(config):

    # 1. Инициализация
    sources = config.sources              # WP, Static, e-books
    rules = config.rules                  # приоритети, мапинги, селектори
    store  = init_raw_store()             # временно хранилище за сурови данни

    # 2. Обхождане на всички източници
    for source in sources:
        pages = crawl_source(source)      # връща списък от URL + HTML

        for page in pages:
            dom = parse_html(page.html)

            page_type = classify_page(page.url, dom, rules)

            # 3. Роутване към правилния pipeline за сурови факти
            if page_type == "wp_post":
                extract_from_wp_post(page, dom, store, rules)

            else if page_type == "wp_category":
                extract_from_wp_category(page, dom, store, rules)

            else if page_type == "wp_tag":
                extract_from_wp_tag(page, dom, store, rules)

            else if page_type == "wp_structural":
                extract_from_wp_structural(page, dom, store, rules)

            else if page_type == "static_author":
                extract_from_static_author(page, dom, store, rules)

            else if page_type == "static_book":
                extract_from_static_book(page, dom, store, rules)

            else if page_type == "static_exhibition":
                extract_from_static_exhibition(page, dom, store, rules)

            else if page_type == "static_gallery":
                extract_from_static_gallery(page, dom, store, rules)

            else if page_type == "ebooks_metadata":
                extract_from_ebooks(page, dom, store, rules)

            else:
                log_warning("Unknown page type", page.url)

    # 4. След обхождането: имаме сурови факти за автори, книги, произведения, изложби
    #    Сега ги обединяваме в DataTypes

    authors      = build_authors(store, rules)
    books        = build_books(store, rules)
    artworks     = build_artworks(store, rules)
    exhibitions  = build_exhibitions(store, rules)
    issues       = build_issues(store, rules)

    # 5. Запис на резултатите
    output = {
        "authors": authors,
        "books": books,
        "artworks": artworks,
        "exhibitions": exhibitions,
        "issues": issues
    }

    write_output(output, config.output_path)
    write_logs(config.logs_path)

    return output
3. Как изглежда „суровото хранилище“ (Raw Store)
pseudo
function init_raw_store():
    return {
        "authors":    [],   # списък от сурови записи за автори
        "books":      [],
        "artworks":   [],
        "exhibitions":[],
        "issues":     []
    }
Всеки extract_from_* не строи финален Author/Book, а добавя факти:

pseudo
store.authors.append({
    "source": "wp_tag",
    "name": "...",
    "biography": "...",
    "portrait_url": "...",
    "url": page.url,
    "extra": {...}
})
4. Класификация на страниците (classify_page)
pseudo
function classify_page(url, dom, rules):

    if matches_wp_post(url, dom, rules):
        return "wp_post"

    if matches_wp_category(url, dom, rules):
        return "wp_category"

    if matches_wp_tag(url, dom, rules):
        return "wp_tag"

    if matches_wp_structural(url, dom, rules):
        return "wp_structural"

    if matches_static_author(url, dom, rules):
        return "static_author"

    if matches_static_book(url, dom, rules):
        return "static_book"

    if matches_static_exhibition(url, dom, rules):
        return "static_exhibition"

    if matches_static_gallery(url, dom, rules):
        return "static_gallery"

    if matches_ebooks_metadata(url, dom, rules):
        return "ebooks_metadata"

    return "unknown"
5. Обединяване: build_authors / build_books / …
Тук влиза приоритетната логика.

pseudo
function build_authors(store, rules):

    # 1. Групиране на суровите факти по ключ (име, slug, id)
    groups = group_raw_authors(store.authors, rules)

    authors = []

    for key, raw_list in groups:

        author = init_author_object()

        # 2. Прилагане на приоритети за всяко поле
        author.name       = choose_best("name",       raw_list, rules)
        author.biography  = choose_best("biography",  raw_list, rules)
        author.portrait   = choose_best("portrait",   raw_list, rules)
        author.roles      = merge_roles(raw_list, rules)
        author.sources    = collect_sources(raw_list)

        authors.append(author)

    return authors
Същата идея за build_books, build_artworks, build_exhibitions, build_issues.

6. Функцията choose_best (сърцето на приоритетите)
pseudo
function choose_best(field, raw_list, rules):

    # пример: rules.priority_order = ["H2", "H3", "wp_tag", "wp_post", "static", "ebooks"]

    for source_type in rules.priority_order:

        candidates = filter(raw_list, r => r.source_type == source_type and r[field] is not empty)

        if not empty(candidates):
            # ако има повече от един, може да вземем първия или да приложим допълнителни правила
            return candidates[0][field]

    return null
