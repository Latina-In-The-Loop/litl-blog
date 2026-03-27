#!/usr/bin/env python3
"""
Social graphics generator for Latina in the Loop.

Usage:
  python scripts/generate-social.py 2026-03-27-passive-learning-trap
  python scripts/generate-social.py 2026-03-27-passive-learning-trap \\
      --quote "You're not behind. You're overprepared for the wrong thing." \\
      --emoji "✈️"
"""

import argparse
import html
import re
import sys
import time
from pathlib import Path

import frontmatter

# ── Paths ──────────────────────────────────────────────────────────────────────
BLOG_ROOT  = Path(__file__).resolve().parent.parent
POSTS_DIR  = BLOG_ROOT / "_posts"
SOCIAL_DIR = BLOG_ROOT / "assets" / "social"

# ── Brand tokens ───────────────────────────────────────────────────────────────
TERRA       = "#C1622A"
TERRA_LIGHT = "#D4845E"
TERRA_DARK  = "#8B3E1F"
TERRA_PALE  = "#F5ECE5"
NEAR_BLACK  = "#0D0D0D"
CREAM       = "#FAF6F0"
WARM_WHITE  = "#FFFDF9"
INK         = "#1A1008"
INK_MID     = "#5C3D2A"
INK_LIGHT   = "#9A7560"
RULE        = "#E8D5C4"

URL_LABEL   = "latina-in-the-loop.substack.com"

LOGO_WHITE = """<svg class="logo" viewBox="0 0 130 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 6 L22 18 L8 30" stroke="#C1622A" stroke-width="5.5"
    stroke-linecap="square" stroke-linejoin="miter" fill="none"/>
  <text x="32" y="26" font-family="'DM Sans', sans-serif" font-weight="700"
    font-size="22" fill="#FFFFFF" letter-spacing="2">LITL</text>
  <rect x="116" y="6" width="4" height="24" fill="#C1622A"/>
</svg>"""

LOGO_DARK = """<svg class="logo" viewBox="0 0 130 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 6 L22 18 L8 30" stroke="#C1622A" stroke-width="5.5"
    stroke-linecap="square" stroke-linejoin="miter" fill="none"/>
  <text x="32" y="26" font-family="'DM Sans', sans-serif" font-weight="700"
    font-size="22" fill="#1A1008" letter-spacing="2">LITL</text>
  <rect x="116" y="6" width="4" height="24" fill="#C1622A"/>
</svg>"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_issue_number(slug: str) -> int:
    """Return 1-based issue number from chronological post order."""
    posts = sorted(p.stem for p in POSTS_DIR.glob("*.md"))
    try:
        return posts.index(slug) + 1
    except ValueError:
        return len(posts)


def strip_md(text: str) -> str:
    """Remove common markdown formatting from a string."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    return text.strip()


def extract_content(post: frontmatter.Post):
    """
    Returns (excerpt, list_items, closing_question) from post body.

    excerpt          — first real paragraph, plain text
    list_items       — list[dict(term, desc)], up to 4
    closing_question — last sentence ending with ?
    """
    body = post.content
    lines = body.splitlines()

    # ── Paragraphs ──
    paragraphs = []
    current = []
    skip = False
    for line in lines:
        s = line.strip()
        # Skip HTML blocks
        if re.match(r'^<[a-z]', s, re.I):
            skip = True
        if skip:
            if re.match(r'^</', s) or s == '':
                skip = False
            continue
        # Skip headings, blockquotes, front-matter fences
        if s.startswith('#') or s.startswith('>') or s == '---':
            continue
        if not s:
            if current:
                para = ' '.join(current)
                para = strip_md(para)
                if len(para) > 20:
                    paragraphs.append(para)
            current = []
        else:
            current.append(s)
    if current:
        para = strip_md(' '.join(current))
        if len(para) > 20:
            paragraphs.append(para)

    excerpt = paragraphs[0] if paragraphs else ""

    # ── List items (bullets or numbered with bold term) ──
    list_items = []
    for line in lines:
        s = line.strip()
        m = re.match(r'^(?:[-*]|\d+\.)\s+\*\*(.+?)\*\*\s*(.*)', s)
        if m:
            term = m.group(1).strip().rstrip('.,;:')
            desc = strip_md(m.group(2)).lstrip('—–- ').strip()
            list_items.append({'term': term, 'desc': desc})

    # ── Closing question ──
    closing_question = ""
    for line in reversed(lines):
        s = strip_md(line).strip('*').strip()
        if s.endswith('?') and len(s) > 25 and not s.startswith('#'):
            closing_question = s
            break

    return excerpt, list_items[:4], closing_question


