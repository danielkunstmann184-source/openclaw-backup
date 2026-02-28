#!/bin/bash
# Voice Message Poller - Prüft alle 5 Minuten auf neue Sprachnachrichten

INBOUND_DIR="/root/.openclaw/media/inbound"
PROCESSED_LOG="/root/workspace/logs/voice_processed.log"
LOCK_FILE="/tmp/voice_poller.lock"

# Lock-File verhindern doppelte Ausführung
[ -f "$LOCK_FILE" ] && exit 0
touch "$LOCK_FILE"

# Neue OGG-Dateien finden (nicht im Log vorhanden)
find "$INBOUND_DIR" -name "*.ogg" -type f | while read file; do
    filename=$(basename "$file")
    
    # Prüfe ob bereits verarbeitet
    if ! grep -q "$filename" "$PROCESSED_LOG" 2>/dev/null; then
        # Transkribiere
        text=$(whisper "$file" --model tiny --language de 2>/dev/null | tail -1)
        
        # Speichere Ergebnis
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $filename: $text" >> "$PROCESSED_LOG"
        
        # Benachrichtige via Telegram (einfacher Text)
        echo "🎙️ Sprachnachricht empfangen:\n$text" > /tmp/voice_notification.txt
    fi
done

rm -f "$LOCK_FILE"
