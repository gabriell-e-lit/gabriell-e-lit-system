<?php include __DIR__ . "/../../includes/header.php"; ?>

<div class="book-page">

    <h1 class="book-title">{{ metadata.title }}</h1>

    <div class="book-cover-block">
        {{#cover.print_url}}
        <img src="{{ cover.print_url }}" alt="{{ cover.print_alt }}" class="cover-print">
        {{/cover.print_url}}

        {{#cover.ebook_url}}
        <img src="{{ cover.ebook_url }}" alt="{{ cover.ebook_alt }}" class="cover-ebook">
        {{/cover.ebook_url}}
    </div>

    <div class="book-metadata">
        {{#metadata.author}}<p><strong>Автор:</strong> {{ metadata.author }}</p>{{/metadata.author}}
        {{#metadata.genre}}<p><strong>Жанр:</strong> {{ metadata.genre }}</p>{{/metadata.genre}}
        {{#metadata.year}}<p><strong>Година:</strong> {{ metadata.year }}</p>{{/metadata.year}}
        {{#metadata.pages}}<p><strong>Страници:</strong> {{ metadata.pages }}</p>{{/metadata.pages}}
        {{#metadata.isbn_print}}<p><strong>ISBN (хартиена):</strong> {{ metadata.isbn_print }}</p>{{/metadata.isbn_print}}
        {{#metadata.isbn_pdf}}<p><strong>ISBN (PDF):</strong> {{ metadata.isbn_pdf }}</p>{{/metadata.isbn_pdf}}
        {{#metadata.isbn_epub}}<p><strong>ISBN (EPUB):</strong> {{ metadata.isbn_epub }}</p>{{/metadata.isbn_epub}}
    </div>

    {{#intro}}
    <div class="book-intro">
        {{{ intro }}}
    </div>
    {{/intro}}

    {{#description}}
    <div class="book-description">
        {{{ description }}}
    </div>
    {{/description}}

    {{#reviews_rendered.length}}
    <h2>Рецензии</h2>
    <div class="book-reviews">
        {{#reviews_rendered}}
        <div class="review">
            <p>{{ text }}</p>
            {{#source_url}}
            <p class="review-source"><a href="{{ source_url }}">{{ source_label }}</a></p>
            {{/source_url}}
        </div>
        {{/reviews_rendered}}
    </div>
    {{/reviews_rendered.length}}

</div>

<?php include __DIR__ . "/../../includes/footer.php"; ?>