def tags_to_eyebrow(tags: list) -> str:
    """Convert tag list to a short uppercase eyebrow string."""
    priority = ['agentic-ai', 'building', 'governance', 'systems-thinking',
                'product-management', 'learning', 'automation']
    selected = [t for t in tags if t in priority][:2]
    if not selected:
        selected = [t for t in tags if t][:2]
    return ' · '.join(t.replace('-', ' ').upper() for t in selected) or 'BUILDING WITH AI'


def highlight_subtitle(subtitle: str) -> str:
    """
    Wrap the trailing clause of a subtitle in a .highlight span
    so Card 01 can colour it in terra-light.
    """
    # Split on 'and why' / ', and' / last comma clause
    m = re.search(r'(,\s+and\s+)(.*)', subtitle, re.IGNORECASE)
    if m:
        return html.escape(subtitle[:m.start()]) + \
               '<span class="hl">, and ' + html.escape(m.group(2)) + '</span>'
    # Fallback: colour last ~30% of words
    words = subtitle.split()
    split = max(int(len(words) * 0.65), len(words) - 6)
    return html.escape(' '.join(words[:split])) + \
           ' <span class="hl">' + html.escape(' '.join(words[split:])) + '</span>'


def build_list_items_html(items: list) -> str:
    rows = []
    for i, item in enumerate(items, 1):
        term = html.escape(item['term'])
        desc = html.escape(item['desc'])
        rows.append(f"""\
        <div class="li-row">
          <span class="li-num">{i:02d}</span>
          <div class="li-body">
            <span class="li-term">{term}</span>
            <span class="li-desc">{desc}</span>
          </div>
        </div>""")
    return '\n'.join(rows)


# ── HTML generation ────────────────────────────────────────────────────────────

def generate_html(data: dict) -> str:
    title           = html.escape(data['title'])
    subtitle_html   = highlight_subtitle(data['subtitle'])
    issue_label     = html.escape(data['issue_label'])
    excerpt         = html.escape(data['excerpt'])
    closing_q       = html.escape(data['closing_question'])
    quote           = html.escape(data['quote'])
    emoji           = data['emoji']
    eyebrow         = html.escape(data['eyebrow'])
    url             = html.escape(URL_LABEL)

    default_items = [
        {'term': 'Orchestration',    'desc': 'how multiple models and data sources are coordinated'},
        {'term': 'Guardrails',       'desc': 'the operational constraints that keep the system reliable'},
        {'term': 'Decision points',  'desc': 'the logic that navigates non-linear, messy real-world workflows'},
        {'term': 'Human-in-the-loop','desc': 'knowing exactly where to place human oversight, and why'},
    ]
    items = data['list_items'] if len(data['list_items']) >= 3 else default_items
    list_html = build_list_items_html(items[:4])

    # Card 05: split excerpt into headline + body
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', data['excerpt']) if s.strip()]
    headline = html.escape(sentences[0]) if sentences else excerpt
    body_txt = html.escape(' '.join(sentences[1:3])) if len(sentences) > 1 else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Social — {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: #1A1A1A;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  gap: 60px;
  align-items: flex-start;
  font-family: 'DM Sans', sans-serif;
}}

