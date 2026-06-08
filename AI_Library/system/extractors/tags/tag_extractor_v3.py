from bs4 import BeautifulSoup
import re

def extract_tag_page(html, tag_url):
    """
    Extracts data from a tag page in the gabriell-e-lit system.
    Works with GridWP layout (div.gridwp-grid-post).
    """

    soup = BeautifulSoup(html, "html.parser")

    # -----------------------------------------
    # 1. Extract slug from URL
    # -----------------------------------------
    slug = tag_url.rstrip("/").split("/")[-1]

    # -----------------------------------------
    # 2. Extract title (H1)
    # -----------------------------------------
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else slug

    # -----------------------------------------
    # 3. Extract Wikipedia link (if present)
    # -----------------------------------------
    wikipedia_url = ""
    wiki_link = soup.find("a", href=lambda h: h and "wikipedia.org" in h)
    if wiki_link:
        wikipedia_url = wiki_link["href"]

    # -----------------------------------------
    # 4. Extract static author page link (if present)
    # -----------------------------------------
    static_page_url = ""
    static_link = soup.find("a", href=lambda h: h and "/authors/" in h)
    if static_link:
        static_page_url = static_link["href"]

    # -----------------------------------------
    # 5. Extract injected biography (if present)
    # -----------------------------------------
    biography_short = ""
    bio_block = soup.find("div", class_="tag-biography")  # if you add a class later
    if not bio_block:
        # fallback: first <p> after H1
        if h1:
            p = h1.find_next("p")
            if p:
                biography_short = p.get_text(" ", strip=True)

    # -----------------------------------------
    # 6. Extract publications (GridWP layout)
    # -----------------------------------------
    publications = []

    posts = soup.find_all("div", class_=lambda c: c and "gridwp-grid-post" in c)

    for post in posts:
        # Title + URL
        title_tag = post.find("h3", class_="gridwp-grid-post-title")
        if not title_tag:
            continue

        a = title_tag.find("a")
        if not a:
            continue

        pub_title = a.get_text(strip=True)
        pub_url = a["href"]

        # Date
        date_tag = post.find("span", class_="gridwp-grid-post-date")
        pub_year = ""
        if date_tag:
            date_text = date_tag.get_text(strip=True)
            m = re.search(r"(\d{4})", date_text)
            if m:
                pub_year = m.group(1)

        publications.append({
            "title": pub_title,
            "url": pub_url,
            "year": pub_year
        })

    # -----------------------------------------
    # 7. Return structured data
    # -----------------------------------------
    return {
        "slug": slug,
        "tag_url": tag_url,
        "title": title,
        "wikipedia": wikipedia_url,
        "static_page_url": static_page_url,
        "biography_short": biography_short,
        "publications": publications
    }
