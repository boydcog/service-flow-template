#!/bin/bash

# Web-Native Component Synchronization Check
# Ensures that Web and Native components maintain 1:1 parity
# Run after component modifications to verify consistency

set -e

WEB_DIR="components/web/ui"
NATIVE_DIR="components/native/ui"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "🔄 Checking Web-Native component synchronization..."
echo

# Check if directories exist
if [[ ! -d "$WEB_DIR" ]] || [[ ! -d "$NATIVE_DIR" ]]; then
  echo "${RED}❌ Component directories not found${NC}"
  exit 1
fi

# Count components
WEB_COUNT=$(find "$WEB_DIR" -maxdepth 1 -name "*.tsx" -type f | wc -l)
NATIVE_COUNT=$(find "$NATIVE_DIR" -maxdepth 1 -name "*.tsx" -type f | wc -l)

# Get array of web components (lowercase filenames without extension)
WEB_COMPONENTS=()
while IFS= read -r file; do
  NAME=$(basename "$file" .tsx)
  WEB_COMPONENTS+=("$NAME")
done < <(find "$WEB_DIR" -maxdepth 1 -name "*.tsx" -type f | sort)

# Get array of native components (PascalCase filenames without extension)
NATIVE_COMPONENTS=()
while IFS= read -r file; do
  NAME=$(basename "$file" .tsx)
  NATIVE_COMPONENTS+=("$NAME")
done < <(find "$NATIVE_DIR" -maxdepth 1 -name "*.tsx" -type f | sort)

HAS_ISSUES=0

# Function to convert lowercase to PascalCase
to_pascal_case() {
  echo "$1" | awk '{print toupper(substr($0,1,1)) substr($0,2)}'
}

# Function to convert PascalCase to lowercase
to_lowercase() {
  echo "$1" | awk '{print tolower(substr($0,1,1)) substr($0,2)}'
}

# Check for missing Native components
MISSING_NATIVE=()
for web_comp in "${WEB_COMPONENTS[@]}"; do
  native_name=$(to_pascal_case "$web_comp")
  found=0
  for native_comp in "${NATIVE_COMPONENTS[@]}"; do
    if [[ "$native_comp" == "$native_name" ]]; then
      found=1
      break
    fi
  done
  if [[ $found -eq 0 ]]; then
    MISSING_NATIVE+=("$web_comp")
  fi
done

# Check for missing Web components
MISSING_WEB=()
for native_comp in "${NATIVE_COMPONENTS[@]}"; do
  web_name=$(to_lowercase "$native_comp")
  found=0
  for web_comp in "${WEB_COMPONENTS[@]}"; do
    if [[ "$web_comp" == "$web_name" ]]; then
      found=1
      break
    fi
  done
  if [[ $found -eq 0 ]]; then
    MISSING_WEB+=("$native_comp")
  fi
done

# Report results
if [[ ${#MISSING_NATIVE[@]} -gt 0 ]]; then
  echo "${YELLOW}⚠️  Missing Native components:${NC}"
  for component in "${MISSING_NATIVE[@]}"; do
    NATIVE_NAME=$(to_pascal_case "$component")
    echo "  • $component.tsx (Web) → $NATIVE_NAME.tsx (Native) not found"
  done
  HAS_ISSUES=1
  echo
fi

if [[ ${#MISSING_WEB[@]} -gt 0 ]]; then
  echo "${YELLOW}⚠️  Missing Web components:${NC}"
  for component in "${MISSING_WEB[@]}"; do
    LOWER_NAME=$(to_lowercase "$component")
    echo "  • ${LOWER_NAME}.tsx (Web) not found for $component.tsx (Native)"
  done
  HAS_ISSUES=1
  echo
fi

if [[ $HAS_ISSUES -eq 0 ]]; then
  echo "${GREEN}✅ All components synchronized!${NC}"
  echo "   Web: $WEB_COUNT components"
  echo "   Native: $NATIVE_COUNT components"
  exit 0
else
  echo "${RED}❌ Component synchronization issues detected${NC}"
  echo "   Follow the naming convention:"
  echo "   • Web: lowercase (e.g., button.tsx)"
  echo "   • Native: PascalCase (e.g., Button.tsx)"
  exit 1
fi