.logo {{ height: 28px; width: auto; display: block; }}
.card {{ flex-shrink: 0; position: relative; overflow: hidden; }}

/* ── CARD 01 ── */
#c01 {{
  width: 1080px; height: 1080px;
  background: {NEAR_BLACK};
  display: flex; flex-direction: column;
  justify-content: space-between;
  padding: 64px;
}}
#c01::before {{
  content: '';
  position: absolute;
  top: -100px; right: -100px;
  width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(193,98,42,0.22) 0%, transparent 62%);
  pointer-events: none;
}}
#c01 .quote-wrap {{
  flex: 1;
  display: flex;
  align-items: center;
}}
#c01 .quote-text {{
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 27px;
  color: #FFFFFF;
  line-height: 1.6;
  max-width: 860px;
}}
#c01 .hl {{ color: {TERRA_LIGHT}; }}
#c01 .foot {{
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: rgba(255,255,255,0.3);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

/* ── CARD 02 ── */
#c02 {{
  width: 1080px; height: 1080px;
  background: {CREAM};
  border: 1.5px solid {RULE};
  display: flex; flex-direction: column;
  justify-content: space-between;
  padding: 64px;
}}
#c02 .eyebrow {{
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: {TERRA};
  margin-top: 28px;
  margin-bottom: 14px;
}}
#c02 .card-title {{
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  font-size: 24px;
  color: {INK};
  line-height: 1.3;
  max-width: 700px;
}}
#c02 .shifts {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 36px;
  padding: 40px 0;
}}
#c02 .sr {{
  display: flex;
  align-items: center;
  gap: 22px;
  font-family: 'DM Mono', monospace;
  font-size: 16px;
}}
#c02 .sr-from {{
  color: rgba(26,16,8,0.28);
  text-decoration: line-through;
  text-decoration-color: rgba(26,16,8,0.18);
  min-width: 200px;
}}
#c02 .sr-arrow {{ color: {TERRA}; font-size: 22px; }}
#c02 .sr-to {{ color: {INK}; font-weight: 500; }}
#c02 .foot {{
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  color: {INK_LIGHT};
  letter-spacing: 0.1em;
  text-transform: uppercase;
}}

/* ── CARD 03 ── */
#c03 {{
  width: 1080px; height: 1080px;
  background: {TERRA};
  display: flex; flex-direction: column;
  justify-content: space-between;
  padding: 64px;
}}
#c03 .quote-wrap {{
  flex: 1;
  display: flex;
  align-items: center;
}}
#c03 .quote-text {{
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 34px;
  color: #FFFFFF;
  line-height: 1.45;
  max-width: 880px;
}}
#c03 .foot {{
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  color: rgba(255,255,255,0.5);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

/* ── CARD 04 ── */
#c04 {{
  width: 1080px; height: 1350px;
  background: {NEAR_BLACK};
  display: flex; flex-direction: column;
  justify-content: space-between;
  padding: 64px;
}}
#c04 .eyebrow {{
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: {TERRA};
  margin-top: 28px;
  margin-bottom: 14px;
}}
#c04 .card-title {{
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  font-size: 22px;
  color: #FFFFFF;
  line-height: 1.35;
  max-width: 780px;
}}
#c04 .list-items {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 34px;
  padding: 40px 0;
}}
#c04 .li-row {{
  display: flex;
  gap: 24px;
  align-items: flex-start;
}}
#c04 .li-num {{
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: {TERRA};
  flex-shrink: 0;
  min-width: 26px;
  padding-top: 2px;
}}
#c04 .li-body {{
  display: flex;
  flex-direction: column;
  gap: 5px;
}}
#c04 .li-term {{
  font-weight: 500;
  font-size: 16px;
  color: #FFFFFF;
}}
#c04 .li-desc {{
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  line-height: 1.55;
  font-weight: 300;
}}
#c04 .foot {{
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  color: rgba(255,255,255,0.25);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}}

