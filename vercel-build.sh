#!/usr/bin/env bash
# Vercel build entry — handles three things Vercel's stock Hugo preset misses:
#   1. Dart Sass binary (Hugo Blox SCSS needs @use/@forward — libsass can't compile it)
#   2. Go toolchain (Hugo Modules pull the theme via `go mod download`)
#   3. Per-deployment baseURL (otherwise previews load assets from the prod domain)
#
# Tools land under ./.tools/, which Vercel keeps across builds when its build
# cache hits, so subsequent deploys reuse them.

set -euo pipefail

DART_SASS_VERSION="1.83.0"
GO_VERSION="1.21.13"
TOOLS_DIR="${PWD}/.tools"

mkdir -p "${TOOLS_DIR}"

if ! command -v sass >/dev/null 2>&1; then
  if [ ! -x "${TOOLS_DIR}/dart-sass/sass" ]; then
    echo "→ Installing Dart Sass ${DART_SASS_VERSION}"
    curl -fsSL "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" \
      | tar -xz -C "${TOOLS_DIR}"
  fi
  export PATH="${TOOLS_DIR}/dart-sass:${PATH}"
fi

if ! command -v go >/dev/null 2>&1; then
  if [ ! -x "${TOOLS_DIR}/go/bin/go" ]; then
    echo "→ Installing Go ${GO_VERSION}"
    curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" \
      | tar -xz -C "${TOOLS_DIR}"
  fi
  export PATH="${TOOLS_DIR}/go/bin:${PATH}"
fi

echo "→ sass:  $(command -v sass)  $(sass --version 2>/dev/null | head -1)"
echo "→ go:    $(command -v go)    $(go version 2>/dev/null)"
echo "→ hugo:  $(command -v hugo)  $(hugo version 2>/dev/null)"

if [ "${VERCEL_ENV:-}" = "production" ]; then
  echo "→ Production build (baseURL from config.yaml)"
  hugo --gc --minify --logLevel error
else
  PREVIEW_URL="${VERCEL_BRANCH_URL:-${VERCEL_URL:-localhost}}"
  echo "→ Preview build for https://${PREVIEW_URL}/"
  hugo --gc --minify --buildFuture --buildDrafts --logLevel error \
    --baseURL "https://${PREVIEW_URL}/"
fi
