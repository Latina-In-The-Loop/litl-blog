#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# new-post.sh — Create a new LITL blog post with pre-filled front matter
# Usage: ./scripts/new-post.sh
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

POSTS_DIR="$(dirname "$0")/../_posts"
DATE=$(date +%Y-%m-%d)

# ── Prompt for title ──────────────────────────────────────────────────────────
echo ""
echo "✦ New Post — Latina in the Loop"
echo "────────────────────────────────"
echo ""
read -rp "Post title: " TITLE

if [[ -z "$TITLE" ]]; then
  echo "Error: title cannot be empty." >&2
  exit 1
fi

# ── Prompt for subtitle ───────────────────────────────────────────────────────
read -rp "Subtitle (optional): " SUBTITLE

# ── Prompt for tags ───────────────────────────────────────────────────────────
read -rp "Tags (comma-separated, e.g. agentic-ai, building): " TAGS_RAW

# ── Build slug from title ─────────────────────────────────────────────────────
SLUG=$(echo "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed 's/[^a-z0-9 -]//g' \
  | tr ' ' '-' \
  | sed 's/--*/-/g' \
  | sed 's/^-//;s/-$//')

FILENAME="${POSTS_DIR}/${DATE}-${SLUG}.md"

# ── Check if file already exists ─────────────────────────────────────────────
if [[ -f "$FILENAME" ]]; then
  echo ""
  echo "Error: file already exists: $FILENAME" >&2
  exit 1
fi

# ── Build YAML tags list ──────────────────────────────────────────────────────
TAGS_YAML=""
if [[ -n "$TAGS_RAW" ]]; then
  IFS=',' read -ra TAG_ARRAY <<< "$TAGS_RAW"
  for tag in "${TAG_ARRAY[@]}"; do
    trimmed=$(echo "$tag" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    TAGS_YAML="${TAGS_YAML}  - ${trimmed}"$'\n'
  done
fi

# ── Write the file ────────────────────────────────────────────────────────────
cat > "$FILENAME" <<EOF
---
layout: post
title: "${TITLE}"
subtitle: "${SUBTITLE}"
date: ${DATE}
tags:
${TAGS_YAML}author: Latina in the Loop
description: ""
---

<!-- Write your post here -->
EOF

echo ""
echo "Created: $FILENAME"
echo ""

# ── Open in default editor ────────────────────────────────────────────────────
EDITOR="${EDITOR:-}"

if [[ -z "$EDITOR" ]]; then
  # Try to detect a sensible default
  if command -v code &>/dev/null; then
    EDITOR="code"
  elif command -v nano &>/dev/null; then
    EDITOR="nano"
  elif command -v vim &>/dev/null; then
    EDITOR="vim"
  fi
fi

if [[ -n "$EDITOR" ]]; then
  echo "Opening in ${EDITOR}..."
  $EDITOR "$FILENAME"
else
  echo "No editor found. Open manually: $FILENAME"
fi
