#!/bin/bash
# Daily Diary Entry Script for Notion - FIXED VERSION
# Lädt Token aus Datei, aktualisierte API-Version

WORKSPACE="/home/ubuntu/.openclaw/workspace"

# Token aus .env.notion laden (nicht hardcoded!)
if [ -f "$WORKSPACE/.env.notion" ]; then
    NOTION_TOKEN=$(grep "^NOTION_API_KEY=" "$WORKSPACE/.env.notion" | cut -d'=' -f2 | tr -d '[:space:]')
else
    echo "❌ .env.notion nicht gefunden"
    exit 1
fi

# Prüfe ob Token gesetzt
if [ -z "$NOTION_TOKEN" ]; then
    echo "❌ Notion Token ist leer"
    exit 1
fi

DATABASE_ID="416f67c5-1cda-4248-8f43-2911e8ca633c"

# Get today's date in German
DATE_STR=$(date '+%Y%m%d')
DATE_GERMAN=$(date '+%d.%m.%Y')
WEEKDAY=$(date '+%A')

# Translate weekday to German
case $WEEKDAY in
    Monday) WEEKDAY_GER="Montag" ;;
    Tuesday) WEEKDAY_GER="Dienstag" ;;
    Wednesday) WEEKDAY_GER="Mittwoch" ;;
    Thursday) WEEKDAY_GER="Donnerstag" ;;
    Friday) WEEKDAY_GER="Freitag" ;;
    Saturday) WEEKDAY_GER="Samstag" ;;
    Sunday) WEEKDAY_GER="Sonntag" ;;
esac

# Prüfe ob Eintrag für heute bereits existiert (einfache Prüfung via Titel)
EXISTING=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"filter\": {
      \"property\": \"Name\",
      \"title\": {
        \"equals\": \"${DATE_STR}_Tagesreflexion\"
      }
    }
  }" | grep -o '"results":\[\]' || echo "not_found")

if [ "$EXISTING" != "not_found" ]; then
    echo "ℹ️ Eintrag für $DATE_STR existiert bereits"
    exit 0
fi

# Create page in Notion
RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"database_id\": \"$DATABASE_ID\"},
    \"properties\": {
      \"Name\": {\"title\": [{\"text\": {\"content\": \"${DATE_STR}_Tagesreflexion\"}}]}
    },
    \"children\": [
      {\"object\": \"block\", \"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🌙 Abend-Reflexion - $WEEKDAY_GER, $DATE_GERMAN\"}}]}},
      {\"object\": \"block\", \"type\": \"divider\", \"divider\": {}},
      {\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"☀️ Morgens / Vormittag\"}}]}},
      {\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Automatisch generiert - Details folgen)\"}}]}},
      {\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"💼 Arbeit / Nachmittag\"}}]}},
      {\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Automatisch generiert - Details folgen)\"}}]}},
      {\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🌆 Abend\"}}]}},
      {\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Automatisch generiert - Details folgen)\"}}]}},
      {\"object\": \"block\", \"type\": \"divider\", \"divider\": {}},
      {\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🙏 Dankbarkeit\"}}]}},
      {\"object\": \"block\", \"type\": \"numbered_list_item\", \"numbered_list_item\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"\"}}]}},
      {\"object\": \"block\", \"type\": \"numbered_list_item\", \"numbered_list_item\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"\"}}]}},
      {\"object\": \"block\", \"type\": \"numbered_list_item\", \"numbered_list_item\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"\"}}]}},
      {\"object\": \"block\", \"type\": \"divider\", \"divider\": {}},
      {\"object\": \"block\", \"type\": \"heading_2\", \"heading_2\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"🎯 Ausblick Morgen\"}}]}},
      {\"object\": \"block\", \"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"(Wird aus MEMORY.md ermittelt)\"}}]}}
    ]
  }")

# Prüfe Response
if echo "$RESPONSE" | grep -q '"id"'; then
    echo "✅ Tagebucheintrag für $DATE_STR erstellt"
    exit 0
else
    echo "❌ Fehler beim Erstellen: $RESPONSE"
    exit 1
fi
