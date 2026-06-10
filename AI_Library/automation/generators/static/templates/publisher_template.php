<?php
// ===============================
// Publisher Template v1.0
// ===============================

$title = "Издателство gabriell-e-lit: АВТОРИ: {{name}}";
$description = "Авторска страница на {{name}} — биография, книги, публикации и информация от издателство gabriell-e-lit.";
$page_url = "{{static_page}}";

include __DIR__ . '/../../includes/header.php';
include __DIR__ . '/../../includes/top_block.php';
include __DIR__ . '/../../includes/menu_top.php';
?>

<div class="row">
    <div class="col-md-12">
        <div class="main-content">

            <h1 class="author-title">{{name}}</h1>

            <div class="author-header">
                <div class="author-photo">
                    <img src="{{photo}}" alt="{{photo_alt}}" class="img-rounded" width="180">
                </div>

                <div class="author-bio">
                    <h3>Биография</h3>
                    <p>{{biography}}</p>

                    <ul class="author-origin">
                        <li><strong>Месторождение:</strong> {{origin_city}}, {{origin_country}}</li>
                        <li><strong>Година на раждане:</strong> {{origin_birth}}</li>
                    </ul>

                    <p><strong>Таг страница:</strong>
                        <a href="{{tag_page}}" target="_blank">{{name}} в „Картини с думи и багри“</a>
                    </p>
                </div>
            </div>

            <hr>

            <!-- ========================= -->
            <!-- КНИГИ НА ИЗДАТЕЛСТВОТО -->
            <!-- ========================= -->
            <h3>Книги на издателство gabriell-e-lit</h3>

            <div class="row">
                {{#books_publisher}}
                <div class="col-md-3">
                    <div class="thumbnail">
                        <img src="{{cover}}" alt="{{title}}" class="img-rounded" style="width:100%">

                        <div class="caption">
                            <p align="center"><strong>{{title}}</strong></p>
                        </div>

                        <div class="ebook-formats">
                            {{#formats}}
                            <a href="{{url}}" target="_blank">
                                <img src="/icon-{{type}}.png" alt="{{type}}" title="{{type}}">
                            </a>
                            {{/formats}}
                        </div>
                    </div>
                </div>
                {{/books_publisher}}
            </div>

            <hr>

            <!-- ========================= -->
            <!-- ПУБЛИКАЦИИ В СПИСАНИЕТО -->
            <!-- ========================= -->
            <h3>Публикации в списание „Картини с думи и багри“</h3>

            <ul class="author-publications">
                {{#publications}}
                <li>
                    <strong>Брой {{issue}}</strong>
                    {{#title}} — {{title}}{{/title}}
                    {{#url}} <a href="{{url}}" target="_blank">прочети</a>{{/url}}
                </li>
                {{/publications}}
            </ul>

        </div>
    </div>
</div>

<?php include __DIR__ . '/../../includes/footer.php'; ?>
