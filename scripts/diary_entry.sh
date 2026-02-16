#!/bin/bash
# Daily Diary Entry Script for Notion
# Runs at 23:40 UTC

WORKSPACE="/home/ubuntu/.openclaw/workspace"
NOTION_TOKEN="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"
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

# Create page in Notion
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2025-09-03" \
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
  }"
