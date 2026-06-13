<?php
// =====================
// AUTHOR v2.3 — DATA PANEL (екстракторът работи тук)
// =====================

// --- SEO ---
$seo_title = "Издателство gabriell-e-lit: Автор – {{author_name}}";
$seo_description = "{{author_description_short}}";
$page_url = "https://gabriell-e-lit.com/p-izdatelstvo/authors/{{author_slug}}.php";

// --- Required fields ---
$author_id = {{author_id}};
$author_slug = "{{author_slug}}";
$author_name = "{{author_name}}";

$author_bio = <<<HTML
{{author_bio}}
HTML;

$author_photo = "{{author_photo}}";

// --- Optional fields ---
$author_birth = "{{author_birth}}";
$author_origin = "{{author_origin}}";
$author_death = "{{author_death}}";

$author_quote = <<<HTML
{{author_quote}}
HTML;

$gallery_subcategory = "{{gallery_subcategory}}";
$author_tag_url = "{{author_tag_url}}";

// --- Structural placement ---
$structural_pages_h2 = {{structural_pages_h2_array}};
$structural_pages_h3 = {{structural_pages_h3_array}};
$first_appearance = "{{first_appearance}}";

// --- Books (array) ---
$books = {{books_array}};

// --- Publications (array) ---
$publications = {{publications_array}};

// =====================
// VIEW PANEL (визуализация — екстракторът НЕ работи тук)
// =====================

include __DIR__ . '/../../includes/header.php';
include __DIR__ . '/../../includes/top_block.php';
include __DIR__ . '/../../includes/menu_top.php';

echo '<div class="row"><div class="col-md-12"><div class="main-content">';

// Alphabet navigation
include __DIR__ . '/../includes/alphabet_nav.php';

// Author block (снимка, биография, цитат)
include __DIR__ . '/../includes/author_block.php';

// Books block
include __DIR__ . '/../includes/books_block.php';

// Publications block
include __DIR__ . '/../includes/publications_block.php';

echo '</div></div></div>';

include __DIR__ . '/../../includes/footer.php';