/* ── CARD 05 ── */
#c05 {{
  width: 1080px; height: 1080px;
  background: {CREAM};
  border: 1.5px solid {RULE};
  display: flex; flex-direction: column;
  justify-content: space-between;
  padding: 64px;
}}
#c05 .top-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}}
#c05 .story-emoji {{
  font-size: 72px;
  line-height: 1;
}}
#c05 .story-body {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
  padding: 36px 0;
}}
#c05 .headline {{
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  font-size: 26px;
  color: {INK};
  line-height: 1.35;
  max-width: 860px;
}}
#c05 .body-text {{
  font-size: 16px;
  color: {INK_MID};
  line-height: 1.65;
  max-width: 820px;
  font-weight: 300;
}}
#c05 .foot {{
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  color: {INK_LIGHT};
  letter-spacing: 0.1em;
  text-transform: uppercase;
}}

/* ── CARD 06 ── */
#c06 {{
  width: 1080px; height: 1080px;
  background: {NEAR_BLACK};
  display: flex; flex-direction: column;
  justify-content: space-between;
  padding: 64px 64px 60px;
}}
#c06::after {{
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 4px;
  background: {TERRA};
}}
#c06 .quote-wrap {{
  flex: 1;
  display: flex;
  align-items: center;
}}
#c06 .quote-text {{
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 26px;
  color: rgba(255,255,255,0.9);
  line-height: 1.6;
  max-width: 880px;
}}
#c06 .cta-block {{
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding-bottom: 8px;
}}
#c06 .cta-label {{
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  color: rgba(255,255,255,0.28);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}}
#c06 .cta-url {{
  font-family: 'DM Mono', monospace;
  font-size: 14px;
  color: {TERRA_LIGHT};
  font-weight: 500;
}}
</style>
</head>
<body>

<!-- ── CARD 01 — Core Quote ── -->
<div class="card" id="c01">
  {LOGO_WHITE}
  <div class="quote-wrap">
    <div class="quote-text">&#8220;{subtitle_html}&#8221;</div>
  </div>
  <div class="foot">{url} &middot; {issue_label}</div>
</div>

<!-- ── CARD 02 — Three Shifts ── -->
<div class="card" id="c02">
  <div>
    {LOGO_DARK}
    <div class="eyebrow">The Paradigm Shift</div>
    <div class="card-title">Three things had to change before I could build.</div>
  </div>
  <div class="shifts">
    <div class="sr"><span class="sr-from">Deterministic</span><span class="sr-arrow">&#8594;</span><span class="sr-to">Probabilistic</span></div>
    <div class="sr"><span class="sr-from">Execution</span><span class="sr-arrow">&#8594;</span><span class="sr-to">Governance</span></div>
    <div class="sr"><span class="sr-from">Tools</span><span class="sr-arrow">&#8594;</span><span class="sr-to">Orchestration</span></div>
  </div>
  <div class="foot">{url} &middot; {issue_label}</div>
</div>

<!-- ── CARD 03 — Reframe Quote ── -->
<div class="card" id="c03">
  {LOGO_WHITE}
  <div class="quote-wrap">
    <div class="quote-text">&#8220;{quote}&#8221;</div>
  </div>
  <div class="foot">Latina in the Loop &middot; {issue_label}</div>
</div>

<!-- ── CARD 04 — Numbered List ── -->
<div class="card" id="c04">
  <div>
    {LOGO_WHITE}
    <div class="eyebrow">{eyebrow}</div>
    <div class="card-title">What building actually looks like — in practice, not theory.</div>
  </div>
  <div class="list-items">
{list_html}
  </div>
  <div class="foot">{url}</div>
</div>

<!-- ── CARD 05 — Personal Story ── -->
<div class="card" id="c05">
  <div class="top-row">
    {LOGO_DARK}
    <span class="story-emoji">{emoji}</span>
  </div>
  <div class="story-body">
    <div class="headline">{headline}</div>
    <div class="body-text">{body_txt}</div>
  </div>
  <div class="foot">{url} &middot; {issue_label}</div>
