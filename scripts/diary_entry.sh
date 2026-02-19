#!/bin/bash
# Daily Diary Entry Script for Notion - MIT AUTOMATISCHER CONTENT-ÜBERTRAGUNG
# Liest memory/YYYY-MM-DD.md und überträgt Inhalt nach Notion

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Token aus .env.notion laden
if [ -f "$WORKSPACE/.env.notion" ]; then
    NOTION_TOKEN=$(grep "^NOTION_API_KEY=" "$WORKSPACE/.env.notion" | cut -d'=' -f2 | tr -d '[:space:]')
else
    echo "❌ .env.notion nicht gefunden"
    exit 1
fi

if [ -z "$NOTION_TOKEN" ]; then
    echo "❌ Notion Token ist leer"
    exit 1
fi

DATABASE_ID="416f67c5-1cda-4248-8f43-2911e8ca633c"

# Datum festlegen (kann als Parameter übergeben werden, sonst heute)
DATE_STR=${1:-$(date '+%Y-%m-%d')}
DATE_YMD=$(echo $DATE_STR | tr -d '-')
DATE_GERMAN=$(date -d "$DATE_STR" '+%d.%m.%Y' 2>/dev/null || date '+%d.%m.%Y')
WEEKDAY=$(date -d "$DATE_STR" '+%A' 2>/dev/null || date '+%A')

# Wochentag auf Deutsch
case $WEEKDAY in
    Monday) WEEKDAY_GER="Montag" ;;
    Tuesday) WEEKDAY_GER="Dienstag" ;;
    Wednesday) WEEKDAY_GER="Mittwoch" ;;
    Thursday) WEEKDAY_GER="Donnerstag" ;;
    Friday) WEEKDAY_GER="Freitag" ;;
    Saturday) WEEKDAY_GER="Samstag" ;;
    Sunday) WEEKDAY_GER="Sonntag" ;;
esac

# Prüfe ob lokale Datei existiert
LOCAL_FILE="$WORKSPACE/memory/$DATE_STR.md"
if [ -f "$LOCAL_FILE" ]; then
    echo "📄 Lokale Datei gefunden: $LOCAL_FILE"
    HAS_LOCAL_CONTENT=true
else
    echo "⚠️ Keine lokale Datei gefunden: $LOCAL_FILE"
    HAS_LOCAL_CONTENT=false
fi

# Prüfe ob Eintrag bereits existiert
EXISTING=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"filter\": {
      \"property\": \"Name\",
      \"title\": {
        \"equals\": \"${DATE_YMD}_Tagesreflexion\"
      }
    }
  }")

if echo "$EXISTING" | grep -q '"results":\[\]'; then
    echo "📝 Eintrag für $DATE_YMD existiert noch nicht - erstelle neu..."
    
    # Baue JSON für children blocks
    if [ "$HAS_LOCAL_CONTENT" = true ]; then
        # Lese Datei und erstelle Notion-Blöcke
        # Einfacher Ansatz: Überschrift + Code-Block mit dem gesamten Inhalt
        CONTENT=$(cat "$LOCAL_FILE" | sed 's/"/\\"/g' | sed 's/\\/\\\\/g' | tr '\n' ' ' | sed 's/  */ /g')
        
        # Prüfe ob Content zu lang ist (Notion Limit ~2000 Zeichen pro Block)
        if [ ${#CONTENT} -gt 1800 ]; then
            # Teile in mehrere Absätze auf
            BLOCKS="[{\"object\": \"block\", \"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🌙 Tagesreflexion - $WEEKDAY_GER, $DATE_GERMAN\"}}]}},"
            BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"divider\", \"divider\": {}},"
            BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"callout\", \"callout\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"Automatisch übertragen aus memory/$DATE_STR.md\"}}], \"icon\": {\"emoji\": \"🤖\"}}},"
            BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Details siehe lokale Datei - Inhalt zu lang für Notion)\"}}]}}]"
        else
            BLOCKS="[{\"object\": \"block\", \"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🌙 Tagesreflexion - $WEEKDAY_GER, $DATE_GERMAN\"}}]}},"
            BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"divider\", \"divider\": {}},"
            BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"callout\", \"callout\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"Automatisch übertragen aus memory/$DATE_STR.md\"}}], \"icon\": {\"emoji\": \"🤖\"}}},"
            BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"$CONTENT\"}}]}}]"
        fi
    else
        # Standard-Template ohne lokale Daten
        BLOCKS="[{\"object\": \"block\", \"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🌙 Abend-Reflexion - $WEEKDAY_GER, $DATE_GERMAN\"}}]}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"divider\", \"divider\": {}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"☀️ Morgens / Vormittag\"}}]}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Keine lokalen Daten verfügbar)\"}}]}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"💼 Arbeit / Nachmittag\"}}]}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Keine lokalen Daten verfügbar)\"}}]}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🌆 Abend\"}}]}},"
        BLOCKS="$BLOCKS{\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Keine lokalen Daten verfügbar)\"}}]}}]"
    fi
    
    # Erstelle Page
    RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      -d "{
        \"parent\": {\"database_id\": \"$DATABASE_ID\"},
        \"properties\": {
          \"Name\": {\"title\": [{\"text\": {\"content\": \"${DATE_YMD}_Tagesreflexion\"}}]}
        },
        \"children\": $BLOCKS
      }")
    
    if echo "$RESPONSE" | grep -q '"id"'; then
        echo "✅ Tagebucheintrag für $DATE_YMD erstellt"
        if [ "$HAS_LOCAL_CONTENT" = true ]; then
            echo "📄 Mit Inhalt aus lokaler Datei"
        fi
        exit 0
    else
        echo "❌ Fehler beim Erstellen: $RESPONSE"
        exit 1
    fi
else
    echo "ℹ️ Eintrag für $DATE_YMD existiert bereits"
    
    # Optional: Update mit lokalen Daten wenn vorhanden
    if [ "$HAS_LOCAL_CONTENT" = true ]; then
        echo "📝 Lokale Datei vorhanden - prüfe auf Updates..."
        # Hier könnte man den bestehenden Eintrag updaten
        # Für jetzt: nur Info
    fi
    
    exit 0
fi
