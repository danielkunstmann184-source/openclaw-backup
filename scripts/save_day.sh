#!/bin/bash
# save_day.sh - Persistiert alle wichtigen Informationen des Tages
# Nutzung: ./scripts/save_day.sh [OPTIONAL: Zusammenfassung als Parameter]

set -e

WORKSPACE="/home/ubuntu/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"
DIARY_LOG="$WORKSPACE/logs/diary.log"

echo "[$(date '+%Y-%m-%d %H:%M')] 💾 Starte Tages-Speicherung..." >> "$DIARY_LOG"

# Stelle sicher, dass das Memory-Verzeichnis existiert
mkdir -p "$MEMORY_DIR"

# Erstelle oder aktualisiere die Tagesdatei
if [ ! -f "$TODAY_FILE" ]; then
    echo "# $TODAY" > "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "## Tagesablauf" >> "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "### Morgens / Vormittag" >> "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "### Arbeit / Nachmittag" >> "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "### Abend" >> "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "## 🙏 Dankbarkeit" >> "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "## 🎯 Ausblick Morgen" >> "$TODAY_FILE"
    echo "" >> "$TODAY_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M')] ✅ Neue Tagesdatei erstellt: $TODAY_FILE" >> "$DIARY_LOG"
fi

# Wenn eine Zusammenfassung als Parameter übergeben wurde, füge sie hinzu
if [ -n "$1" ]; then
    echo "" >> "$TODAY_FILE"
    echo "### Update $(date '+%H:%M')" >> "$TODAY_FILE"
    echo "$1" >> "$TODAY_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M')] 📝 Zusammenfassung hinzugefügt" >> "$DIARY_LOG"
fi

# Backup in Git
cd "$WORKSPACE"
if git diff --quiet && git diff --cached --quiet; then
    echo "[$(date '+%Y-%m-%d %H:%M')] ℹ️ Keine Änderungen zum Commiten" >> "$DIARY_LOG"
else
    git add -A >> "$DIARY_LOG" 2>&1
    git commit -m "💾 Manuelles Speichern - $TODAY $(date '+%H:%M')" >> "$DIARY_LOG" 2>&1
    git push origin master >> "$DIARY_LOG" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M')] ✅ Backup gepusht" >> "$DIARY_LOG"
fi

echo "[$(date '+%Y-%m-%d %H:%M')] ✓ Tages-Speicherung abgeschlossen" >> "$DIARY_LOG"
echo "Tagesdatei: $TODAY_FILE"
