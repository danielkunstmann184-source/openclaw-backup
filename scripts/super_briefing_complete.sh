#!/bin/bash
# KOMPLETTES SUPER-BRIEFING - Mit funktionierenden APIs

WORKSPACE="/root/workspace"
LOG_DIR="$WORKSPACE/logs"
BRIEFING_FILE="$LOG_DIR/super_briefing_complete.txt"

# Brave API Key laden
export BRAVE_API_KEY=$(cat ~/.config/openclaw/.env.brave 2>/dev/null | grep "BRAVE_API_KEY=" | cut -d'=' -f2)

# Datum
TODAY=$(TZ="Europe/Berlin" date '+%Y-%m-%d')
TODAY_GERMAN=$(TZ="Europe/Berlin" date '+%d.%m.%Y')
WEEKDAY=$(TZ="Europe/Berlin" date '+%A')

case $WEEKDAY in
    Monday) WEEKDAY_GER="Montag" ;; Tuesday) WEEKDAY_GER="Dienstag" ;; Wednesday) WEEKDAY_GER="Mittwoch" ;;
    Thursday) WEEKDAY_GER="Donnerstag" ;; Friday) WEEKDAY_GER="Freitag" ;; Saturday) WEEKDAY_GER="Samstag" ;;
    Sunday) WEEKDAY_GER="Sonntag" ;;
esac

echo "🌅 SUPER-BRIEFING - $WEEKDAY_GER, $TODAY_GERMAN" > "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# 1. SYSTEM-CHECK
echo "🩺 SYSTEM:" >> "$BRIEFING_FILE"
cd "$WORKSPACE"
UNCOMMITTED=$(git status --short 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "  ⚠️ $UNCOMMITTED uncommitted Änderungen" >> "$BRIEFING_FILE"
else
    echo "  ✅ Alles synchronisiert" >> "$BRIEFING_FILE"
fi
echo "" >> "$BRIEFING_FILE"

# 2. WETTER (Open-Meteo - funktioniert zuverlässig)
echo "🌤️ WETTER FRIEDRICHRODA:" >> "$BRIEFING_FILE"
WEATHER=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=50.86&longitude=10.57&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=Europe/Berlin&forecast_days=1" 2>/dev/null)

MAX=$(echo "$WEATHER" | grep -o '"temperature_2m_max":\[[0-9.]*\]' | grep -o '[0-9.]*' | head -1)
MIN=$(echo "$WEATHER" | grep -o '"temperature_2m_min":\[[0-9.]*\]' | grep -o '[0-9.]*' | head -1)
CODE=$(echo "$WEATHER" | grep -o '"weathercode":\[[0-9]*\]' | grep -o '[0-9]*' | head -1)
RAIN=$(echo "$WEATHER" | grep -o '"precipitation_sum":\[[0-9.]*\]' | grep -o '[0-9.]*' | head -1)

case "$CODE" in
    0) ICON="☀️"; DESC="Klarer Himmel" ;;
    1|2|3) ICON="⛅"; DESC="Teils bewölkt" ;;
    45|48) ICON="🌫️"; DESC="Nebel" ;;
    51|53|55|61|63|65) ICON="🌧️"; DESC="Regen" ;;
    71|73|75) ICON="🌨️"; DESC="Schnee" ;;
    95|96|99) ICON="⛈️"; DESC="Gewitter" ;;
    *) ICON="☁️"; DESC="Wechselhaft" ;;
esac

