#!/usr/bin/env python3
"""
Sitemap generator for rebrixe.com
----------------------------------
Scans the repo for .html files (root pages + /blogs/ posts), builds clean
URLs (no double counting of index.html), pulls last-modified dates from git
history when available, and writes a sitemap.xml at the project root.

Usage:
    python3 generate_sitemap.py

Run this from the root of your repo before pushing/whenever you add new
blog posts. It will overwrite sitemap.xml with the latest full list.
"""

import os
import subprocess
import datetime
from xml.sax.saxutils import escape

# ---- CONFIG: edit these if your setup changes ----
DOMAIN = "https://rebrixe.com"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(ROOT_DIR, "sitemap.xml")

# Folders to completely skip while scanning
EXCLUDE_DIRS = {".git", "node_modules", ".github", "venv", "__pycache__"}

# Specific files to skip (sitemap doesn't need to list these even though
# they're .html, e.g. error pages)
EXCLUDE_FILES = {"404.html", "500.html"}
# ----------------------------------------------------


def get_git_lastmod(filepath):
    """Return the last commit date for a file in YYYY-MM-DD format,
    or today's date if git history isn't available (e.g. uncommitted file)."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=short", "--", filepath],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            timeout=5,
        )
        date_str = result.stdout.strip()
        if date_str:
            return date_str
    except Exception:
        pass
    return datetime.date.today().isoformat()


def path_to_url(filepath):
    """
    Convert a filesystem path to a clean site URL.
    - root index.html -> https://rebrixe.com/
    - blogs/index.html -> https://rebrixe.com/blogs/
    - blogs/first-post.html -> https://rebrixe.com/blogs/first-post.html
    - about.html -> https://rebrixe.com/about.html
    """
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    rel_path = rel_path.replace(os.sep, "/")  # windows safety

    if rel_path == "index.html":
        url_path = ""
    elif rel_path.endswith("/index.html"):
        url_path = rel_path[: -len("index.html")]
    else:
        url_path = rel_path

    return f"{DOMAIN}/{url_path}".replace("//", "/").replace(":/", "://")


def collect_html_files():
    seen_urls = {}  # url -> filepath, used to dedupe
    for current_root, dirs, files in os.walk(ROOT_DIR):
        # prune excluded directories in-place so os.walk skips them
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for filename in files:
            if not filename.endswith(".html"):
                continue
            if filename in EXCLUDE_FILES:
                continue

            full_path = os.path.join(current_root, filename)
            url = path_to_url(full_path)

            if url in seen_urls:
                # Duplicate URL resolved (e.g. shouldn't normally happen,
                # but guards against weird edge cases)
                print(f"  [skip] Duplicate URL for {full_path} -> {url} "
                      f"(already mapped from {seen_urls[url]})")
                continue

            seen_urls[url] = full_path

    return seen_urls


def build_sitemap(url_map):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Sort: homepage first, then alphabetically by URL for readability
    def sort_key(url):
        return (url != f"{DOMAIN}/", url)

    for url in sorted(url_map.keys(), key=sort_key):
        filepath = url_map[url]
        lastmod = get_git_lastmod(filepath)
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(url)}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    print(f"Scanning {ROOT_DIR} for .html files...")
    url_map = collect_html_files()
    print(f"Found {len(url_map)} unique URLs.")

    sitemap_xml = build_sitemap(url_map)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    print(f"Wrote {OUTPUT_FILE}")
    print("\nPreview of URLs included:")
    for url in sorted(url_map.keys()):
        print(f"  {url}")


if __name__ == "__main__":
    main()