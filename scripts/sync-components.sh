#!/usr/bin/env bash
# Usage: ./scripts/sync-components.sh <project-dir>
# Description: Synchronize template components to a project directory

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project-dir>"
  echo "Example: $0 projects/my-project"
  exit 1
fi

PROJECT_DIR="$1"
TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Project directory not found: $PROJECT_DIR"
  exit 1
fi

# Ensure components directory exists in project
mkdir -p "$PROJECT_DIR/components"

# Sync components from template to project (delete extra files in project)
echo "🔄 Syncing components from template to $PROJECT_DIR..."
rsync -av --delete \
  "$TEMPLATE_DIR/components/" \
  "$PROJECT_DIR/components/" \
  --exclude=".DS_Store"

echo "✅ Component sync complete: $PROJECT_DIR"
echo ""
echo "Components synced:"
find "$PROJECT_DIR/components" -type f -name "*.tsx" -o -name "*.ts" | grep -E "^$PROJECT_DIR/components/(web|native|theme)/" | head -20
