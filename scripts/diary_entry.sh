#!/bin/bash
# Daily Diary Entry Script for Notion - v3.0 (Mit Content-Import)
# Liest memory/YYYY-MM-DD.md und überträgt INHALT nach Notion

WORKSPACE="/root/workspace"
LOG_FILE="$WORKSPACE/logs/diary.log"
CONFIG_DIR="$HOME/.config/openclaw"
DATABASE_ID="416f67c5-1cda-4248-8f43-2911e8ca633c"

# Logging
log() {
    echo "[$(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

mkdir -p "$WORKSPACE/logs"
log "=== Script gestartet (v3.0) ==="

# Token laden
NOTION_TOKEN=$(grep "^NOTION_API_KEY=" "$CONFIG_DIR/.env.notion" 2>/dev/null | cut -d'=' -f2 | tr -d '[:space:]')
[ -z "$NOTION_TOKEN" ] && { log "❌ Token fehlt"; exit 1; }

# Datum mit Zeitzone Berlin
DATE_STR=${1:-$(TZ='Europe/Berlin' date '+%Y-%m-%d')}
DATE_YMD=$(echo $DATE_STR | tr -d '-')
DATE_GERMAN=$(TZ='Europe/Berlin' date -d "$DATE_STR" '+%d.%m.%Y' 2>/dev/null || TZ='Europe/Berlin' date '+%d.%m.%Y')
WEEKDAY=$(TZ='Europe/Berlin' date -d "$DATE_STR" '+%A' 2>/dev/null || TZ='Europe/Berlin' date '+%A')

case $WEEKDAY in
    Monday) WEEKDAY_GER="Montag" ;; Tuesday) WEEKDAY_GER="Dienstag" ;; Wednesday) WEEKDAY_GER="Mittwoch" ;;
    Thursday) WEEKDAY_GER="Donnerstag" ;; Friday) WEEKDAY_GER="Freitag" ;; Saturday) WEEKDAY_GER="Samstag" ;;
    Sunday) WEEKDAY_GER="Sonntag" ;;
esac

log "Datum: $DATE_STR ($WEEKDAY_GER, $DATE_GERMAN)"

# Lokale Datei prüfen
LOCAL_FILE="$WORKSPACE/memory/$DATE_STR.md"
if [ -f "$LOCAL_FILE" ]; then
    log "📄 Datei gefunden: $LOCAL_FILE"
    HAS_CONTENT=true
    # Lese Inhalt (max 3000 Zeichen für Notion)
    CONTENT=$(cat "$LOCAL_FILE" | head -c 3000)
else
    log "⚠️ Keine lokale Datei gefunden"
    HAS_CONTENT=false
fi

# Prüfe Existenz
EXISTING=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{\"filter\":{\"property\":\"Name\",\"title\":{\"equals\":\"${DATE_YMD}_Tagesreflexion\"}}}")

if echo "$EXISTING" | grep -q '"results":\[\]'; then
    log "📝 Erstelle neuen Eintrag mit Inhalt..."
    
    # Baue Blöcke
    BLOCKS="[{\"object\":\"block\",\"type\":\"heading_1\",\"heading_1\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"🌙 Tagesreflexion - $WEEKDAY_GER, $DATE_GERMAN\"}}]}},"
    BLOCKS="$BLOCKS{\"object\":\"block\",\"type\":\"divider\",\"divider\":{}},"
    
    if [ "$HAS_CONTENT" = true ]; then
        # Füge Inhalt als Callout hinzu
        # Escape für JSON
        SAFE_CONTENT=$(echo "$CONTENT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/ /g' | tr '\n' ' ' | sed 's/  */ /g' | head -c 2000)
        BLOCKS="$BLOCKS{\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"📝 Inhalt aus memory/$DATE_STR.md:\"}}],\"icon\":{\"emoji\":\"📄\"}}},"
        BLOCKS="$BLOCKS{\"object\":\"block\",\"type\":\"paragraph\",\"paragraph\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$SAFE_CONTENT\"}}]}}"
    else
        BLOCKS="$BLOCKS{\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"Keine lokale Datei gefunden\"}}],\"icon\":{\"emoji\":\"⚠️\"}}}"
    fi
    BLOCKS="$BLOCKS]"
    
    # Erstelle Page
    curl -s -X POST "https://api.notion.com/v1/pages" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      -d "{
        \"parent\":{\"database_id\":\"$DATABASE_ID\"},
        \"properties\":{\"Name\":{\"title\":[{\"text\":{\"content\":\"${DATE_YMD}_Tagesreflexion\"}}]}},
        \"children\":$BLOCKS
      }" > /dev/null 2>&1
    
    log "✅ Eintrag erstellt"
else
    log "ℹ️ Eintrag existiert bereits"
    
    # Optional: Aktualisiere mit Inhalt wenn vorhanden
    if [ "$HAS_CONTENT" = true ]; then
        log "📝 Aktualisiere mit Inhalt..."
        PAGE_ID=$(echo "$EXISTING" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ -n "$PAGE_ID" ]; then
            SAFE_CONTENT=$(echo "$CONTENT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/ /g' | tr '\n' ' ' | sed 's/  */ /g' | head -c 1500)
            
            # Füge neuen Block hinzu
            curl -s -X PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" \
              -H "Authorization: Bearer $NOTION_TOKEN" \
              -H "Notion-Version: 2022-06-28" \
              -H "Content-Type: application/json" \
              -d "{
                \"children\":[
                  {\"object\":\"block\",\"type\":\"divider\",\"divider\":{}},
                  {\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"🔄 Aktualisiert am $(TZ='Europe/Berlin' date '+%d.%m.%Y %H:%M')\"}}],\"icon\":{\"emoji\":\"🤖\"}}},
                  {\"object\":\"block\",\"type\":\"paragraph\",\"paragraph\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$SAFE_CONTENT\"}}]}}
                ]
              }" > /dev/null 2>&1
            log "✅ Eintrag aktualisiert"
        fi
    fi
fi

log "=== Fertig ==="