</div>

<!-- ── CARD 06 — Closing CTA ── -->
<div class="card" id="c06">
  {LOGO_WHITE}
  <div class="quote-wrap">
    <div class="quote-text">{closing_q}</div>
  </div>
  <div class="cta-block">
    <span class="cta-label">Read {issue_label} &#8594;</span>
    <span class="cta-url">{url}</span>
  </div>
</div>

</body>
</html>"""


# ── Screenshot ─────────────────────────────────────────────────────────────────

CARDS = [
    ("c01", 1080, 1080,  "01_core_quote"),
    ("c02", 1080, 1080,  "02_three_shifts"),
    ("c03", 1080, 1080,  "03_reframe_quote"),
    ("c04", 1080, 1350,  "04_numbered_list"),
    ("c05", 1080, 1080,  "05_personal_story"),
    ("c06", 1080, 1080,  "06_closing_cta"),
]


def screenshot_cards(html_path: Path, output_dir: Path):
    from playwright.sync_api import sync_playwright

    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for card_id, w, h, name in CARDS:
            page = browser.new_page(
                viewport={"width": w, "height": h},
                device_scale_factor=2,
            )
            page.goto(f"file:///{html_path.resolve().as_posix()}")
            # Wait for Google Fonts to load
            page.wait_for_timeout(2000)

            out = output_dir / f"{name}.png"
            page.locator(f"#{card_id}").screenshot(path=str(out))
            print(f"  \u2713 {name}.png ({w}x{h})")

        browser.close()


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate social graphics for a Latina in the Loop post."
    )
    parser.add_argument("slug", help="Post slug, e.g. 2026-03-27-passive-learning-trap")
    parser.add_argument("--quote",  default=None, help="Override Card 03 reframe quote")
    parser.add_argument("--emoji",  default="✈️",   help="Override Card 05 emoji")
    args = parser.parse_args()

    slug = args.slug.removesuffix(".md")
    post_path = POSTS_DIR / f"{slug}.md"

    if not post_path.exists():
        sys.exit(f"Error: post not found at {post_path}")

    post  = frontmatter.load(str(post_path))
    title = post.get("title", slug)

    print(f"Generating social graphics for: {title}")
    print(f"Reading post: _posts/{slug}.md")

    issue_num   = get_issue_number(slug)
    issue_label = f"Issue {issue_num:02d}"
    tags        = post.get("tags", [])

    excerpt, list_items, closing_question = extract_content(post)

    if not closing_question:
        closing_question = (
            "What expertise from your past is waiting to be applied "
            "to the systems of the future?"
        )

    print("Extracted: title, subtitle, excerpt, closing question")
    print(f"Issue: {issue_label}  ·  Tags: {', '.join(str(t) for t in tags[:3])}")

    data = {
        "title":            title,
        "subtitle":         post.get("subtitle", title),
        "issue_label":      issue_label,
        "excerpt":          excerpt,
        "list_items":       list_items,
        "closing_question": closing_question,
        "quote":            args.quote or "You\u2019re not behind. You\u2019re overprepared for the wrong thing.",
        "emoji":            args.emoji,
        "eyebrow":          tags_to_eyebrow(tags),
    }

    print("Generating HTML...")
    page_html = generate_html(data)

    # Write staging HTML
    SOCIAL_DIR.mkdir(parents=True, exist_ok=True)
    html_path = SOCIAL_DIR / f"{slug}.html"
    html_path.write_text(page_html, encoding="utf-8")

    output_dir = SOCIAL_DIR / slug
    print("Screenshotting 6 cards...")
    t0 = time.time()

    screenshot_cards(html_path, output_dir)

    print(f"Saved to: assets/social/{slug}/")
    print(f"Done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
