def integrate_author_data(canon_data, issue_data=None, library_data=None, gallery_data=None):
    """
    Integrates all available author data into a unified AuthorModel_v3 object.

    canon_data: object from CanonExtractor_v3 (required)
    issue_data: object from IssueExtractor_v3 (optional)
    library_data: object from LibraryExtractor (optional)
    gallery_data: object from GalleryExtractor (optional)
    """

    # 1. Start with the canonical model (base)
    author = canon_data.copy()

    # ---------------------------------------------------------
    # 2. Integrate ISSUE DATA (first appearance + publications)
    # ---------------------------------------------------------
    if issue_data:
        # First appearance
        if issue_data.get("first_appearance"):
            author["structure"]["first_appearance"] = issue_data["first_appearance"]

        # Publications
        if issue_data.get("publications"):
            author["publications"] = issue_data["publications"]

        # Magazine issues
        if issue_data.get("magazine_issues"):
            author["magazine_issues"] = issue_data["magazine_issues"]

    # ---------------------------------------------------------
    # 3. Integrate LIBRARY DATA (biography + static page + photo)
    # ---------------------------------------------------------
    if library_data:
        # Biography
        if library_data.get("biography_short"):
            author["biography"]["short"] = library_data["biography_short"]

        if library_data.get("biography_long"):
            author["biography"]["long"] = library_data["biography_long"]

        # Static page URL
        if library_data.get("static_page_url"):
            author["links"]["library_url"] = library_data["static_page_url"]

        # Photo (library photo overrides canon photo)
        if library_data.get("photo_url"):
            author["photo"]["url"] = library_data["photo_url"]
            author["photo"]["alt"] = library_data.get("photo_alt", author["photo"]["alt"])

    # ---------------------------------------------------------
    # 4. Integrate GALLERY DATA (subcategory + gallery URL)
    # ---------------------------------------------------------
    if gallery_data:
        if gallery_data.get("gallery_url"):
            author["links"]["gallery_url"] = gallery_data["gallery_url"]

        if gallery_data.get("gallery_subcategory"):
            author["links"]["gallery_subcategory"] = gallery_data["gallery_subcategory"]

    # ---------------------------------------------------------
    # 5. Normalize missing fields
    # ---------------------------------------------------------
    if not author["identity"]["name_original"]:
        author["identity"]["name_original"] = author["identity"]["name_display"]

    # ---------------------------------------------------------
    # 6. Final cleanup
    # ---------------------------------------------------------
    # Remove empty lists if needed (optional)
    # Remove empty strings if needed (optional)

    return author
