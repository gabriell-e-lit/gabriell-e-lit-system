import json
import os
import re
import urllib.parse
from collections import defaultdict, Counter

INPUT_RAW = "database/json/authors_raw.json"
OUTPUT_V2 = "database/json/authors_v2.json"

# --- помощни функции за имена ---

TITLES_PAT = re.compile(
    r"\b(д-р|др\.?|prof\.?|проф\.?|професор|доц\.?|акад\.?|D R|Dr\.?|DR)\b",
    flags=re.IGNORECASE
)

SECTION_NAME_PAT = re.compile(
    r"(автори|през\s*20\d{2}|издателството|стават|биографии)",
    flags=re.IGNORECASE
)

def decode_if_urlencoded(name: str) -> str:
    if "%" in name or "+" in name:
        try:
            return urllib.parse.unquote(name)
        except Exception:
            return name
    return name

def strip_titles(name: str) -> str:
    name = TITLES_PAT.sub("", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def normalize_case(name: str) -> str:
    if re.search(r"[А-Я]", name) and name.upper() == name:
        name = name.title()
    return name.strip()

def normalize_name_raw(name: str | None) -> str | None:
    if not name:
        return None
    name = decode_if_urlencoded(name)
    name = strip_titles(name)
    name = normalize_case(name)
    return name

def is_cyrillic(s: str) -> bool:
    return bool(re.search(r"[А-Яа-я]", s))

def choose_display_name(names: list[str]) -> str | None:
    names = [n for n in names if n]
    if not names:
        return None
    counts = Counter(names)
    cyr = [n for n in names if is_cyrillic(n)]
    if cyr:
        c_counts = Counter(cyr)
        return c_counts.most_common(1)[0][0]
    return counts.most_common(1)[0][0]

def fallback_slug_from_name(name: str | None) -> str | None:
    if not name:
        return None
    s = name.strip().lower()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s)
    return s or None

def get_group_key(author: dict) -> tuple[str, str | None]:
    slug = author.get("slug")
    name = normalize_name_raw(author.get("name") or "")
    if slug:
        return ("slug", slug)
    if name:
        return ("name", name.lower())
    return ("name", None)

def extract_issue_label(issue_id: str | None) -> str | None:
    if not issue_id:
        return None
    m = re.match(r"(\d+)-(\d+)", issue_id)
    if not m:
        return issue_id
    return f"{m.group(1)}/{m.group(2)}"

def collect_authors(authors_raw: list[dict]) -> dict[tuple[str, str | None], list[dict]]:
    groups: dict[tuple[str, str | None], list[dict]] = defaultdict(list)
    for a in authors_raw:
        key = get_group_key(a)
        groups[key].append(a)
    return groups

# --- външни връзки ---

def build_external_links(slug: str | None) -> dict:
    if not slug:
        return {
            "publisher": None,
            "gallery_e_gallery": None,
            "gallery_ksdb": None,
            "gallery_gabriell": None,
            "library": None,
            "wikipedia": None,
        }

    return {
        "publisher": f"https://gabriell-e-lit.com/p-izdatelstvo/authors/{slug}.php",
        "gallery_e_gallery": f"https://e-gallery.gabriell-e-lit.com/authors/e-gallery/{slug}.php",
        "gallery_ksdb": f"https://e-gallery.gabriell-e-lit.com/authors/kartini-s-dumi-i-bagri/{slug}.php",
        "gallery_gabriell": f"https://e-gallery.gabriell-e-lit.com/authors/gabriell-e-lit/{slug}.php",
        "library": f"https://e-library.gabriell-e-lit.com/authors/{slug}.php",
        "wikipedia": None,
    }

# --- биографии и HTML ---

def merge_bios(bios: list[str | None]) -> str:
    bios = [b.strip() for b in bios if b and b.strip()]
    if not bios:
        return ""
    bios.sort(key=len, reverse=True)
    return bios[0]

def extract_name_from_bio(bio: str) -> str | None:
    """
    Грубо: взимаме първото изречение и първите 2–3 думи като кандидат-име.
    """
    if not bio:
        return None
    first_sentence = re.split(r"[.!?]", bio, maxsplit=1)[0]
    words = first_sentence.strip().split()
    if not words:
        return None
    # до 3 думи – често „Име Фамилия“, „Име Презиме Фамилия“
    candidate = " ".join(words[:3])
    # махаме запетаи и др.
    candidate = re.sub(r"[,\u2013\-]+$", "", candidate).strip()
    # ако няма интервал → вероятно не е име
    if " " not in candidate:
        return None
    return candidate

