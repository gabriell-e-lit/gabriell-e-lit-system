<?php
// =====================
// SEO
// =====================
$seo_title       = "Издателство gabriell-e-lit: Автор – {{author_name}}";
$seo_description = "{{author_description_short}}";
$canonical_url   = "https://gabriell-e-lit.com/p-izdatelstvo/authors/{{author_slug}}.php";

// =====================
// IDENTITY
// =====================
$author_id        = "{{author_id}}";
$author_slug      = "{{author_slug}}";
$author_name      = "{{author_name}}";
$author_name_orig = "{{author_name_original}}";

// =====================
// BIOGRAPHY
// =====================
$author_bio_short = "{{author_bio_short}}";
$author_bio_long  = <<<HTML
{{author_bio_long}}
HTML;

$author_quote = <<<HTML
{{author_quote}}
HTML;

// =====================
// PHOTO
// =====================
$author_photo_url = "{{author_photo}}";
$author_photo_alt = "{{author_name}} – портрет";

// =====================
// ORIGIN
// =====================
$author_birth = "{{author_birth}}";
$author_death = "{{author_death}}";
$author_country = "{{author_country}}";
$author_city    = "{{author_city}}";

// =====================
// LINKS
// =====================
$author_tag_url       = "{{author_tag_url}}";
$gallery_subcategory  = "{{gallery_subcategory}}";
$gallery_url          = "{{gallery_url}}";
$library_url          = "{{library_url}}";

// =====================
// STRUCTURE
// =====================
$structural_pages_h2 = {{structural_pages_h2_array}};
$structural_pages_h3 = {{structural_pages_h3_array}};
$first_appearance    = "{{first_appearance}}";

// =====================
// CONTENT LISTS
// =====================
$books         = {{books_array}};
$publications  = {{publications_array}};
$magazine_issues = {{magazine_issues_array}};
$exhibitions     = {{exhibitions_array}};
$collections     = {{collections_array}};

// =====================
// NAVIGATION
// =====================
$navigation_alphabetical = true;

// =====================
// VISUAL OPTIONS
// =====================
$show_quote        = true;
$show_origin       = true;
$show_gallery      = true;
$show_publications = true;
?>
