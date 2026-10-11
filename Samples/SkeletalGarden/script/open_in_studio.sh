#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
/usr/bin/open -a "${ADA_STUDIO_APP:-Ada Studio}" "$PROJECT_ROOT"
