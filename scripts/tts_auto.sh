#!/bin/bash
# TTS Wrapper für Auto-Modus - Natürliche deutsche Sprache mit gTTS
# KONVERTIERT LANGE TEXTE mit Python direkt (nicht gtts-cli)

TEXT="$1"
OUTPUT_FILE="${2:-/root/workspace/media/tts_output.ogg}"

if [ -z "$TEXT" ]; then
    echo "Usage: $0 'Text zu sprechen' [output.ogg]"
    exit 1
fi

# Temporäre MP3 Datei
TMP_MP3=$(mktemp /tmp/tts_XXXXXX.mp3)

# Python direkt für lange Texte
python3 <> PYEOF
from gtts import gTTS
text = """$TEXT"""
tts = gTTS(text=text, lang='de', slow=False)
tts.save('$TMP_MP3')
PYEOF

# Konvertiere zu OGG (Telegram-Format)
ffmpeg -i "$TMP_MP3" -c:a libopus -b:a 24k -y "$OUTPUT_FILE" 2> /dev/null

# Aufräumen
rm -f "$TMP_MP3"

# Ausgabe Pfad
echo "$OUTPUT_FILE"
