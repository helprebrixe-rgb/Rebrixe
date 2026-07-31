/**
 * related-posts.js
 * ─────────────────────────────────────────────
 * Renders the "Related tools and guides" block on every blog post page.
 *
 * This script does NOT decide which posts are related — that's computed
 * ahead of time by build_related_links.py, which guarantees every post
 * gets at least one incoming link (no orphans possible), and writes the
 * result to /blogs/related-links.json. This script's only job is to
 * look up the current post's entry and render it.
 *
 * WHY IT'S SPLIT THIS WAY
 * Guaranteeing "every post has an incoming link" requires looking at ALL
 * posts at once (to build link cycles) — that can't be done correctly
 * by each page independently deciding its own links in the browser.
 * So the guarantee-work happens once, in Python, ahead of time; this
 * script just displays the precomputed result. Re-run
 * build_related_links.py any time posts.json changes (new posts added)
 * to keep related-links.json in sync.
 *
 * HOW TO ADD THIS TO A POST FILE
 * Replace the hardcoded related-posts section with an empty shell:
 *
 *   <section class="related-posts" aria-label="Related tools and guides" id="related-tools">
 *     <h2>Related tools and guides</h2>
 *     <div class="related-grid" id="related-grid"></div>
 *   </section>
 *
 * Then add this line near your other scripts, before </body>:
 *   <script src="/blogs/related-posts.js"></script>
 *
 * Nothing else needs to change per post, ever again — as long as
 * build_related_links.py gets re-run after posts.json changes.
 */

(() => {
  const CATS = {
    'generators':     { label: 'AI / Names' },
    'growth':         { label: 'Growth' },
    'technical':      { label: 'Dev & Technical' },
    'image-visual': { label: 'Visual' },
    'time-date':    { label: 'Time & Productivity' },
  };

  async function init() {
    const grid = document.getElementById('related-grid');
    if (!grid) return; // page doesn't have the related-posts section

    // Normalize the current path so matching works whether the page is
    // accessed via the clean URL or the raw .html file (e.g. during local
    // testing, or before a redirect resolves) — same normalization is
    // applied to posts.json/related-links.json URLs below.
    const normalize = (p) => p.replace(/\/$/, '').replace(/\.html$/, '');
    const currentPath = normalize(window.location.pathname);

    let relatedLinks, posts;
    try {
      const [linksRes, postsRes] = await Promise.all([
        fetch('/blogs/related-links.json', { cache: 'default' }),
        fetch('/blogs/posts.json', { cache: 'default' }),
      ]);
      if (!linksRes.ok) throw new Error('Failed to load related-links.json');
      if (!postsRes.ok) throw new Error('Failed to load posts.json');
      relatedLinks = await linksRes.json();
      posts = await postsRes.json();
    } catch (err) {
      console.error('related-posts.js:', err);
      grid.closest('.related-posts')?.remove(); // fail quietly, don't show a broken section
      return;
    }

    // Match ignoring trailing slash and .html differences
    const matchKey = Object.keys(relatedLinks).find(
      k => normalize(k) === currentPath
    );
    const relatedUrls = matchKey ? relatedLinks[matchKey] : [];

    if (!relatedUrls || relatedUrls.length === 0) {
      grid.closest('.related-posts')?.remove();
      return;
    }

    const postsByUrl = new Map(posts.map(p => [normalize(p.url), p]));
    const relatedPosts = relatedUrls
      .map(url => postsByUrl.get(normalize(url)))
      .filter(Boolean);

    if (relatedPosts.length === 0) {
      grid.closest('.related-posts')?.remove();
      return;
    }

    grid.innerHTML = relatedPosts.map(cardHTML).join('');
  }

  function cardHTML(post) {
    const catLabel = (CATS[post.cat] && CATS[post.cat].label) || post.cat || '';
    return `
      <a class="related-card" href="${post.url}">
        <span class="related-label">${escapeHTML(catLabel)}</span>
        <h3>${escapeHTML(post.title)}</h3>
        <p>${escapeHTML(post.desc)}</p>
      </a>
    `;
  }

  function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();