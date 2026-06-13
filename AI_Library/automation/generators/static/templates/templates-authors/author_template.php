<?php
// =====================
// АВТОМАТИЧНО ЗАРЕЖДАНЕ НА JSON ДАННИ ЗА АВТОРА
// =====================

// Извличаме slug от името на файла
$slug = basename(__FILE__, '.php');

// Път до JSON файла
$json_path = __DIR__ . '/../data/authors/' . $slug . '.json';

// Зареждаме JSON
$data = json_decode(file_get_contents($json_path), true);

// Променливи от JSON
$author_name            = $data["name"] ?? "";
$author_bio             = $data["biography"] ?? "";
$author_photo           = $data["image"] ?? null;
$author_photo_alt       = $author_name;

$books_publisher        = $data["books_publisher"] ?? [];
$books_library          = $data["books_library"] ?? [];
$publications           = $data["publications"] ?? [];
$author_tag_url         = $data["sources"]["tag_page"] ?? null;

$publication_display_mode = $data["publication_display_mode"] ?? "gallery";

// =====================
// SEO
// =====================
$title = htmlspecialchars($author_name) . " – gabriell-e-lit";
$description = mb_substr(strip_tags($author_bio), 0, 160) . "...";

// URL на страницата (генераторът може да го попълва автоматично)
$page_url = "";

// =====================
// ГЛАВНИ ИНКЛУДИ
// =====================
include __DIR__ . '/../includes/header.php';
include __DIR__ . '/../includes/top_block.php';
include __DIR__ . '/../includes/menu_top.php';

// =====================
// НАВИГАЦИЯ А–Я (мини-инклуд за конкретния поддомейн)
// =====================
include __DIR__ . '/../includes/alphabet_nav_config.php';
?>

<div class="main-content">

    <?php include __DIR__ . '/../includes/author_block.php'; ?>

    <?php include __DIR__ . '/../includes/books_block_library.php'; ?>

    <?php include __DIR__ . '/../includes/books_block.php'; ?>

    <?php include __DIR__ . '/../includes/publications_block.php'; ?>

</div>

<?php include __DIR__ . '/../includes/footer.php'; ?>