def build_intro(name: str, roles: list[str]) -> str:
    role_part = ""
    if roles:
        role_part = " " + ", ".join(sorted(set(roles)))
    return f"{name} е{role_part}."

def build_main_bio_text(merged_bio: str, first_issue_label: str | None) -> str:
    parts: list[str] = []
    if merged_bio:
        parts.append(merged_bio.strip())
    if first_issue_label:
        parts.append(f"Автор в списание „Картини с думи и багри“ от брой {first_issue_label}.")
    return " ".join(parts)

def build_external_links_html(external_links: dict, first_issue_url: str | None, first_issue_label: str | None) -> str:
    items: list[str] = []

    if external_links.get("wikipedia"):
        items.append(f'<li><a href="{external_links["wikipedia"]}">Wikipedia</a></li>')

    if first_issue_url and first_issue_label:
        items.append(
            f'<li><a href="{first_issue_url}">Първа поява в списанието (брой {first_issue_label})</a></li>'
        )

    if external_links.get("publisher"):
        items.append(f'<li><a href="{external_links["publisher"]}">Авторска страница в издателството</a></li>')

    if any(external_links.get(k) for k in ("gallery_e_gallery", "gallery_ksdb", "gallery_gabriell")):
        items.append('<li>Авторска страница в галерията (e-gallery.gabriell-e-lit.com)</li>')

    if external_links.get("library"):
        items.append('<li>Авторска страница в е‑библиотеката (e-library.gabriell-e-lit.com)</li>')

    if not items:
        return ""

    return "<h4>Външни връзки</h4>\n<ul>\n" + "\n".join(items) + "\n</ul>"

def build_meta_description(name: str) -> str:
    return (
        f"{name} – кратка биография, творчество и участие в списание „Картини с думи и багри“. "
        "Основни акценти от литературния/художествения му/ѝ път."
    )

def build_first_issue_url(issue_id: str | None) -> str | None:
    if not issue_id:
        return None
    return f"https://gabriell-e-lit.com/izdatelstvo/kartini-s-dumi-i-bagri-spisanie-authors-{issue_id}/"

# --- основна логика ---

def load_authors_raw(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def is_section_like_name(name: str | None) -> bool:
    if not name:
        return False
    return bool(SECTION_NAME_PAT.search(name))

def main():
    if not os.path.exists(INPUT_RAW):
        print(f"Липсва {INPUT_RAW}")
        return

    authors_raw = load_authors_raw(INPUT_RAW)
    groups = collect_authors(authors_raw)

    authors_v2: dict[str, dict] = {}

    for (key_type, key_val), records in groups.items():
        # събираме всички варианти на името
        raw_names = [r.get("name") or "" for r in records]
        norm_names = [normalize_name_raw(n) for n in raw_names]
        display_name = choose_display_name([n for n in norm_names if n])

        # ако името прилича на секционно заглавие → по-добре да пропуснем този „автор“
        if display_name and is_section_like_name(display_name):
            # тези записи най-вероятно са „Автори на издателството през 2019 г.“ и подобни
            continue

        if not display_name:
            display_name = norm_names[0] if norm_names and norm_names[0] else "Неизвестен автор"

        # slug – не сливаме различни slug-ове, просто взимаме първия наличен
        slugs = [r.get("slug") for r in records if r.get("slug")]
        slug = slugs[0] if slugs else fallback_slug_from_name(display_name)

        # роли
        roles_set = set()
        for r in records:
            for role in r.get("roles") or []:
                roles_set.add(role)
        roles = sorted(roles_set)

        # броеве и първи брой
        issues_set = set()
        first_issue_id: str | None = None
        for r in records:
            issue_id = r.get("issue_id")
            if issue_id:
                issues_set.add(issue_id)
                if not first_issue_id:
                    first_issue_id = issue_id
                else:
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

        # проверка за несъответствие между име и биография
        bio_name_candidate = extract_name_from_bio(merged_bio) if merged_bio else None
        bio_mismatch = False
        if bio_name_candidate and display_name:
            # ако и двете са на кирилица и се различават значимо → mismatch
            if is_cyrillic(bio_name_candidate) and is_cyrillic(display_name):
                if bio_name_candidate.split()[0] != display_name.split()[0]:
                    bio_mismatch = True

        # външни връзки
        external_links = build_external_links(slug)

        # HTML
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

        authors_v2[slug or display_name] = {
            "name": display_name,
            "slug": slug,
            "issues": sorted(issues_set),
            "roles": roles,
            "first_issue_id": first_issue_id,
            "first_issue_label": first_issue_label,
            "first_issue_url": first_issue_url,
            "bio_raw": merged_bio,
            "bio_html": bio_html,
            "bio_mismatch": bio_mismatch,
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