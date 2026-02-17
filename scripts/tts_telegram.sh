#!/bin/bash
# Telegram Voice Message Generator
# Nutzt sherpa-onnx für TTS + opusenc für Telegram-Format

TEXT="$1"
OUTPUT="${2:-/tmp/telegram_voice.ogg}"

if [ -z "$TEXT" ]; then
    echo "Usage: $0 'Text to speak' [output_file]"
    exit 1
fi

# Temporäre WAV-Datei
WAV_FILE="/tmp/tts_temp_$$.wav"

# TTS mit sherpa-onnx (Standard-Modell oder Espeak als Fallback)
if command -v sherpa-onnx-offline-tts &> /dev/null; then
    # Versuche sherpa-onnx mit deutschem Modell
    MODEL_DIR="$HOME/.openclaw/tools/sherpa-onnx-tts/models"
    
    if [ -f "$MODEL_DIR/model.onnx" ] && [ -s "$MODEL_DIR/model.onnx" ]; then
        sherpa-onnx-offline-tts \
            --vits-model="$MODEL_DIR/model.onnx" \
            --vits-tokens="$MODEL_DIR/tokens.txt" \
            --output-filename="$WAV_FILE" \
            --text="$TEXT" 2>/dev/null
    else
        # Fallback: Espeak
        espeak -v de -w "$WAV_FILE" "$TEXT" 2>/dev/null
    fi
else
    # Fallback: Espeak
    espeak -v de -w "$WAV_FILE" "$TEXT" 2>/dev/null
fi

# Konvertiere zu OGG/Opus (Telegram Voice Format)
if [ -f "$WAV_FILE" ]; then
    opusenc --bitrate 24 --vbr "$WAV_FILE" "$OUTPUT" 2>/dev/null
    rm -f "$WAV_FILE"
    
    if [ -f "$OUTPUT" ]; then
        echo "✅ Voice message created: $OUTPUT"
        exit 0
    fi
fi

echo "❌ Failed to create voice message"
exit 1
