#!/usr/bin/env bash
set -euo pipefail

echo "Checking for tracked env files..."
git ls-files | grep -E '(^|/)\.env($|\.|/)|(^|/)docker\.env$|(^|/)\.env\.compose$' && {
  echo "Tracked secret-like env file found. Fix this."; exit 1
} || true

echo "Checking for hardcoded secret markers..."
grep -RIn --exclude-dir=.git --exclude-dir=.venv \
  -E 'GROQ_API_KEY\s*=\s*"|API_KEY\s*=\s*"' src/ || true

echo "Secret-safety check completed."
