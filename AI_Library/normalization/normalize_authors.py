import json
import os
import re
import urllib.parse
from collections import defaultdict, Counter

INPUT_RAW = "database/json/authors_raw.json"
OUTPUT_V2 = "database/json/authors_v2.json"

def load_authors_raw(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- НОРМАЛИЗАЦИЯ НА ИМЕНА ---

TITLES_PAT = re.compile(
    r"\b(д-р|др\.?|prof\.?|проф\.?|професор|доц\.?|акад\.?|D R|Dr\.?|DR)\b",
    flags=re.IGNORECASE
)

def decode_if_urlencoded(name):
    # ако съдържа % или +, опитваме декодиране
    if "%" in name or "+" in name:
        try:
            return urllib.parse.unquote(name)
        except Exception:
            return name
    return name

def strip_titles(name):
    name = TITLES_PAT.sub("", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def normalize_case(name):
    # ако е на кирилица и е с главни букви → правим „Нормален Регистър“
    if re.search(r"[А-Я]", name) and name.upper() == name:
        name = name.title()
    return name.strip()

def normalize_name_raw(name):
    if not name:
        return None
    name = decode_if_urlencoded(name)
    name = strip_titles(name)
    name = normalize_case(name)
    return name

def is_cyrillic(s):
    return bool(re.search(r"[А-Яа-я]", s))

def choose_display_name(names):
    """
    Взимаме най-често срещаното име; ако има кирилица и латиница,
    предпочитаме кирилица.
    """
    names = [n for n in names if n]
    if not names:
        return None
    counts = Counter(names)
    # отделяме кирилските
    cyr = [n for n in names if is_cyrillic(n)]
    if cyr:
        c_counts = Counter(cyr)
        return c_counts.most_common(1)[0][0]
    return counts.most_common(1)[0][0]

# --- СЛУГОВЕ И ГРУПИРАНЕ ---

def fallback_slug_from_name(name):
    if not name:
        return None
    # транслитерация не правим тук – само груб slug
    s = name.strip().lower()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s)
    return s or None

def get_group_key(author):
    slug = author.get("slug")
    name = normalize_name_raw(author.get("name") or "")
    if slug:
        return ("slug", slug)
    if name:
        return ("name", name.lower())
    return ("name", None)

# --- ИЗВЛИЧАНЕ НА ИНФО ОТ RAW ЗАПИСИТЕ ---

def extract_issue_label(issue_id):
    # "1-2019" → "1/2019"
    if not issue_id:
        return None
    m = re.match(r"(\d+)-(\d+)", issue_id)
    if not m:
        return issue_id
    return f"{m.group(1)}/{m.group(2)}"

def collect_authors(authors_raw):
    groups = defaultdict(list)
    for a in authors_raw:
        key = get_group_key(a)
        groups[key].append(a)
    return groups

# --- ВЪНШНИ ВРЪЗКИ ---

def build_external_links(slug):
    if not slug:
        return {}
    links = {}

    # издателство
    links["publisher"] = f"https://gabriell-e-lit.com/p-izdatelstvo/authors/{slug}.php"

    # галерия – трите възможни варианта
    links["gallery_e_gallery"] = f"https://e-gallery.gabriell-e-lit.com/authors/e-gallery/{slug}.php"
    links["gallery_ksdb"] = f"https://e-gallery.gabriell-e-lit.com/authors/kartini-s-dumi-i-bagri/{slug}.php"
    links["gallery_gabriell"] = f"https://e-gallery.gabriell-e-lit.com/authors/gabriell-e-lit/{slug}.php"

    # е-библиотека
    links["library"] = f"https://e-library.gabriell-e-lit.com/authors/{slug}.php"

    # Wikipedia – ще се попълва ръчно или по-късно автоматично
    links["wikipedia"] = None

    return links

# --- ГЕНЕРИРАНЕ НА БИОГРАФИЯ И HTML ---

def merge_bios(bios):
    bios = [b.strip() for b in bios if b and b.strip()]
    if not bios:
        return ""
    # засега – просто взимаме най-дългата; по-късно можем да правим интелигентно съкращаване
    bios.sort(key=len, reverse=True)
    return bios[0]

def build_intro(name, roles):
    # 1–2 изречения, bold
    role_part = ""
    if roles:
        role_part = " " + ", ".join(sorted(set(roles)))
    return f"{name} е{role_part}."

def build_main_bio_text(merged_bio, first_issue_label):
    # засега използваме наличната биография + едно изречение за списанието
    parts = []
    if merged_bio:
        parts.append(merged_bio.strip())
    if first_issue_label:
        parts.append(f"Автор в списание „Картини с думи и багри“ от брой {first_issue_label}.")
    return " ".join(parts)

def build_external_links_html(external_links, first_issue_url, first_issue_label):
    items = []

    if external_links.get("wikipedia"):
        items.append(f'<li><a href="{external_links["wikipedia"]}">Wikipedia</a></li>')

    if first_issue_url and first_issue_label:
        items.append(
            f'<li><a href="{first_issue_url}">Първа поява в списанието (брой {first_issue_label})</a></li>'
        )

    if external_links.get("publisher"):
        items.append(f'<li><a href="{external_links["publisher"]}">Авторска страница в издателството</a></li>')

    if external_links.get("gallery_e_gallery") or external_links.get("gallery_ksdb") or external_links.get("gallery_gabriell"):
        # показваме една обща връзка към галерията – по-късно можем да я уточним
        items.append('<li>Авторска страница в галерията (e-gallery.gabriell-e-lit.com)</li>')

    if external_links.get("library"):
        items.append('<li>Авторска страница в е‑библиотеката (e-library.gabriell-e-lit.com)</li>')

    if not items:
        return ""

    return "<h4>Външни връзки</h4>\n<ul>\n" + "\n".join(items) + "\n</ul>"

def build_meta_description(name):
    return (
        f"{name} – кратка биография, творчество и участие в списание „Картини с думи и багри“. "
        "Основни акценти от литературния/художествения му/ѝ път."
    )

def build_first_issue_url(issue_id):
    if not issue_id:
        return None
    return f"https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie-authors-{issue_id}/"

def main():
    if not os.path.exists(INPUT_RAW):
        print(f"Липсва {INPUT_RAW}")
        return

    authors_raw = load_authors_raw(INPUT_RAW)
    groups = collect_authors(authors_raw)

    authors_v2 = {}

    for (key_type, key_val), records in groups.items():
        # събираме всички варианти на името
        names = [normalize_name_raw(r.get("name") or "") for r in records]
        display_name = choose_display_name(names)
        if not display_name:
            # fallback
            display_name = names[0] if names else "Неизвестен автор"

        # slug
        slugs = [r.get("slug") for r in records if r.get("slug")]
        slug = slugs[0] if slugs else fallback_slug_from_name(display_name)

        # роли
        roles = set()
        for r in records:
            for role in r.get("roles") or []:
                roles.add(role)

        # броеве
        issues = set()
        first_issue_id = None
        for r in records:
            issue_id = r.get("issue_id")
            if issue_id:
                issues.add(issue_id)
                if not first_issue_id:
                    first_issue_id = issue_id
                else:
                    # избираме най-ранния по година/номер, ако можем
                    m1 = re.match(r"(\d+)-(\d+)", first_issue_id or "")
                    m2 = re.match(r"(\d+)-(\d+)", issue_id)
                    if m1 and m2:
                        y1, y2 = int(m1.group(2)), int(m2.group(2))
                        n1, n2 = int(m1.group(1)), int(m2.group(1))
                        if (y2 < y1) or (y2 == y1 and n2 < n1):
                            first_issue_id = issue_id

        first_issue_label = extract_issue_label(first_issue_id)
        first_issue_url = build_first_issue_url(first_issue_id)

        # биографии
        bios = [r.get("bio") for r in records]
        merged_bio = merge_bios(bios)

        # външни връзки (по slug)
        external_links = build_external_links(slug)

        # HTML за тага
        intro = build_intro(display_name, roles)
        main_bio_text = build_main_bio_text(merged_bio, first_issue_label)
        external_html = build_external_links_html(external_links, first_issue_url, first_issue_label)

        bio_html_parts = [
            f"<h4>{display_name}</h4>",
            f"<p><strong>{intro}</strong></p>",
        ]
        if main_bio_text:
            bio_html_parts.append(f"<p>{main_bio_text}</p>")
        if external_html:
            bio_html_parts.append(external_html)

        bio_html = "\n\n".join(bio_html_parts)

        meta_description = build_meta_description(display_name)
        focus_keyword = display_name

        authors_v2[slug] = {
            "name": display_name,
            "slug": slug,
            "issues": sorted(issues),
            "roles": sorted(roles),
            "first_issue_id": first_issue_id,
            "first_issue_label": first_issue_label,
            "first_issue_url": first_issue_url,
            "bio_raw": merged_bio,
            "bio_html": bio_html,
            "external_links": external_links,
            "seo": {
                "focus_keyword": focus_keyword,
                "meta_description": meta_description,
            },
        }

    os.makedirs(os.path.dirname(OUTPUT_V2), exist_ok=True)
    with open(OUTPUT_V2, "w", encoding="utf-8") as f:
        json.dump(authors_v2, f, ensure_ascii=False, indent=4)

    print(f"Готово. Създаден е {OUTPUT_V2}.")

if __name__ == "__main__":
    main()