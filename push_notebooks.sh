#!/bin/bash
# push_notebooks.sh
# Automatically stage, commit, and push all changes in the repo

# Exit immediately if a command exits with a non-zero status
set -e

echo "Staging all changes..."
git add -A

# Generate commit message with timestamp
COMMIT_MSG="Auto commit on $(date '+%Y-%m-%d %H:%M:%S')"
echo "Committing with message: $COMMIT_MSG"
git commit -m "$COMMIT_MSG" || echo "No changes to commit."

# Push to current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Pushing to branch: $CURRENT_BRANCH"
git push origin "$CURRENT_BRANCH"

echo "✅ Push complete."
