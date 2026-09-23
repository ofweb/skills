#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

targets=()
for arg in "$@"; do
    targets+=("$(realpath "$arg")")
done

cd "$skill_dir"
exec vale --config .vale.ini "${targets[@]}"
