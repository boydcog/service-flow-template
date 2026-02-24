#!/bin/bash
set -e

validate_gh_token() {
  local token_file=".gh-token"

  if [ ! -f "$token_file" ]; then
    echo "ERROR: $token_file not found"
    echo ""
    echo "GitHub token file is missing. Contact the template administrator:"
    echo ""
    grep -A 5 "^admins:" .claude/manifests/admins.yaml | grep -E "name|github|email" | sed 's/^/  /'
    echo ""
    exit 1
  fi

  GH_TOKEN=$(cat "$token_file")

  if [ -z "$GH_TOKEN" ]; then
    echo "ERROR: $token_file is empty"
    echo ""
    echo "GitHub token is empty. Contact the template administrator:"
    echo ""
    grep -A 5 "^admins:" .claude/manifests/admins.yaml | grep -E "name|github|email" | sed 's/^/  /'
    echo ""
    exit 1
  fi

  if ! curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/user > /dev/null 2>&1; then
    echo "ERROR: Invalid GitHub token"
    echo ""
    echo "GitHub token is invalid or expired. Contact the template administrator:"
    echo ""
    grep -A 5 "^admins:" .claude/manifests/admins.yaml | grep -E "name|github|email" | sed 's/^/  /'
    echo ""
    exit 1
  fi

  export GH_TOKEN
  return 0
}

validate_gh_token
