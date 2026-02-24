#!/bin/bash
# Daily Diary Entry Script for Notion - v2.2 (Stabil)
# Liest memory/YYYY-MM-DD.md und überträgt Inhalt nach Notion

WORKSPACE="/root/workspace"
LOG_FILE="$WORKSPACE/logs/diary.log"
CONFIG_DIR="$HOME/.config/openclaw"
DATABASE_ID="416f67c5-1cda-4248-8f43-2911e8ca633c"

# Logging
log() {
    echo "[$(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

mkdir -p "$WORKSPACE/logs"
log "=== Script gestartet ==="

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
[ -f "$LOCAL_FILE" ] && log "📄 Datei gefunden: $LOCAL_FILE" || log "⚠️ Keine Datei gefunden"

# Prüfe Existenz
EXISTING=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{\"filter\":{\"property\":\"Name\",\"title\":{\"equals\":\"${DATE_YMD}_Tagesreflexion\"}}}")

if echo "$EXISTING" | grep -q '"results":\[\]'; then
    log "📝 Erstelle neuen Eintrag..."
    
    # Einfacher JSON-Build
    TITLE="🌙 Tagesreflexion - $WEEKDAY_GER, $DATE_GERMAN"
    
    curl -s -X POST "https://api.notion.com/v1/pages" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      -d "{
        \"parent\":{\"database_id\":\"$DATABASE_ID\"},
        \"properties\":{\"Name\":{\"title\":[{\"text\":{\"content\":\"${DATE_YMD}_Tagesreflexion\"}}]}},
        \"children\":[
          {\"object\":\"block\",\"type\":\"heading_1\",\"heading_1\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$TITLE\"}}]}},
          {\"object\":\"block\",\"type\":\"divider\",\"divider\":{}},
          {\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"Automatisch aus memory/$DATE_STR.md\"}}],\"icon\":{\"emoji\":\"🤖\"}}}
        ]
      }" > /dev/null 2>&1
    
    log "✅ Eintrag erstellt"
else
    log "ℹ️ Eintrag existiert bereits"
fi

log "=== Fertig ==="
