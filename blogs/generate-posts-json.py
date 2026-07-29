#!/usr/bin/env python3
"""
Auto-generate posts.json entries from your blog HTML files.

WHAT IT DOES
  1. Scans every .html file inside your /blogs/ folder
  2. Skips any file whose /blogs/filename.html URL is already in posts.json
  3. For each NEW file, extracts:
       - title     -> from <meta property="og:title">  (falls back to <title>)
       - desc      -> from <meta name="description">
       - url       -> /blogs/<filename>.html
       - cat       -> from <body data-theme="..."> attribute
       - date      -> from the JSON-LD "datePublished" field (falls back to the
                       visible date text in .post-meta)
       - readTime  -> from the "X min read" text inside .post-meta
       - featured  -> always false for new entries (flip manually when you want)
  4. Appends the new entries to posts.json. Existing entries are NEVER touched.
  5. Makes a posts.json.bak backup before writing, just in case.

USAGE
  1. Put this script directly INSIDE your /blogs/ folder (the same folder
     that contains posts.json and all your .html blog files)
  2. Run:  pip install beautifulsoup4        (only needed once)
  3. Run:  python3 generate_posts_json.py
  4. Re-run it any time you add new blog files — it only adds what's missing.
"""

import json
import re
from pathlib import Path
from datetime import datetime

# ---- CONFIG: adjust these two paths if your layout is different ----------
BLOGS_DIR = Path(".")   # script lives inside /blogs/, so "." IS the blogs folder
POSTS_JSON = BLOGS_DIR / "posts.json"
# ----------------------------------------------------------------------------

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit(
        "This script needs BeautifulSoup4.\n"
        "Install it with:  pip install beautifulsoup4\n"
    )


def load_existing_posts():
    if POSTS_JSON.exists():
        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def format_date(iso_date):
    """'2026-07-03' -> 'Jul 3, 2026'  (matches your existing 'Jun 29, 2026' style)"""
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def extract_post_data(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # ---- Title: prefer og:title (cleanest, no "| Rebrixe" suffix) ---------
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    else:
        raw_title = soup.title.string if soup.title else html_path.stem
        title = raw_title.split("|")[0].strip()

    # ---- Description ---------------------------------------------------------
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    # ---- Category: from <body data-theme="..."> -------------------------------
    body_tag = soup.find("body")
    cat = body_tag.get("data-theme", "").strip() if body_tag else ""

    # ---- Date: prefer JSON-LD datePublished, fall back to .post-meta text ----
    date_str = None
    for script_tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script_tag.string)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(data, dict) and "datePublished" in data:
            try:
                date_str = format_date(data["datePublished"])
            except ValueError:
                pass
            break

    if not date_str:
        meta_div = soup.find(class_="post-meta")
        if meta_div:
            match = re.search(r"([A-Z][a-z]+ \d{1,2}, \d{4})", meta_div.get_text())
            if match:
                date_str = match.group(1)

    if not date_str:
        date_str = "Unknown"

    # ---- Read time: "X min read" text inside .post-meta -----------------------
    read_time = "5 min read"
    meta_div = soup.find(class_="post-meta")
    if meta_div:
        match = re.search(r"(\d+\s*min read)", meta_div.get_text())
        if match:
            read_time = match.group(1)

    return {
        "title": title,
        "desc": desc,
        "url": f"/blogs/{html_path.name}",
        "cat": cat,
        "date": date_str,
        "readTime": read_time,
        "featured": False,
    }


def main():
    if not BLOGS_DIR.exists():
        raise SystemExit(f"Could not find '{BLOGS_DIR}' - edit BLOGS_DIR at the top of this script.")

    existing_posts = load_existing_posts()
    existing_urls = {p["url"] for p in existing_posts}

    html_files = sorted(BLOGS_DIR.glob("*"))
    new_posts = []
    skipped = []

    for html_path in html_files:
        if html_path.name.lower() == "index":
            continue

        url = f"/blogs/{html_path.name}"
        if url in existing_urls:
            continue  # already in posts.json - leave it exactly as it is

        try:
            post = extract_post_data(html_path)
            new_posts.append(post)
        except Exception as e:
            skipped.append((html_path.name, str(e)))

    if not new_posts:
        print("No new blog files found. posts.json is already up to date.")
        if skipped:
            print("\nCouldn't process these files (check manually):")
            for name, err in skipped:
                print(f"   - {name}: {err}")
        return

    # Backup before writing
    if POSTS_JSON.exists():
        backup_path = POSTS_JSON.with_suffix(".json.bak")
        backup_path.write_text(POSTS_JSON.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Backed up existing posts.json -> {backup_path.name}")

    updated_posts = existing_posts + new_posts

    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(updated_posts, f, indent=2, ensure_ascii=False)

    print(f"\nAdded {len(new_posts)} new post(s) to {POSTS_JSON}")
    for p in new_posts:
        print(f"   + {p['title']}  ({p['cat']}, {p['date']}, {p['readTime']})")

    if skipped:
        print("\nCouldn't process these files (check manually):")
        for name, err in skipped:
            print(f"   - {name}: {err}")


if __name__ == "__main__":
    main()