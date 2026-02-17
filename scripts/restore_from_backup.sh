#!/bin/bash
# POST-REINSTALL RECOVERY SCRIPT
# Run this immediately after OpenClaw reinstall to restore all data

WORKSPACE="/home/ubuntu/.openclaw/workspace"
BACKUP_REPO="https://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@github.com/danielkunstmann184-source/openclaw-backup.git"

echo "🔄 RESTORING FROM BACKUP..."
echo "============================"

# Backup current empty workspace first
mv "$WORKSPACE" "$WORKSPACE.empty.$(date +%s)" 2>/dev/null

# Clone backup
cd /home/ubuntu/.openclaw || exit 1
git clone "$BACKUP_REPO" workspace

if [ $? -eq 0 ]; then
    echo "✅ RESTORE COMPLETE"
    echo ""
    echo "📊 Restored files:"
    ls -la "$WORKSPACE"/*.md
    echo ""
    echo "🧠 Peter now has full memory restored!"
else
    echo "❌ RESTORE FAILED"
    exit 1
fi
