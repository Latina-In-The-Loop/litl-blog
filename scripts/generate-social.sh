#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# generate-social.sh — Generate social graphics for a blog post
#
# PLACEHOLDER — not yet implemented.
#
# PLANNED BEHAVIOR:
#   1. Takes a post slug as input (e.g. "2026-03-27-passive-learning-trap")
#   2. Reads the post's front matter (title, subtitle, date, tags)
#   3. Renders 6 social card templates using a headless browser or image tool:
#         - Open Graph (1200×630) — primary share card
#         - Twitter/X card (1200×628)
#         - Instagram square (1080×1080)
#         - Instagram story (1080×1920)
#         - LinkedIn banner (1200×627)
#         - Substack preview card (600×400)
#   4. Exports each as PNG to: /assets/social/[post-slug]/
#         e.g. assets/social/passive-learning-trap/og.png
#              assets/social/passive-learning-trap/twitter.png
#              etc.
#
# IMPLEMENTATION NOTES (future):
#   - Option A: Use Puppeteer/Playwright to render an HTML template to PNG
#       npm i -D puppeteer
#       node scripts/render-card.js --slug $SLUG --template og
#   - Option B: Use ImageMagick with pre-designed card layouts
#       convert -size 1200x630 template.png -font Playfair-Display ...
#   - Option C: Use a cloud API (Bannerbear, Placid, or similar)
#       curl -X POST https://api.bannerbear.com/v2/images \
#            -H "Authorization: Bearer $BANNERBEAR_API_KEY" ...
#
# Brand colors:
#   Primary:    #C1622A (terracotta)
#   Background: #FAF6F0 (warm cream)
#   Dark:       #0D0D0D (near black)
#   Accent:     #9A7560
#
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

echo "generate-social.sh: not yet implemented."
echo ""
echo "Usage: ./scripts/generate-social.sh <post-slug>"
echo "Example: ./scripts/generate-social.sh passive-learning-trap"
echo ""
echo "See script comments for implementation options."
exit 0
