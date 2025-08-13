#!/bin/bash
set -e

echo "📥 Pulling latest changes..."
git pull --rebase origin master

echo "📦 Adding notebook files..."
git add *.ipynb

echo "📝 Committing changes..."
git commit -m "Update notebooks"

echo "🚀 Pushing changes..."
git push origin master

echo "✅ Done."

