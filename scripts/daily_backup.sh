#!/bin/bash
# Daily Backup Script for OpenClaw Workspace
# Runs at 23:30 UTC

WORKSPACE="/home/ubuntu/.openclaw/workspace"
DATE=$(date '+%Y-%m-%d %H:%M')

cd "$WORKSPACE" || exit 1

# Add all changes
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "[$DATE] No changes to backup"
    exit 0
fi

# Commit with timestamp
git commit -m "Daily backup - $DATE"

# Push to GitHub
if git push origin master; then
    echo "[$DATE] Backup successful"
else
    echo "[$DATE] Backup failed"
    exit 1
fi
