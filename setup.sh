#!/usr/bin/env bash
set -e

DEST="$HOME/Development/pdftools/pdf-annotation-extractor"

echo "→ Copying project to $DEST"
mkdir -p "$DEST"
cp -r . "$DEST"
cd "$DEST"

echo "→ Initializing git"
git init
git add .
git commit -m "Initial commit: PDF annotation extractor with click + rich"

echo "→ Creating uv environment and syncing dependencies"
uv sync

echo ""
echo "✓ Done! To use the tool:"
echo "  cd $DEST"
echo "  uv run extract-pdf-annotations --help"
