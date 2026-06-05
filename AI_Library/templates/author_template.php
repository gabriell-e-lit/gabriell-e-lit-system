<?php
// =====================
// АВТОМАТИЧНО ЗАРЕЖДАНЕ НА JSON ДАННИ ЗА АВТОРА
// =====================

// Определяме slug-а от името на файла
$slug = basename(__FILE__, '.php');

// Път до JSON файла
$json_path = __DIR__ . '/../data/authors/' . $slug . '.json';

// Зареждаме JSON
$data = json_decode(file_get_contents($json_path), true);

// Променливи от JSON
$author_name   = $data["name"] ?? "";
$author_bio    = $data["biography"] ?? "";
$author_photo  = $data["image"] ?? null;
$author_photo_alt = $author_name;

$wikipedia     = $data["wikipedia"] ?? null;
$books         = $data["books"] ?? [];
$roles         = $data["roles"] ?? [];
$sources       = $data["sources"] ?? [];
$author_tag_url = $sources["tag_page"] ?? null;

// =====================
// SEO
// =====================
$title = "е-Библиотека gabriell-e-lit: Автор – " . htmlspecialchars($author_name);
$description = mb_substr(strip_tags($author_bio), 0, 160) . "...";
$page_url = "https://e-library.gabriell-e-lit.com/authors/" . $slug . ".php";

include __DIR__ . '/../includes/header.php';
include __DIR__ . '/../includes/top_block.php';
include __DIR__ . '/../includes/menu_top.php';
?>

<div class="row">
    <div class="col-md-12">
        <div class="main-content">

            <?php include __DIR__ . '/../includes/author_block.php'; ?>

            <hr/>

            <h3>Книги в е-Библиотека gabriell-e-lit</h3>
            <div class="row">
                <?php if (!empty($books)) : ?>
                    <?php foreach ($books as $book) : ?>
                        <p>
                            <a href="<?php echo htmlspecialchars($book["url"]); ?>" target="_blank">
                                <?php echo htmlspecialchars($book["title"]); ?>
                                (<?php echo htmlspecialchars($book["format"]); ?>)
                            </a>
                        </p>
                    <?php endforeach; ?>
                <?php else : ?>
                    <p>Няма налични книги.</p>
                <?php endif; ?>
            </div>

            <br/>

            <h3>Публикации в списание „Картини с думи и багри“</h3>
            <?php if (!empty($author_tag_url)) : ?>
                <p>
                    <a href="<?php echo htmlspecialchars($author_tag_url); ?>" target="_blank">
                        Виж всички публикации →
                    </a>
                </p>
            <?php else : ?>
                <p>Няма налични публикации.</p>
            <?php endif; ?>

        </div>
    </div>
</div>

<?php include __DIR__ . '/../includes/footer.php'; ?>
