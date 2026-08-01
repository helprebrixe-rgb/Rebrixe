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
  <script src="/blogs/related-posts.js"></script>

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


# ════════════════════════════════════════════════════════════════════
# STEP 2: rebuild related-links.json from the full posts list
# (runs automatically after Step 1, every time this script is run)
# ════════════════════════════════════════════════════════════════════

RELATED_COUNT = 6              # <-- was 3. Change this one number to retune site-wide.
MIN_POOL_SIZE = RELATED_COUNT + 1   # a pool needs > RELATED_COUNT posts to run its own circulant


def build_circulant_links(urls, k):
    """The core fix. Sort `urls` into a fixed order; post at position i
    links to the NEXT k posts in that order (wrapping around). This is
    a mathematical guarantee, not a heuristic:

        every post gets EXACTLY k outgoing links
        every post gets EXACTLY k incoming links

    ...as long as len(urls) > k (if the pool is smaller than that,
    k is capped to len(urls)-1 so every post still links to every
    OTHER post in the pool exactly once, which is the best possible
    outcome for a pool that small).

    Proof sketch for why in-degree == out-degree == k when n > k:
    post at position q is targeted by exactly the posts sitting at
    offsets q-1, q-2, ... q-k (mod n) - that's k distinct positions,
    none of which equal q itself, because k < n. So every post is
    targeted by exactly k other posts. No post can "absorb" more
    than its fair share, because every post's target list is offset
    by ITS OWN position - nobody is reading from a shared, static
    list the way the old fill_to_three() did.
    """
    n = len(urls)
    if n <= 1:
        return {u: [] for u in urls}
    k_eff = min(k, n - 1)
    links = {}
    for i, url in enumerate(urls):
        links[url] = [urls[(i + 1 + j) % n] for j in range(k_eff)]
    return links


def build_related_links(posts):
    """Builds the full related-links map with the guarantee above.

    Each category with MORE than RELATED_COUNT posts gets its own
    circulant, so related links stay topically relevant (an image
    post links to other image posts, etc).

    Categories too small to run their own circulant get folded
    together into one merged pool first; if that merged pool is
    STILL too small (this only happens if your whole site has fewer
    than RELATED_COUNT+1 posts, or - like this site right now - one
    category has just a lone post or two), it's folded into the
    largest category so it still gets its guaranteed 6-in/6-out.
    That one lone post's related links won't be perfectly on-topic
    until you publish more posts in its category - once a category
    reaches 7+ posts it automatically gets its own dedicated circulant
    on the next run, no code changes needed.
    """
    posts = [p for p in posts if p.get("url")]
    all_urls = [p["url"] for p in posts]

    by_category = defaultdict(list)
    for p in posts:
        by_category[p.get("cat", "")].append(p["url"])

    big_categories = []      # (cat, urls) - big enough for their own circulant
    leftover_urls = []       # from categories too small to stand alone

    for cat, urls in by_category.items():
        if len(urls) >= MIN_POOL_SIZE:
            big_categories.append((cat, urls))
        else:
            leftover_urls.extend(urls)

    pools = [urls for _cat, urls in big_categories]

    if leftover_urls:
        if len(leftover_urls) >= MIN_POOL_SIZE:
            # enough small-category posts combined to form their own pool
            pools.append(leftover_urls)
        elif pools:
            # too few to stand alone - fold into the single largest pool
            pools.sort(key=len, reverse=True)
            pools[0] = pools[0] + leftover_urls
        else:
            # entire site has fewer than MIN_POOL_SIZE posts total
            pools.append(leftover_urls)

    links_map = {}
    for pool in pools:
        links_map.update(build_circulant_links(pool, RELATED_COUNT))

    # Safety net: any post that somehow wasn't covered above (shouldn't
    # happen, but cheap to guarantee) gets linked to other posts directly.
    missing = [u for u in all_urls if u not in links_map]
    if missing:
        links_map.update(build_circulant_links(all_urls, RELATED_COUNT))

    return {u: links_map[u] for u in all_urls}


def verify_link_health(posts, related_links, k=RELATED_COUNT):
    """Checks the guarantee actually held: zero orphans, and (as close
    to k as pool size allows) incoming links per post. Prints a report."""
    all_urls = {p["url"] for p in posts if p.get("url")}
    incoming = Counter()
    for targets in related_links.values():
        for t in targets:
            incoming[t] += 1

    zero = [u for u in all_urls if incoming.get(u, 0) == 0]
    below_k = [u for u in all_urls if 0 < incoming.get(u, 0) < k]
    at_or_above_k = len(all_urls) - len(zero) - len(below_k)

    print(f"Incoming-link health check (target: {k} incoming links per post):")
    print(f"  {at_or_above_k} post(s) have >= {k} incoming links")
    if below_k:
        print(f"  {len(below_k)} post(s) have between 1 and {k - 1} incoming links "
              f"(only possible if their pool has <= {k} total posts):")
        for u in sorted(below_k):
            print(f"     {incoming.get(u, 0)}  {u}")
    if zero:
        print(f"  ⚠️  {len(zero)} post(s) have ZERO incoming links (orphans):")
        for u in sorted(zero):
            print(f"     {u}")
    if not below_k and not zero:
        print("  ✅ Every single post has at least the target number of incoming links.")
    return zero


def rebuild_related_links(posts):
    """Step 2 entry point — called automatically at the end of a normal run."""
    print("\n" + "─" * 60)
    print(f"Rebuilding related-links.json ({RELATED_COUNT} related links/post, "
          f"guarantees zero orphan pages)")
    print("─" * 60)

    if not posts:
        print("No posts to build related-links for.")
        return

    related_links = build_related_links(posts)

    with open(RELATED_LINKS_JSON, "w", encoding="utf-8") as f:
        json.dump(related_links, f, indent=2)

    print(f"Wrote {RELATED_LINKS_JSON.name} ({len(related_links)} posts)\n")

    verify_link_health(posts, related_links)


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