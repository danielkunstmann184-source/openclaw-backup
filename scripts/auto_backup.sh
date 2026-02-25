#!/bin/bash
# Auto-Backup Script - Täglicher Git-Commit & Push
# Täglich um 22:00 via systemd-Timer

WORKSPACE="/root/workspace"
LOG_FILE="$WORKSPACE/logs/backup.log"

log() {
    echo "[$(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$WORKSPACE" || exit 1

log "=== Auto-Backup gestartet ==="

# Prüfe auf Änderungen
if [ -z "$(git status --porcelain)" ]; then
    log "✅ Keine Änderungen zum Committen"
    log "=== Backup nicht nötig ==="
    exit 0
fi

# Git Config sicherstellen
git config user.email "peter@openclaw.local" 2>/dev/null || true
git config user.name "Peter" 2>/dev/null || true

# Add & Commit
log "📦 Füge Änderungen hinzu..."
git add -A

CHANGES=$(git status --short | wc -l)
log "📝 $CHANGES Dateien geändert"

log "💾 Erstelle Commit..."
if git commit -m "Auto-Backup: $(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M')"; then
    log "✅ Commit erfolgreich"
else
    log "❌ Commit fehlgeschlagen"
    exit 1
fi

# Push mit Token
log "🚀 Push zu GitHub..."
git remote set-url origin "https://danielkunstmann184-source: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@github.com/danielkunstmann184-source/openclaw-backup.git" 2>/dev/null

if git push origin master; then
    log "✅ Push erfolgreich"
    # Token wieder zurücksetzen
    git remote set-url origin "https://TOKEN@github.com/danielkunstmann184-source/openclaw-backup.git" 2>/dev/null
else
    log "❌ Push fehlgeschlagen"
    git remote set-url origin "https://TOKEN@github.com/danielkunstmann184-source/openclaw-backup.git" 2>/dev/null
    exit 1
fi

log "=== Backup erfolgreich ==="
