#!/usr/bin/env bash
# Publishes site/ to the public preview repo (GitHub Pages):
#   https://levelledmedia.github.io/yenstone-preview/
# The source repo is private (and its plan cannot serve Pages), so only the built site goes out.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
cp -R "$ROOT/site/." "$TMP/"
touch "$TMP/.nojekyll"
cd "$TMP"
git init -q -b main
git add -A
git commit -q -m "Preview build $(date '+%Y-%m-%d %H:%M')"
git remote add origin https://github.com/levelledmedia/yenstone-preview.git
git push -q -f origin main
rm -rf "$TMP"
echo "Published: https://levelledmedia.github.io/yenstone-preview/"
