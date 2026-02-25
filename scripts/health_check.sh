#!/bin/bash
# Health Check Script - Prüft alle kritischen Systeme
# Täglich um 06:00 via systemd-Timer

WORKSPACE="/root/workspace"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/health_check.log"
ALERT_FILE="$LOG_DIR/health_alert.txt"

log() {
    echo "[$(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

alert() {
    echo "$1" >> "$ALERT_FILE"
    # Auch ins Log
    log "🚨 ALERT: $1"
}

# Datei vorbereiten
echo "🩺 Health Check - $(TZ='Europe/Berlin' date)" > "$ALERT_FILE"
echo "" >> "$ALERT_FILE"

ERRORS=0

# 1. Prüfe systemd-Timer
log "Prüfe systemd-Timer..."
for timer in notion-diary overnight-analysis; do
    if systemctl is-active --quiet $timer.timer; then
        log "✅ $timer.timer aktiv"
    else
        alert "❌ $timer.timer INAKTIV"
        ((ERRORS++))
        # Versuche zu starten
        systemctl start $timer.timer 2>/dev/null && alert "   🔧 $timer.timer neu gestartet" || alert "   ❌ $timer.timer konnte nicht gestartet werden"
    fi
done

# 2. Prüfe OpenClaw Cron-Jobs
log "Prüfe OpenClaw Cron-Jobs..."
CRON_COUNT=$(openclaw cron list 2>/dev/null | grep -c "MAIN" || echo "0")
if [ "$CRON_COUNT" -ge 10 ]; then
    log "✅ $CRON_COUNT Cron-Jobs aktiv"
else
    alert "❌ Nur $CRON_COUNT Cron-Jobs gefunden (erwartet: 10+)"
    ((ERRORS++))
fi

# 3. Prüfe API-Keys
log "Prüfe API-Keys..."
if [ -f "$HOME/.config/openclaw/.env.notion" ]; then
    NOTION_KEY=$(grep "NOTION_API_KEY" "$HOME/.config/openclaw/.env.notion" | cut -d'=' -f2 | tr -d '[:space:]' | head -c 10)
    if [ -n "$NOTION_KEY" ]; then
        log "✅ Notion API Key vorhanden"
    else
        alert "❌ Notion API Key leer"
        ((ERRORS++))
    fi
else
    alert "❌ Notion API Key Datei fehlt"
    ((ERRORS++))
fi

# 4. Prüfe Git-Status
log "Prüfe Git-Status..."
cd "$WORKSPACE"
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    UNCOMMITTED=$(git status --short | wc -l)
    alert "⚠️ $UNCOMMITTED uncommitted Änderungen"
    # Auto-commit versuchen
    git add -A 2>/dev/null
    git commit -m "Auto-Backup: $(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M')" 2>/dev/null && alert "   🔧 Auto-Commit erfolgreich" || alert "   ❌ Auto-Commit fehlgeschlagen"
else
    log "✅ Git-Status sauber"
fi

# 5. Prüfe Memory-Dateien
log "Prüfe Memory-Dateien..."
TODAY=$(TZ='Europe/Berlin' date '+%Y-%m-%d')
if [ -f "$WORKSPACE/memory/$TODAY.md" ]; then
    log "✅ Heutige Memory-Datei existiert"
else
    alert "⚠️ Heutige Memory-Datei fehlt (optional)"
fi

# 6. Prüfe Logs
log "Prüfe Logs..."
if [ -f "$LOG_DIR/diary_systemd.log" ]; then
    LAST_ENTRY=$(tail -1 "$LOG_DIR/diary_systemd.log" 2>/dev/null | grep -oE '^\[[0-9-]+' | tr -d '[]')
    if [ "$LAST_ENTRY" = "$TODAY" ] || [ "$LAST_ENTRY" = "$(TZ='Europe/Berlin' date -d yesterday '+%Y-%m-%d')" ]; then
        log "✅ Diary-Log aktuell"
    else
        alert "⚠️ Diary-Log nicht aktuell (letzter Eintrag: $LAST_ENTRY)"
    fi
else
    alert "❌ Diary-Log fehlt"
    ((ERRORS++))
fi

# Zusammenfassung
echo "" >> "$ALERT_FILE"
if [ $ERRORS -eq 0 ]; then
    echo "✅ ALLE SYSTEME OK" >> "$ALERT_FILE"
    log "=== Health Check erfolgreich ==="
    exit 0
else
    echo "❌ $ERRORS PROBLEME GEFUNDEN" >> "$ALERT_FILE"
    log "=== Health Check mit $ERRORS Fehlern beendet ==="
    exit 1
fi
