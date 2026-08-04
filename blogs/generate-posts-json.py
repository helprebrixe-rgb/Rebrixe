#!/usr/bin/env python3
"""
generate_posts_json.py
════════════════════════════════════════════════════════════════════
ONE script, ONE command, run every time you add new blog files:

    python3 generate_posts_json.py

It does two things in sequence, automatically:

  STEP 1 — Scan for new blog posts (unchanged from the original workflow)
  ----------------------------------------------------------
  Scans every *.html file in this folder, finds any NOT already in
  posts.json, extracts their title/desc/category/date/readTime from
  the HTML itself, and appends new entries to posts.json. Existing
  entries are never touched. A timestamped posts.json.bak is written
  before any change.

  STEP 2 — Rebuild related-links.json (runs automatically after Step 1)
  ----------------------------------------------------------
  Recomputes related-links.json from the FULL, now-updated posts.json.

  v2 CHANGE (fixes the "everyone collapses onto 2 hub pages" bug):
  Each post now gets RELATED_COUNT = 6 related links (was 3), built
  from a CIRCULANT graph instead of a "cycle + static filler list".

  A circulant graph works like this: sort every post in a category
  into a fixed order. Post at position i links to the NEXT 6 posts
  in that same ordering (i+1, i+2, ... i+6, wrapping around back to
  the start). Every post's target list is offset by ITS OWN position
  — nobody shares the same filler list — so this is not probabilistic,
  it's a guarantee:

      every post in a category of size n > 6 gets EXACTLY 6 outgoing
      links AND exactly 6 incoming links. Provably, not "usually".

  (Why: if post at position q is targeted by posts at offsets
  q-1, q-2, ... q-6 mod n, those are 6 distinct positions whenever
  n > 6 — so in-degree = out-degree = 6, always.)

  The old version built one one-hop "cycle" (guaranteeing only 1
  incoming link per post) and then filled 2 more slots from a static,
  never-rotated per-category list — which is why almost every post's
  2nd and 3rd related link collapsed onto the same couple of "hub"
  posts sitting first in that list, and 90%+ of posts ended up with
  only 1 real incoming link despite showing 3 related cards.

  Categories too small to support their own circulant (fewer than
  RELATED_COUNT + 1 posts) are folded into one merged pool so the
  guarantee still holds. See build_related_links() below.

════════════════════════════════════════════════════════════════════
HOW A NEW POST'S HTML SHOULD LOOK (paste this in, no manual linking)
════════════════════════════════════════════════════════════════════
  <section class="related-posts" aria-label="Related tools and guides" id="related-tools">
    <h2>Related tools and guides</h2>
    <div class="related-grid" id="related-grid"></div>
  </section>

  ...and before </body>:
  

That's it — this script's Step 2 fills in #related-grid at page-load
time via related-posts.js, which reads related-links.json. No change
needed in related-posts.js for the move from 3 to 6 links — it just
renders whatever array is in related-links.json.

════════════════════════════════════════════════════════════════════
ONE-TIME step for your EXISTING ~200 posts (only needed once, ever)
════════════════════════════════════════════════════════════════════
Your existing posts still have hand-picked related-links HTML baked
in. Run this once to swap them all for the empty shell above:

    python3 generate_posts_json.py retrofit .
    python3 generate_posts_json.py retrofit . --dry-run   (preview first)

After that one-time retrofit, you never run "retrofit" again — new
posts get written with the empty shell directly, and every normal
run of this script (no arguments) keeps related-links.json current.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

# ---- CONFIG ---------------------------------------------------------------
# Anchored to the script's own location, NOT the shell's current directory.
BLOGS_DIR = Path(__file__).resolve().parent
POSTS_JSON = BLOGS_DIR / "posts.json"
RELATED_LINKS_JSON = BLOGS_DIR / "related-links.json"
# ----------------------------------------------------------------------------

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit(
        "This script needs BeautifulSoup4.\n"
        "Install it with:  pip install beautifulsoup4\n"
    )


# ════════════════════════════════════════════════════════════════════
# STEP 1: scan HTML files, add new entries to posts.json
# (unchanged from the original generate_posts_json.py)
# ════════════════════════════════════════════════════════════════════

def normalize_url(url: str) -> str:
    """Make URL comparisons robust to trivial formatting differences
    (leading slash, trailing slash, case, a stray .html extension) so the
    same post isn't added twice just because it was written slightly
    differently somewhere. The site serves clean URLs (no .html), so this
    also protects against a URL that accidentally has .html baked in
    being treated as a different page."""
    u = url.strip().lower()
    if not u.startswith("/"):
        u = "/" + u
    u = u.rstrip("/")
    if u.endswith(".html"):
        u = u[: -len(".html")]
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
        "url": f"/blogs/{html_path.stem}",
        "cat": cat,
        "date": date_str,
        "readTime": read_time,
        "featured": False,
    }


def scan_and_update_posts_json():
    """Returns the full, up-to-date list of posts (existing + newly added),
    whether or not anything actually changed this run."""
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
        return existing_posts

    new_posts = []
    skipped = []
    seen_this_run = {}  # normalized url -> filename, to catch in-batch dupes

    for html_path in html_files:
        if html_path.stem.lower() == "index":
            print(f"  - {html_path.name}: skipped (index page)")
            continue

        url = f"/blogs/{html_path.stem}"
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
        return existing_posts

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

    return updated_posts
