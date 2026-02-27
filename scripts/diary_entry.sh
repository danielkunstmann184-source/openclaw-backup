#!/bin/bash
# Daily Diary Entry Script for Notion - v3.2 (Automatische schöne Formatierung)
# Liest memory/YYYY-MM-DD.md und überträgt INHALT formatiert nach Notion

WORKSPACE="/root/workspace"
LOG_FILE="$WORKSPACE/logs/diary.log"
CONFIG_DIR="$HOME/.config/openclaw"
DATABASE_ID="416f67c5-1cda-4248-8f43-2911e8ca633c"

# Logging
log() {
    echo "[$(TZ='Europe/Berlin' date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# JSON escaping für Notion
json_escape() {
    echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/ /g' | sed 's/  */ /g'
}

mkdir -p "$WORKSPACE/logs"
log "=== Script gestartet (v3.2) ==="

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
else
    log "⚠️ Keine lokale Datei gefunden"
    HAS_CONTENT=false
fi

# Extrahiere Stichwort aus Tagesdatei
extract_keyword() {
    local file="$1"
    local keyword=""
    
    # Suche nach Fokus
    if grep -q "Fokus" "$file" 2>/dev/null; then
        keyword=$(grep -A1 "Fokus" "$file" | tail -1 | sed 's/^- //; s/^[[:space:]]*//' | cut -d' ' -f1-3)
    fi
    
    # Falls kein Fokus gefunden, nimm ersten wichtigen Begriff
    if [ -z "$keyword" ]; then
        keyword=$(grep -E "^\*\*|^\-" "$file" | head -1 | sed 's/^[\*\-] //; s/^\*\*//' | cut -d' ' -f1-2)
    fi
    
    # Falls immer noch leer, nimm Aktivität
    if [ -z "$keyword" ]; then
        keyword=$(grep -E "Büro|Akquise|Sauna|Sport|Termin" "$file" | head -1 | cut -d' ' -f1)
    fi
    
    # Cleanup
    keyword=$(echo "$keyword" | tr -d '\n' | sed 's/[[:space:]]*$//')
    
    echo "$keyword"
}
build_blocks() {
    local file="$1"
    local blocks=""
    local first=true
    
    while IFS= read -r line; do
        # Überspringe leere Zeilen am Anfang
        [ "$first" = true ] && [ -z "$line" ] && continue
        first=false
        
        # Escape für JSON
        local safe_line=$(json_escape "$line")
        
        if [ -z "$line" ]; then
            # Leere Zeile = Divider (aber nicht doppelt)
            continue
        elif [[ "$line" =~ ^#+\  ]]; then
            # Heading (## Überschrift)
            local level=$(echo "$line" | grep -o '^#*' | wc -c)
            level=$((level - 1))
            [ $level -gt 3 ] && level=3
            local text=$(echo "$line" | sed 's/^#* //')
            safe_line=$(json_escape "$text")
            [ -n "$blocks" ] && blocks="$blocks,"
            blocks="$blocks{\"object\":\"block\",\"type\":\"heading_$level\",\"heading_$level\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$safe_line\"}}]}}"
        elif [[ "$line" =~ ^[\*\-]\  ]]; then
            # Bullet point
            local text=$(echo "$line" | sed 's/^[\*\-] //')
            safe_line=$(json_escape "$text")
            [ -n "$blocks" ] && blocks="$blocks,"
            blocks="$blocks{\"object\":\"block\",\"type\":\"bulleted_list_item\",\"bulleted_list_item\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$safe_line\"}}]}}"
        elif [[ "$line" =~ ^\|\  ]]; then
            # Tabelle (als Callout)
            safe_line=$(json_escape "$line")
            [ -n "$blocks" ] && blocks="$blocks,"
            blocks="$blocks{\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$safe_line\"}}],\"icon\":{\"emoji\":\"📊\"}}}"
        else
            # Normaler Paragraph (nur wenn nicht leer)
            [ -n "$safe_line" ] || continue
            [ -n "$blocks" ] && blocks="$blocks,"
            blocks="$blocks{\"object\":\"block\",\"type\":\"paragraph\",\"paragraph\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"$safe_line\"}}]}}"
        fi
    done < "$file"
    
    echo "$blocks"
}

if [ "$HAS_CONTENT" = true ]; then
    KEYWORD=$(extract_keyword "$LOCAL_FILE")
    [ -n "$KEYWORD" ] && KEYWORD="_$KEYWORD"
else
    KEYWORD=""
fi

log "Stichwort: ${KEYWORD:-keines}"

# Prüfe Existenz
EXISTING=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{\"filter\":{\"property\":\"Name\",\"title\":{\"equals\":\"${DATE_YMD}${KEYWORD}_Tagesreflexion\"}}}")

if echo "$EXISTING" | grep -q '"results":\[\]'; then
    # NEUER EINTRAG
    log "📝 Erstelle neuen Eintrag mit formatiertem Inhalt..."
    
    # Haupttitel
    BLOCKS="{\"object\":\"block\",\"type\":\"heading_1\",\"heading_1\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"🌙 Tagesreflexion - $WEEKDAY_GER, $DATE_GERMAN\"}}]}}"
    
    if [ "$HAS_CONTENT" = true ]; then
        # Füge formatierte Inhaltsblöcke hinzu
        CONTENT_BLOCKS=$(build_blocks "$LOCAL_FILE")
        [ -n "$CONTENT_BLOCKS" ] && BLOCKS="$BLOCKS,$CONTENT_BLOCKS"
    else
        BLOCKS="$BLOCKS,{\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"Keine Tagesdatei gefunden\"}}],\"icon\":{\"emoji\":\"⚠️\"}}}"
    fi
    
    # Footer
    BLOCKS="$BLOCKS,{\"object\":\"block\",\"type\":\"divider\",\"divider\":{}},"
    BLOCKS="$BLOCKS{\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"Automatisch übertragen aus memory/$DATE_STR.md\"}}],\"icon\":{\"emoji\":\"🤖\"}}}"
    
    # Erstelle Page
    RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      -d "{
        \"parent\":{\"database_id\":\"$DATABASE_ID\"},
        \"properties\":{\"Name\":{\"title\":[{\"text\":{\"content\":\"${DATE_YMD}${KEYWORD}_Tagesreflexion\"}}]}},
        \"children\":[$BLOCKS]
      }")
    
    if echo "$RESPONSE" | grep -q '"id"'; then
        log "✅ Eintrag erstellt"
    else
        log "❌ Fehler beim Erstellen: $(echo $RESPONSE | head -c 200)"
    fi
else
    # BESTEHENDER EINTRAG - AKTUALISIERE
    log "📝 Eintrag existiert - aktualisiere mit formatiertem Inhalt..."
    
    PAGE_ID=$(echo "$EXISTING" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$PAGE_ID" ] && [ "$HAS_CONTENT" = true ]; then
        # Lösche alte Blöcke (außer Titel wenn möglich, sonst einfach neuen Inhalt anhängen)
        # Wir fügen einen "Aktualisiert"-Block hinzu
        
        BLOCKS="{\"object\":\"block\",\"type\":\"divider\",\"divider\":{}}"
        
        # Füge neuen formatierten Inhalt hinzu
        CONTENT_BLOCKS=$(build_blocks "$LOCAL_FILE")
        [ -n "$CONTENT_BLOCKS" ] && BLOCKS="$BLOCKS,$CONTENT_BLOCKS"
        
        # Aktualisierungshinweis
        BLOCKS="$BLOCKS,{\"object\":\"block\",\"type\":\"callout\",\"callout\":{\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"🔄 Aktualisiert am $(TZ='Europe/Berlin' date '+%d.%m.%Y %H:%M') aus memory/$DATE_STR.md\"}}],\"icon\":{\"emoji\":\"🤖\"}}}"
        
        # Füge neue Blöcke hinzu
        RESPONSE=$(curl -s -X PATCH "https://api.notion.com/v1/blocks/$PAGE_ID/children" \
          -H "Authorization: Bearer $NOTION_TOKEN" \
          -H "Notion-Version: 2022-06-28" \
          -H "Content-Type: application/json" \
          -d "{\"children\":[$BLOCKS]}")
        
        if echo "$RESPONSE" | grep -q '"id"'; then
            log "✅ Eintrag aktualisiert"
        else
            log "⚠️ Konnte nicht aktualisieren: $(echo $RESPONSE | head -c 200)"
        fi
    else
        log "ℹ️ Kein Inhalt zum Aktualisieren"
    fi
fi

log "=== Fertig ==="
