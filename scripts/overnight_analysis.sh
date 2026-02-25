#!/bin/bash
# Overnight Analysis Script - Läuft vor dem Morgen-Briefing
# Analysiert Memory-Dateien und speichert Ergebnis

WORKSPACE="/root/workspace"
LOG_DIR="$WORKSPACE/logs"
OUTPUT_FILE="$LOG_DIR/overnight_analysis.txt"

# Datum (Berlin)
TODAY=$(TZ="Europe/Berlin" date '+%Y-%m-%d')
YESTERDAY=$(TZ="Europe/Berlin" date -d "yesterday" '+%Y-%m-%d' 2>/dev/null || date -d "yesterday" '+%Y-%m-%d')

# Ergebnis-Datei vorbereiten
echo "🧠 Overnight Analysis - $(TZ='Europe/Berlin' date)" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Suche nach Memory-Dateien der letzten 3 Tage
for days_ago in 0 1 2; do
    DATE=$(TZ="Europe/Berlin" date -d "$days_ago days ago" '+%Y-%m-%d' 2>/dev/null || date -d "$days_ago days ago" '+%Y-%m-%d')
    FILE="$WORKSPACE/memory/$DATE.md"
    
    if [ -f "$FILE" ]; then
        echo "📄 $DATE:" >> "$OUTPUT_FILE"
        
        # Extrahiere wichtige Abschnitte
        if grep -q "## ✅ Erledigt" "$FILE"; then
            echo "  ✅ Erledigt:" >> "$OUTPUT_FILE"
            grep "\- \[x\]" "$FILE" | head -3 | sed 's/^/    /' >> "$OUTPUT_FILE"
        fi
        
        if grep -q "### 🧠 Reflexion" "$FILE"; then
            echo "  🧠 Reflexion vorhanden" >> "$OUTPUT_FILE"
        fi
        
        # Zähle offene Tasks
        OPEN_TASKS=$(grep -c "\- \[ \]" "$FILE" 2>/dev/null || echo "0")
        if [ "$OPEN_TASKS" != "0" ] && [ "$OPEN_TASKS" -gt 0 ] 2>/dev/null; then
            echo "  ⏳ Offene Tasks: $OPEN_TASKS" >> "$OUTPUT_FILE"
        fi
        
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Zusammenfassung
echo "📊 Zusammenfassung:" >> "$OUTPUT_FILE"
echo "- Analysierte Tage: $(grep -c '^📄' "$OUTPUT_FILE")" >> "$OUTPUT_FILE"
echo "- Datei erstellt: $(date -r "$OUTPUT_FILE" '+%H:%M')" >> "$OUTPUT_FILE"

# Log-Eintrag
echo "[$(TZ='Europe/Berlin' date)] Overnight Analysis erstellt" >> "$LOG_DIR/diary.log"
