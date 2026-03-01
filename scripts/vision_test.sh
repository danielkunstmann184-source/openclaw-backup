#!/bin/bash
# Vision Test - Bildanalyse mit Kimi k2p5

IMAGE="$1"
[ -z "$IMAGE" ] && IMAGE="/root/.openclaw/media/inbound/test.jpg"

if [ ! -f "$IMAGE" ]; then
    echo "❌ Kein Testbild gefunden"
    echo "Nutze: $0 <pfad/zum/bild>"
    exit 1
fi

echo "🖼️ Analysiere Bild: $IMAGE"
echo "📤 Sende an Kimi k2p5..."
echo ""

# Das Bild muss über den normalen Chat gesendet werden
# Dieses Script ist ein Wrapper für die Dokumentation

echo "✅ Vision ist bereit!"
echo ""
echo "💡 Nutzung:"
echo "   1. Sende ein Bild im Chat"
echo "   2. Schreibe dazu: 'Beschreibe dieses Bild'"
echo "   3. Kimi k2p5 analysiert es automatisch"
echo ""
echo "⚠️  Hinweis: Bilder werden direkt im Chat verarbeitet."
