<?php
// =====================
// SEO
// =====================
$seo_title       = "Издателство gabriell-e-lit: Заглавие – Автор";
$seo_description = "Кратко SEO описание (2–3 изречения).";
$canonical_url   = "https://gabriell-e-lit.com/p-izdatelstvo/poezia/novakniga.php";

// =====================
// ОСНОВНИ ДАННИ
// =====================
$book_title   = "Заглавие на книгата";
$book_author  = "Име на автора";
$book_genre   = "поезия / проза / документална проза / сборник";
$book_year    = "2026";
$book_pages   = "250";

$book_binding_print = "мека";
$book_format_print  = "А5";

$book_isbn_print = "978-619-XXXX-XX-X";
$book_isbn_pdf   = "978-619-XXXX-XX-X";
$book_isbn_epub  = "978-619-XXXX-XX-X";

// =====================
// КОРИЦИ
// =====================
$cover_ebook_url = "https://e-books.gabriell-e-lit.com/.../cover.jpg";
$cover_ebook_alt = "Заглавие – електронна корица";

$cover_print_url = "https://gabriell-e-lit.com/p-izdatelstvo/books/covers/print.jpg";
$cover_print_alt = "Заглавие – печатна корица";

// =====================
// ФОРМАТИ
// =====================
$book_pdf_url   = "https://e-books.gabriell-e-lit.com/.../Book.pdf";
$book_epub_url  = "https://e-books.gabriell-e-lit.com/.../Book.epub";
$book_pbook_url = "https://e-books.gabriell-e-lit.com/.../Book.pdf"; // ако има печатно издание
$book_audio_url = ""; // опционално

// =====================
// ВРЪЗКИ
// =====================
$book_author_page_url = "https://gabriell-e-lit.com/p-izdatelstvo/authors/Author.php";
$book_tag_url         = "https://gabriell-e-lit.com/izdatelstvo/tag/ime-na-knigata/";
$book_registry_url    = "https://booksinprint.bg/Publication/Details/...";
$book_goodreads_url   = ""; // опционално
$book_bookstore_url   = ""; // опционално

// =====================
// ТЕКСТОВЕ
// =====================
$book_intro       = "Кратко интро (2–4 изречения).";
$book_description = "Дълго описание или откъс.";

// =====================
// РЕЦЕНЗИИ
// =====================
$book_reviews = [
    [
        "text"         => "Текст на рецензия.",
        "source_url"   => "https://gabriell-e-lit.com/izdatelstvo/tag/ime-na-knigata/",
        "source_label" => "Публикации в сп. „Картини с думи и багри“"
    ]
];

// =====================
// НАВИГАЦИЯ (UX слой)
// =====================
$navigation_alphabetical = true;  // винаги за p-izdatelstvo
$navigation_genre        = false; // опционално

// =====================
// ВИЗУАЛЕН СЛОЙ
// =====================
$include_book_cell = true; // включва IdealBookCell
?>
