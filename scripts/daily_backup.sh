#!/bin/bash
# Daily Backup Script for OpenClaw Workspace
# Runs at 23:30 UTC
# ROBUST VERSION - works even after reinstall

WORKSPACE="/home/ubuntu/.openclaw/workspace"
DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="$WORKSPACE/logs/backup.log"
GITHUB_TOKEN="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"
REPO_URL="https://${GITHUB_TOKEN}@github.com/danielkunstmann184-source/openclaw-backup.git"

cd "$WORKSPACE" || exit 1

# Ensure git remote is configured (in case of reinstall)
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# Configure git user if not set
git config user.email "peter@openclaw.local" 2>/dev/null || true
git config user.name "Peter (OpenClaw)" 2>/dev/null || true

# Add all changes
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "[$DATE] No changes to backup"
    exit 0
fi

# Commit with timestamp
git commit -m "📦 Daily backup - $DATE

Changes:
$(git diff --cached --stat | tail -1)

Auto-committed by daily_backup.sh"

# Push to GitHub
if git push origin master; then
    echo "[$DATE] ✅ Backup successful"
else
    echo "[$DATE] ❌ Backup failed - trying force pull first"
    git pull origin master --rebase || true
    if git push origin master; then
        echo "[$DATE] ✅ Backup successful after rebase"
    else
        echo "[$DATE] ❌ Backup failed permanently"
        exit 1
    fi
fi
