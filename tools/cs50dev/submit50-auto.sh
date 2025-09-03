#!/usr/bin/env bash
set -uo pipefail

problem="${1:-}"
if [[ -z "$problem" ]]; then
  echo "Usage: tools/cs50dev/submit50-auto.sh <problem>" >&2
  echo "Problems: hello | mario/less | mario/more | cash | credit" >&2
  exit 2
fi

# Map problem -> relative dir and candidate slugs (in order)
dir=""; declare -a slugs=()
case "$problem" in
  hello)
    dir="pset1-c/hello"
    slugs=("cs50/problems/2025/x/hello" "cs50/problems/2024/x/hello")
    ;;
  mario/less)
    dir="pset1-c/mario-less"
    slugs=("cs50/problems/2025/x/mario/less")
    ;;
  mario/more)
    dir="pset1-c/mario-more"
    slugs=("cs50/problems/2025/x/mario/more")
    ;;
  cash)
    dir="pset1-c/cash"
    slugs=("cs50/problems/2025/x/cash")
    ;;
  credit)
    dir="pset1-c/credit"
    slugs=("cs50/problems/2025/x/credit")
    ;;
  *)
    echo "Unknown problem: $problem" >&2
    exit 2
    ;;
esac

if [[ ! -d "$dir" ]]; then
  echo "Directory not found: $dir (run from repo root)" >&2
  exit 2
fi

cd "$dir"

echo "Submitting $problem from $(pwd)"
for slug in "${slugs[@]}"; do
  echo "Trying: submit50 $slug"
  if submit50 "$slug"; then
    echo "Submission succeeded: $slug"
    exit 0
  fi
  echo "Attempt failed: $slug"
done

# Fallback for hello if submit50 slugs are not accepted this year
if [[ "$problem" == "hello" ]]; then
  echo "submit50 did not accept hello for your cohort; running check50 as a fallback..."
  if check50 cs50/problems/2024/x/hello; then
    echo "check50 finished. Your cohort may not grade hello; progress page may not list it."
    exit 0
  fi
fi

echo "All attempts failed. Please verify the slug for your year in the course page." >&2
exit 1