echo "  $ICON $DESC" >> "$BRIEFING_FILE"
echo "  🌡️ $MIN°C bis $MAX°C" >> "$BRIEFING_FILE"
[ -n "$RAIN" ] && [ "$RAIN" != "0" ] && [ "$RAIN" != "0.0" ] && echo "  🌧️ Niederschlag: ${RAIN}mm" >> "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# 3. KRYPTO (CoinGecko - funktioniert)
echo "💰 KRYPTO (USD):" >> "$BRIEFING_FILE"
CRYPTO=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd&include_24hr_change=true" 2>/dev/null)
BTC=$(echo "$CRYPTO" | grep -o '"usd":[0-9.]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)
BTC_CHG=$(echo "$CRYPTO" | grep -o '"usd_24h_change":[^,}]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)
SOL=$(echo "$CRYPTO" | grep -o '"usd":[0-9.]*' | tail -1 | cut -d':' -f2)
SOL_CHG=$(echo "$CRYPTO" | grep -o '"usd_24h_change":[^,}]*' | tail -1 | cut -d':' -f2 | cut -d'.' -f1)

# Trend-Pfeile (sicherer Vergleich - nur erste Zahl nehmen)
BTC_CHG_CLEAN=$(echo "$BTC_CHG" | head -1 | tr -d '\n')
SOL_CHG_CLEAN=$(echo "$SOL_CHG" | head -1 | tr -d '\n')
[ -n "$BTC_CHG_CLEAN" ] && [ "$BTC_CHG_CLEAN" -gt 0 ] 2>/dev/null && BTC_ARROW="📈" || BTC_ARROW="📉"
[ -n "$SOL_CHG_CLEAN" ] && [ "$SOL_CHG_CLEAN" -gt 0 ] 2>/dev/null && SOL_ARROW="📈" || SOL_ARROW="📉"

echo "  $BTC_ARROW Bitcoin: \$$BTC (${BTC_CHG}%)" >> "$BRIEFING_FILE"
echo "  $SOL_ARROW Solana: \$$SOL (${SOL_CHG}%)" >> "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# 4. GESTERN (Memory-Analyse)
echo "🧠 GESTERN:" >> "$BRIEFING_FILE"
YESTERDAY=$(TZ="Europe/Berlin" date -d "yesterday" '+%Y-%m-%d')
YESTERDAY_FILE="$WORKSPACE/memory/$YESTERDAY.md"

if [ -f "$YESTERDAY_FILE" ]; then
    DONE=$(grep -c "\- \[x\]" "$YESTERDAY_FILE" 2>/dev/null || echo "0")
    OPEN=$(grep -c "\- \[ \]" "$YESTERDAY_FILE" 2>/dev/null || echo "0")
    echo "  ✅ $DONE Tasks erledigt" >> "$BRIEFING_FILE"
    [ "$OPEN" -gt 0 ] && echo "  ⏳ $OPEN Tasks offen" >> "$BRIEFING_FILE"
    grep -q "### 🧠 Reflexion" "$YESTERDAY_FILE" && echo "  📝 Tagesreflexion geschrieben" >> "$BRIEFING_FILE"
else
    echo "  Keine Daten vom Vortag" >> "$BRIEFING_FILE"
fi
echo "" >> "$BRIEFING_FILE"

# 4b. MEDIKAMENTE (tägliche Erinnerung)
echo "💊 MEDIKAMENTE:" >> "$BRIEFING_FILE"
echo "  • Cetirizin gegen Heuschnupfen" >> "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# 5. HEUTE
echo "📋 HEUTE:" >> "$BRIEFING_FILE"
TODAY_FILE="$WORKSPACE/memory/$TODAY.md"

if [ -f "$TODAY_FILE" ]; then
    # Termine extrahieren
    if grep -q "### 📅 Termine" "$TODAY_FILE"; then
        grep -E "^\*\*[0-9]{2}:[0-9]{2}\*\*|^- " "$TODAY_FILE" | head -4 | sed 's/^/  /' >> "$BRIEFING_FILE"
    else
        echo "  (Keine festen Termine eingetragen)" >> "$BRIEFING_FILE"
    fi
    
    # Fokus
    FOKUS=$(grep -A1 "### 🎯 Fokus" "$TODAY_FILE" 2>/dev/null | tail -1 | sed 's/^- //; s/^[[:space:]]*//')
    [ -n "$FOKUS" ] && echo "" >> "$BRIEFING_FILE" && echo "  🎯 Fokus: $FOKUS" >> "$BRIEFING_FILE"
else
    echo "  Keine Tagesplanung vorhanden" >> "$BRIEFING_FILE"
    echo "  💡 Erstelle: memory/$TODAY.md" >> "$BRIEFING_FILE"
fi

echo "" >> "$BRIEFING_FILE"
echo "⏰ Generiert: $(TZ='Europe/Berlin' date '+%H:%M Uhr')" >> "$BRIEFING_FILE"

echo "[$(TZ='Europe/Berlin' date)] Super-Briefing (komplett)" >> "$LOG_DIR/super.log"
