#!/usr/bin/env bash
# Second Brain Manager Installation Script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=== Installing Second Brain Host Manager ==="

# 1. Create config directory
sudo mkdir -p /etc/second-brain
if [ ! -f /etc/second-brain/settings.yml ]; then
    echo "Creating /etc/second-brain/settings.yml from template..."
    sudo cp "${REPO_DIR}/config/settings.example.yml" /etc/second-brain/settings.yml
fi

# 2. Symlink CLI to /usr/local/bin
sudo ln -sf "${SCRIPT_DIR}/second_brain.py" /usr/local/bin/second-brain
sudo chmod +x "${SCRIPT_DIR}/second_brain.py"

echo "Installation complete!"
echo "Run 'second-brain status' to check your system."
