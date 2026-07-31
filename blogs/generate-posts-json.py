#!/usr/bin/env python3
"""
generate_posts_json.py
════════════════════════════════════════════════════════════════════
ONE script, ONE command, run every time you add new blog files:

    python3 generate_posts_json.py

It does two things in sequence, automatically:

  STEP 1 — Scan for new blog posts (your original workflow, unchanged)
  ----------------------------------------------------------
  Scans every *.html file in this folder, finds any NOT already in
  posts.json, extracts their title/desc/category/date/readTime from
  the HTML itself, and appends new entries to posts.json. Existing
  entries are never touched. A timestamped posts.json.bak is written
  before any change.

  STEP 2 — Rebuild related-links.json (new — runs automatically after Step 1)
  ----------------------------------------------------------
  Recomputes related-links.json from the FULL, now-updated posts.json
  — guaranteeing every single post (old and new) has at least one
  incoming "related post" link, so nothing can silently become an
  orphan page. This is the file /blogs/related-posts.js reads on each
  post page to render its 3 related-post cards.

You never need to run these as two separate commands, and you never
need to hand-pick related links for a new post — just make sure its
HTML file has the empty related-posts shell (see the snippet near the
bottom of this file) and this script fills it in.

WHY related-links.json GETS REBUILT FROM SCRATCH EVERY RUN
Guaranteeing "every post has an incoming link" requires looking at
ALL posts together (to build link cycles per category) — it can't be
done by patching in just the new posts. So each run recomputes the
whole map fresh from the complete posts.json. Existing posts' related
links CAN shift slightly when new posts join their category — that's
expected, not a bug, and it's what keeps the zero-orphans guarantee
true as the site grows. A "✅ zero orphans" line (or an explicit
warning) prints after every run so you can see the guarantee held.

════════════════════════════════════════════════════════════════════
HOW A NEW POST'S HTML SHOULD LOOK (paste this in, no manual linking)
════════════════════════════════════════════════════════════════════
  <section class="related-posts" aria-label="Related tools and guides" id="related-tools">
    <h2>Related tools and guides</h2>
    <div class="related-grid" id="related-grid"></div>
  </section>

  ...and before </body>:
  <script src="/blogs/related-posts.js"></script>

That's it — this script's Step 2 fills in #related-grid at page-load
time via related-posts.js, which reads related-links.json.

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
from collections import defaultdict

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
# (unchanged from your original generate_posts_json.py)
# ════════════════════════════════════════════════════════════════════

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


# ════════════════════════════════════════════════════════════════════
# STEP 2: rebuild related-links.json from the full posts list
# (runs automatically after Step 1, every time this script is run)
# ════════════════════════════════════════════════════════════════════

RELATED_COUNT = 3
MIN_CATEGORY_SIZE_FOR_OWN_CYCLE = 3  # smaller categories fold into a fallback cycle


def build_cycle_links(urls):
    """A -> B -> C -> ... -> back to A. Guarantees every post has >=1 incoming link."""
    links = {}
    n = len(urls)
    if n == 0:
        return links
    if n == 1:
        links[urls[0]] = []  # can't link to itself
        return links
    for i, url in enumerate(urls):
        links[url] = [urls[(i + 1) % n]]
    return links


def fill_to_three(url, cycle_next, same_category_pool, global_recent_pool):
    chosen, used = [], set()

    for u in cycle_next:
        if u != url and u not in used:
            chosen.append(u)
            used.add(u)

    for u in same_category_pool:
        if len(chosen) >= RELATED_COUNT:
            break
        if u != url and u not in used:
            chosen.append(u)
            used.add(u)

    for u in global_recent_pool:
        if len(chosen) >= RELATED_COUNT:
            break
        if u != url and u not in used:
            chosen.append(u)
            used.add(u)

    return chosen[:RELATED_COUNT]


def build_related_links(posts):
    posts = [p for p in posts if p.get('url')]

    by_category = defaultdict(list)
    for p in posts:
        by_category[p.get('cat', '')].append(p['url'])

    all_urls_by_date_desc = [
        p['url'] for p in sorted(posts, key=lambda p: p.get('date', ''), reverse=True)
    ]

    small_categories_urls = []
    cycle_next_map = {}
    big_categories = []  # (cat, urls) for categories large enough for their own cycle

    for cat, urls in by_category.items():
        if len(urls) >= MIN_CATEGORY_SIZE_FOR_OWN_CYCLE:
            big_categories.append((cat, urls))
        else:
            small_categories_urls.extend(urls)

    if small_categories_urls:
        if len(small_categories_urls) >= MIN_CATEGORY_SIZE_FOR_OWN_CYCLE:
            # Enough leftover small-category posts to form their own fallback cycle.
            cycle_next_map.update(build_cycle_links(small_categories_urls))
        elif big_categories:
            # Too few leftovers to form a cycle on their own (as few as a single
            # lonely post) — fold them into the LARGEST real category's cycle
            # instead, so they still get a guaranteed incoming link.
            big_categories.sort(key=lambda kv: len(kv[1]), reverse=True)
            largest_cat_urls = big_categories[0][1]
            cycle_next_map.update(build_cycle_links(largest_cat_urls + small_categories_urls))
            big_categories = big_categories[1:]  # already built above, don't rebuild below
        else:
            # No big categories exist at all (every post is in a tiny category) —
            # the only case a real cycle isn't fully possible; fall through and
            # let fill_to_three's global-recent fallback catch what it can.
            cycle_next_map.update(build_cycle_links(small_categories_urls))

    for cat, urls in big_categories:
        cycle_next_map.update(build_cycle_links(urls))

    result = {}
    for p in posts:
        url = p['url']
        cat = p.get('cat', '')
        same_cat_pool = [u for u in by_category[cat] if u != url]
        cycle_next = cycle_next_map.get(url, [])
        result[url] = fill_to_three(url, cycle_next, same_cat_pool, all_urls_by_date_desc)

    return result


def verify_no_orphans(posts, related_links):
    all_urls = {p['url'] for p in posts if p.get('url')}
    incoming = set()
    for targets in related_links.values():
        incoming.update(targets)
    return all_urls - incoming


def rebuild_related_links(posts):
    """Step 2 entry point — called automatically at the end of a normal run."""
    print("\n" + "─" * 60)
    print("Rebuilding related-links.json (guarantees zero orphan pages)")
    print("─" * 60)

    if not posts:
        print("No posts to build related-links for.")
        return

    related_links = build_related_links(posts)

    with open(RELATED_LINKS_JSON, 'w', encoding='utf-8') as f:
        json.dump(related_links, f, indent=2)

    print(f"Wrote {RELATED_LINKS_JSON.name} ({len(related_links)} posts)")

    orphans = verify_no_orphans(posts, related_links)
    if orphans:
        print(f"\n⚠️  WARNING: {len(orphans)} post(s) still have zero incoming links:")
        for o in sorted(orphans):
            print(f"   {o}")
        if len(posts) <= 1:
            print("(Expected — there's only one post total, nothing to link to/from yet.)")
        else:
            print("(Can only happen if a post has no valid url/category — check posts.json)")
    else:
        print("✅ Verified: every post has at least one incoming related-link. Zero orphans.")


# ════════════════════════════════════════════════════════════════════
# ONE-TIME MODE: retrofit existing post .html files
# (only ever needed once, for posts written before this system existed)
# ════════════════════════════════════════════════════════════════════

RELATED_SECTION_RE = re.compile(
    r'<section class="related-posts"[^>]*>.*?</section>',
    re.DOTALL
)

NEW_SECTION = (
    '<section class="related-posts" aria-label="Related tools and guides" id="related-tools">\n'
    '      <h2>Related tools and guides</h2>\n'
    '      <div class="related-grid" id="related-grid"></div>\n'
    '    </section>'
)

SCRIPT_TAG = '<script src="/blogs/related-posts.js"></script>'


def retrofit_file(path: Path, dry_run: bool) -> str:
    text = path.read_text(encoding='utf-8')
    original = text

    match = RELATED_SECTION_RE.search(text)
    if not match:
        return 'SKIPPED (no related-posts section found)'

    text = RELATED_SECTION_RE.sub(NEW_SECTION, text, count=1)

    if SCRIPT_TAG not in text:
        if '</body>' in text:
            text = text.replace('</body>', f'  {SCRIPT_TAG}\n</body>', 1)
        else:
            return 'SKIPPED (no </body> tag found, cannot insert script)'

    if text == original:
        return 'UNCHANGED (already up to date)'

    if not dry_run:
        path.with_suffix(path.suffix + '.bak').write_text(original, encoding='utf-8')
        path.write_text(text, encoding='utf-8')

    return 'UPDATED'


def run_retrofit(argv):
    target_dir = Path(argv[0]) if argv else BLOGS_DIR
    dry_run = '--dry-run' in argv

    if not target_dir.is_dir():
        print(f"Error: {target_dir} is not a directory")
        sys.exit(1)

    html_files = sorted(target_dir.glob('*.html'))
    if not html_files:
        print(f"No .html files found in {target_dir}")
        sys.exit(1)

    print(f"{'[DRY RUN] ' if dry_run else ''}Processing {len(html_files)} files in {target_dir}\n")

    counts = {}
    for f in html_files:
        result = retrofit_file(f, dry_run)
        counts[result] = counts.get(result, 0) + 1
        print(f"  {f.name}: {result}")

    print("\nSummary:")
    for status, count in counts.items():
        print(f"  {status}: {count}")


# ════════════════════════════════════════════════════════════════════
# Entry point
# ════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'retrofit':
        run_retrofit(sys.argv[2:])
        return

    # Normal run: scan for new posts, update posts.json, then always
    # rebuild related-links.json from the complete, current post list.
    all_posts = scan_and_update_posts_json()
    rebuild_related_links(all_posts)


if __name__ == "__main__":
    main()