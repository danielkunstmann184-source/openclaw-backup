#!/bin/bash
# SUPER-BRIEFING - Alles in einem (Level 2 Optimized)
# Täglich um 07:00 MEZ - Kombiniert Health, Analysis, Orakel, Wetter

set -e

WORKSPACE="/root/workspace"
LOG_DIR="$WORKSPACE/logs"
BRIEFING_FILE="$LOG_DIR/super_briefing.txt"
ALERT_FILE="$LOG_DIR/super_alert.txt"

# Brave API Key
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

# Briefing starten
echo "🌅 SUPER-BRIEFING - $WEEKDAY_GER, $TODAY_GERMAN" > "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# ============================================
# 1. SYSTEM-CHECK (nur bei Problemen anzeigen)
# ============================================
ERRORS=""

# Prüfe systemd-Timer
for timer in notion-diary; do
    if ! systemctl is-active --quiet $timer.timer 2>/dev/null; then
        ERRORS="${ERRORS}⚠️ $timer.timer inaktiv\n"
    fi
done

# Prüfe Git-Status
cd "$WORKSPACE"
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    ERRORS="${ERRORS}⚠️ $(git status --short | wc -l) uncommitted Änderungen\n"
fi

# Nur bei Fehlern anzeigen
if [ -n "$ERRORS" ]; then
    echo "🩺 SYSTEM:" >> "$BRIEFING_FILE"
    echo -e "$ERRORS" >> "$BRIEFING_FILE"
    echo "" >> "$BRIEFING_FILE"
fi

# ============================================
# 2. WETTER
# ============================================
echo "🌤️ WETTER:" >> "$BRIEFING_FILE"
WEATHER_JSON=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=50.86&longitude=10.57&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=Europe/Berlin&forecast_days=1" 2>/dev/null || echo '{}')

MAX_TEMP=$(echo "$WEATHER_JSON" | grep -o '"temperature_2m_max":\[[^]]*\]' | grep -o '[0-9.]*' | head -1 || echo "??")
MIN_TEMP=$(echo "$WEATHER_JSON" | grep -o '"temperature_2m_min":\[[^]]*\]' | grep -o '[0-9.]*' | head -1 || echo "??")
WEATHER_CODE=$(echo "$WEATHER_JSON" | grep -o '"weathercode":\[[^]]*\]' | grep -o '[0-9]*' | head -1 || echo "0")
PRECIP=$(echo "$WEATHER_JSON" | grep -o '"precipitation_sum":\[[^]]*\]' | grep -o '[0-9.]*' | head -1 || echo "0")

case "$WEATHER_CODE" in
    0) CONDITION="☀️ Klar" ;;
    1|2|3) CONDITION="⛅ Bewölkt" ;;
    45|48) CONDITION="🌫️ Nebel" ;;
    51|53|55|61|63|65) CONDITION="🌧️ Regen" ;;
    71|73|75) CONDITION="🌨️ Schnee" ;;
    95|96|99) CONDITION="⛈️ Gewitter" ;;
    *) CONDITION="☁️ Wechselhaft" ;;
esac

