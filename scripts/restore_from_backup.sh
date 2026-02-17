#!/bin/bash
# POST-REINSTALL RECOVERY SCRIPT

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Token aus Backup-Repo laden (wird nach Restore verfügbar)
if [ -f "$WORKSPACE/.github_token" ]; then
    TOKEN=$(cat "$WORKSPACE/.github_token" | tr -d '[:space:]')
    BACKUP_REPO="https://${TOKEN}@github.com/danielkunstmann184-source/openclaw-backup.git"
else
    echo "❌ .github_token nicht gefunden. Manuelle Eingabe nötig."
    exit 1
fi

echo "🔄 RESTORE FROM BACKUP..."

mv "$WORKSPACE" "$WORKSPACE.empty.$(date +%s)" 2>/dev/null
cd /home/ubuntu/.openclaw || exit 1
git clone "$BACKUP_REPO" workspace

if [ $? -eq 0 ]; then
    echo "✅ RESTORE COMPLETE"
else
    echo "❌ RESTORE FAILED"
    exit 1
fi
