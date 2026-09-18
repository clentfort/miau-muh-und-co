#!/usr/bin/env bash
# Environment setup for Google Jules (https://jules.google/docs/environment/).
# Configure this file as the "Initial Setup" command in the Jules repository
# configuration: bash scripts/jules-setup.sh
set -euo pipefail

NODE_VERSION=24

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

if command -v nvm >/dev/null 2>&1; then
  nvm install "$NODE_VERSION"
  nvm alias default "$NODE_VERSION"
  nvm use default
fi

node -v
python3 --version

npm ci
