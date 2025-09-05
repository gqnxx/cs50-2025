#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$repo_root"

echo "Submitting Week 2 problems..."
tools/cs50dev/submit50-auto.sh scrabble
tools/cs50dev/submit50-auto.sh readability
tools/cs50dev/submit50-auto.sh caesar
echo "Week 2 submissions complete."
