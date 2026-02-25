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

# Wetter für heute holen (Open-Meteo API - kein Key nötig)
echo "" >> "$OUTPUT_FILE"
echo "🌤️ WETTER HEUTE ($TODAY):" >> "$OUTPUT_FILE"

# Koordinaten für Friedrichroda: 50.86, 10.57
WEATHER_JSON=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=50.86&longitude=10.57&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=Europe/Berlin&forecast_days=1" 2>/dev/null || echo '{}')

if command -v jq &>/dev/null; then
    MAX_TEMP=$(echo "$WEATHER_JSON" | jq -r '.daily.temperature_2m_max[0] // "??"')
    MIN_TEMP=$(echo "$WEATHER_JSON" | jq -r '.daily.temperature_2m_min[0] // "??"')
    PRECIP=$(echo "$WEATHER_JSON" | jq -r '.daily.precipitation_sum[0] // "0"')
    WEATHER_CODE=$(echo "$WEATHER_JSON" | jq -r '.daily.weathercode[0] // "0"')
else
    # Fallback ohne jq
    MAX_TEMP=$(echo "$WEATHER_JSON" | grep -o '"temperature_2m_max":\[[^]]*\]' | grep -o '[0-9.]*' | head -1)
    MIN_TEMP=$(echo "$WEATHER_JSON" | grep -o '"temperature_2m_min":\[[^]]*\]' | grep -o '[0-9.]*' | head -1)
    PRECIP="0"
    WEATHER_CODE="0"
fi

# Wetter-Code zu Beschreibung
 case "$WEATHER_CODE" in
     0) CONDITION="Klarer Himmel ☀️" ;;
     1|2|3) CONDITION="Teilweise bewölkt ⛅" ;;
     45|48) CONDITION="Nebel 🌫️" ;;
     51|53|55) CONDITION="Nieselregen 🌦️" ;;
     61|63|65) CONDITION="Regen 🌧️" ;;
     71|73|75) CONDITION="Schneefall 🌨️" ;;
     95|96|99) CONDITION="Gewitter ⛈️" ;;
     *) CONDITION="Wechselhaft ☁️" ;;
 esac
 
 echo "  📍 Friedrichroda" >> "$OUTPUT_FILE"
 echo "  🌡️  $MIN_TEMP°C bis $MAX_TEMP°C" >> "$OUTPUT_FILE"
 echo "  ☁️  $CONDITION" >> "$OUTPUT_FILE"
 
 # Regen-Warnung
 if [ "$PRECIP" != "0" ] && [ "$PRECIP" != "??" ]; then
     PRECIP_NUM=$(echo "$PRECIP" | cut -d. -f1)
     if [ "$PRECIP_NUM" -gt 0 ] 2>/dev/null; then
         echo "  🌧️  Niederschlag: ${PRECIP}mm" >> "$OUTPUT_FILE"
     fi
 fi

# Zusammenfassung
echo "" >> "$OUTPUT_FILE"
echo "📊 Zusammenfassung:" >> "$OUTPUT_FILE"
echo "- Analysierte Tage: $(grep -c '^📄' "$OUTPUT_FILE")" >> "$OUTPUT_FILE"
echo "- Datei erstellt: $(date -r "$OUTPUT_FILE" '+%H:%M')" >> "$OUTPUT_FILE"

# Log-Eintrag
echo "[$(TZ='Europe/Berlin' date)] Overnight Analysis erstellt" >> "$LOG_DIR/diary.log"
