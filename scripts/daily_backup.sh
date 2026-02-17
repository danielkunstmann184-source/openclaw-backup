#!/bin/bash
# Daily Backup Script - FIXED VERSION
# Lädt Token aus Datei (nicht hardcoded)

WORKSPACE="/home/ubuntu/.openclaw/workspace"
DATE=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="$WORKSPACE/logs/backup.log"

# Token aus Datei laden (nicht in Git!)
if [ -f "$WORKSPACE/.github_token" ]; then
    GITHUB_TOKEN=$(cat "$WORKSPACE/.github_token" | tr -d '[:space:]')
else
    echo "[$DATE] ❌ .github_token nicht gefunden" | tee -a "$LOG_FILE"
    exit 1
fi

REPO_URL="https://${GITHUB_TOKEN}@github.com/danielkunstmann184-source/openclaw-backup.git"

cd "$WORKSPACE" || exit 1

# Git Remote setzen
if ! git remote get-url origin &>/dev/null; then
    git remote add origin "$REPO_URL"
else
    git remote set-url origin "$REPO_URL"
fi

# Git User
if ! git config --get user.email &>/dev/null; then
    git config user.email "peter@openclaw.local"
    git config user.name "Peter (OpenClaw)"
fi

# Add & Commit
git add -A
if git diff --cached --quiet; then
    echo "[$DATE] ℹ️ Keine Änderungen" | tee -a "$LOG_FILE"
    exit 0
fi

git commit -m "📦 Daily backup - $DATE" || exit 1

# Push
if git push origin master 2>&1 | tee -a "$LOG_FILE"; then
    echo "[$DATE] ✅ Backup erfolgreich" | tee -a "$LOG_FILE"
else
    echo "[$DATE] ❌ Backup fehlgeschlagen" | tee -a "$LOG_FILE"
    exit 1
fi