echo "  $CONDITION | $MIN_TEMP°C bis $MAX_TEMP°C" >> "$BRIEFING_FILE"
[ "$PRECIP" != "0" ] && [ "$PRECIP" != "0.0" ] && echo "  🌧️ Niederschlag: ${PRECIP}mm" >> "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# ============================================
# 3. KRYPTO (USD)
# ============================================
echo "💰 KRYPTO:" >> "$BRIEFING_FILE"
CRYPTO=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd&include_24hr_change=true" 2>/dev/null || echo '{}')
BTC=$(echo "$CRYPTO" | grep -o '"usd":[0-9.]*' | head -1 | cut -d':' -f2)
BTC_CHG=$(echo "$CRYPTO" | grep -o '"usd_24h_change":[-0-9.]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)
SOL=$(echo "$CRYPTO" | grep -o '"usd":[0-9.]*' | tail -1 | cut -d':' -f2)
SOL_CHG=$(echo "$CRYPTO" | grep -o '"usd_24h_change":[-0-9.]*' | tail -1 | cut -d':' -f2 | cut -d'.' -f1)

[ -n "$BTC" ] && echo "  BTC: \$$BTC (${BTC_CHG}%)" >> "$BRIEFING_FILE"
[ -n "$SOL" ] && echo "  SOL: \$$SOL (${SOL_CHG}%)" >> "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# ============================================
# 4. BÖRSEN (schnell)
# ============================================
echo "📈 BÖRSEN:" >> "$BRIEFING_FILE"
DAX=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/^GDAXI?interval=1d&range=1d" 2>/dev/null | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)
DOW=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/^DJI?interval=1d&range=1d" 2>/dev/null | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)
GOLD=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d" 2>/dev/null | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)

[ -n "$DAX" ] && echo "  DAX: $DAX" >> "$BRIEFING_FILE"
[ -n "$DOW" ] && echo "  Dow: $DOW" >> "$BRIEFING_FILE"
[ -n "$GOLD" ] && echo "  Gold: $GOLD" >> "$BRIEFING_FILE"
echo "" >> "$BRIEFING_FILE"

# ============================================
# 5. THÜRINGEN NEWS (nur Headlines)
# ============================================
echo "📰 THÜRINGEN:" >> "$BRIEFING_FILE"
if [ -n "$BRAVE_API_KEY" ]; then
    NEWS=$(curl -s "https://api.search.brave.com/res/v1/news/search?q=Thüringen+news&count=3" \
        -H "Accept: application/json" \
        -H "X-Subscription-Token: $BRAVE_API_KEY" 2>/dev/null | grep -o '"title":"[^"]*"' | head -3)
    [ -n "$NEWS" ] && echo "$NEWS" | sed 's/"title":"/  • /g; s/"//g' >> "$BRIEFING_FILE" || echo "  (News werden geladen...)" >> "$BRIEFING_FILE"
else
    echo "  (API Key nicht verfügbar)" >> "$BRIEFING_FILE"
fi
echo "" >> "$BRIEFING_FILE"

# ============================================
# 6. MEMORY ANALYSIS (schnell)
# ============================================
echo "🧠 GESTERN:" >> "$BRIEFING_FILE"
YESTERDAY=$(TZ="Europe/Berlin" date -d "yesterday" '+%Y-%m-%d')
YESTERDAY_FILE="$WORKSPACE/memory/$YESTERDAY.md"

if [ -f "$YESTERDAY_FILE" ]; then
    # Zähle erledigte Tasks
    DONE=$(grep -c "\- \[x\]" "$YESTERDAY_FILE" 2>/dev/null || echo "0")
    OPEN=$(grep -c "\- \[ \]" "$YESTERDAY_FILE" 2>/dev/null || echo "0")
    [ "$DONE" -gt 0 ] && echo "  ✅ $DONE erledigt" >> "$BRIEFING_FILE"
    [ "$OPEN" -gt 0 ] && echo "  ⏳ $OPEN offen" >> "$BRIEFING_FILE"
    grep -q "### 🧠 Reflexion" "$YESTERDAY_FILE" && echo "  📝 Reflexion vorhanden" >> "$BRIEFING_FILE"
else
    echo "  Keine Daten" >> "$BRIEFING_FILE"
fi
echo "" >> "$BRIEFING_FILE"

# ============================================
# 7. HEUTE (Tages-Setup)
# ============================================
echo "📋 HEUTE:" >> "$BRIEFING_FILE"
TODAY_FILE="$WORKSPACE/memory/$TODAY.md"

if [ -f "$TODAY_FILE" ]; then
    # Extrahiere Termine
    if grep -q "### 📅 Termine" "$TODAY_FILE"; then
        grep -E "^\*\*\d{2}:\d{2}\*\*" "$TODAY_FILE" | head -3 | sed 's/^/  /' >> "$BRIEFING_FILE"
    else
        echo "  (Termine im Tagesplan)" >> "$BRIEFING_FILE"
    fi
    
    # Fokus
    FOKUS=$(grep -A1 "### 🎯 Fokus" "$TODAY_FILE" | tail -1 | sed 's/^- //')
    [ -n "$FOKUS" ] && echo "  🎯 Fokus: $FOKUS" >> "$BRIEFING_FILE"
else
    echo "  Keine Tagesdatei vorhanden" >> "$BRIEFING_FILE"
fi

echo "" >> "$BRIEFING_FILE"
echo "⏰ Generiert: $(TZ='Europe/Berlin' date '+%H:%M')" >> "$BRIEFING_FILE"

# Log
mkdir -p "$LOG_DIR"
echo "[$(TZ='Europe/Berlin' date)] Super-Briefing erstellt" >> "$LOG_DIR/super.log"
