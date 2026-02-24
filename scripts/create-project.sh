#!/usr/bin/env bash
# Usage: ./scripts/create-project.sh <project-name>
# Description: Create a new empty Vite+React project with template components

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project-name>"
  echo "Example: $0 my-project"
  exit 1
fi

PROJECT_NAME="$1"
PROJECTS_DIR="$(cd "$(dirname "$0")/../projects" && pwd)"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"
TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -d "$PROJECT_PATH" ]; then
  echo "❌ Project already exists: $PROJECT_PATH"
  exit 1
fi

echo "📦 Creating new Vite+React project: $PROJECT_NAME"
echo ""

# Create project with pnpm create vite
cd "$PROJECTS_DIR"
pnpm create vite "$PROJECT_NAME" --template react-ts

echo ""
echo "🔄 Syncing components from template..."
bash "$TEMPLATE_DIR/scripts/sync-components.sh" "$PROJECT_PATH"

echo ""
echo "📝 Installing dependencies..."
cd "$PROJECT_PATH"
pnpm install

echo ""
echo "✅ Project created successfully!"
echo ""
echo "Next steps:"
echo "  cd projects/$PROJECT_NAME"
echo "  pnpm dev"
