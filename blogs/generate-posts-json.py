#!/usr/bin/env python3
"""
Auto-generate posts.json entries from your blog HTML files.

WHAT IT DOES
  1. Scans every *.html file inside your /blogs/ folder (script location, not
     wherever you happen to run it from)
  2. Skips any file whose /blogs/filename.html URL is already in posts.json,
     using a NORMALIZED comparison (case-insensitive, slash/extension tolerant)
     so hand-edited or older-format entries don't cause duplicates
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
  5. Makes a timestamped posts.json.bak backup before writing, every run that
     changes something (old backups are never overwritten).
  6. Prints a full report: what it found, what it skipped, and WHY, so
     failures are visible instead of silent.

USAGE
  1. Put this script directly INSIDE your /blogs/ folder (the same folder
     that contains posts.json and all your .html blog files)
  2. Run:  pip install beautifulsoup4        (only needed once)
  3. Run:  python3 generate_posts_json.py
  4. Re-run it any time you add new blog files - it only adds what's missing.

FIXES vs the previous version
  - BLOGS_DIR now resolves to the script's own folder (Path(__file__).parent),
    not the shell's current working directory. Running the script from
    somewhere else used to silently scan an empty/wrong folder, which is the
    most likely reason a "fresh start" run reported "no new blogs added."
  - Only *.html files are globbed now, instead of every file in the folder
    (which used to include posts.json, the .bak file, and the script itself,
    relying on exceptions to filter them out silently).
  - Existing-entry matching is now normalized (case-insensitive, tolerant of
    a missing leading slash or trailing slash) instead of a raw string ==
    comparison, so entries that were added by hand or by an older script
    format are correctly recognized as duplicates instead of being
    re-added.
  - Duplicate check also runs WITHIN the current batch of new posts, so if
    two HTML files somehow map to the same URL you get a warning instead of
    two entries.
  - Backups are timestamped (posts.json.20260729-153000.bak) so re-running
    never clobbers your previous backup, and you always have a trail.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# ---- CONFIG ---------------------------------------------------------------
# Anchored to the script's own location, NOT the shell's current directory.
# This is the fix for the "ran from scratch, found nothing" failure.
BLOGS_DIR = Path(__file__).resolve().parent
POSTS_JSON = BLOGS_DIR / "posts.json"
# ----------------------------------------------------------------------------

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit(
        "This script needs BeautifulSoup4.\n"
        "Install it with:  pip install beautifulsoup4\n"
    )


def normalize_url(url: str) -> str:
    """Make URL comparisons robust to trivial formatting differences
    (leading slash, trailing slash, case) so the same post isn't added twice
    just because it was written slightly differently somewhere."""
    u = url.strip().lower()
    if not u.startswith("/"):
        u = "/" + u
    u = u.rstrip("/")
    return u


def load_existing_posts():
    if POSTS_JSON.exists():
        try:
            with open(POSTS_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise SystemExit(
                        f"'{POSTS_JSON.name}' does not contain a JSON array at the "
                        f"top level - refusing to touch it. Please check the file."
                    )
                return data
        except json.JSONDecodeError as e:
            raise SystemExit(
                f"'{POSTS_JSON.name}' exists but isn't valid JSON ({e}).\n"
                f"Fix or remove it before running this script."
            )
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

    # ---- Description -----------------------------------------------------
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    # ---- Category: from <body data-theme="..."> ---------------------------
    body_tag = soup.find("body")
    cat = body_tag.get("data-theme", "").strip() if body_tag else ""

    # ---- Date: prefer JSON-LD datePublished, fall back to .post-meta text --
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

    # ---- Read time: "X min read" text inside .post-meta --------------------
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
    print(f"Blogs folder : {BLOGS_DIR}")
    print(f"posts.json   : {POSTS_JSON}\n")

    if not BLOGS_DIR.exists():
        raise SystemExit(f"Could not find '{BLOGS_DIR}'.")

    existing_posts = load_existing_posts()
    existing_urls_norm = {normalize_url(p["url"]) for p in existing_posts if "url" in p}

    # Only *.html files - explicitly. This stops posts.json / posts.json.bak /
    # the script itself / images / css from ever being handed to the HTML parser.
    html_files = sorted(BLOGS_DIR.glob("*.html"))

    print(f"Found {len(html_files)} .html file(s) in the blogs folder.")
    if not html_files:
        print(
            "\nNo .html files were found here. If you expected some, double "
            "check this really is the folder your blog files live in - this "
            "script always looks next to itself, not wherever you ran it from."
        )
        return

    new_posts = []
    skipped = []
    seen_this_run = {}  # normalized url -> filename, to catch in-batch dupes

    for html_path in html_files:
        if html_path.stem.lower() == "index":
            print(f"  - {html_path.name}: skipped (index page)")
            continue

        url = f"/blogs/{html_path.name}"
        norm = normalize_url(url)

        if norm in existing_urls_norm:
            print(f"  - {html_path.name}: already in posts.json, skipped")
            continue

        if norm in seen_this_run:
            skipped.append((
                html_path.name,
                f"same URL as '{seen_this_run[norm]}' already queued this run - "
                f"skipped to avoid creating a duplicate",
            ))
            continue

        try:
            post = extract_post_data(html_path)
        except Exception as e:
            skipped.append((html_path.name, str(e)))
            continue

        new_posts.append(post)
        seen_this_run[norm] = html_path.name
        print(f"  + {html_path.name}: queued as new entry")

    if not new_posts:
        print("\nNo new blog files found. posts.json is already up to date.")
        if skipped:
            print("\nCouldn't process these files (check manually):")
            for name, err in skipped:
                print(f"   - {name}: {err}")
        return

    # Timestamped backup - never overwrites a previous backup.
    if POSTS_JSON.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = BLOGS_DIR / f"posts.json.{stamp}.bak"
        backup_path.write_text(POSTS_JSON.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"\nBacked up existing posts.json -> {backup_path.name}")

    updated_posts = existing_posts + new_posts

    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(updated_posts, f, indent=2, ensure_ascii=False)

    print(f"\nAdded {len(new_posts)} new post(s) to {POSTS_JSON.name}")
    for p in new_posts:
        print(f"   + {p['title']}  ({p['cat']}, {p['date']}, {p['readTime']})")

    if skipped:
        print("\nCouldn't process these files (check manually):")
        for name, err in skipped:
            print(f"   - {name}: {err}")


if __name__ == "__main__":
    main()