#!/bin/bash
# Orakel-Briefing Script - Level 2 Superkraft
# Täglich um 06:45 MEZ - Marktdata + News + Web-Suche

WORKSPACE="/root/workspace"
LOG_DIR="$WORKSPACE/logs"
OUTPUT_FILE="$LOG_DIR/oracle_briefing.txt"

# Brave API Key laden
export BRAVE_API_KEY=$(cat ~/.config/openclaw/.env.brave 2>/dev/null | grep "BRAVE_API_KEY=" | cut -d'=' -f2)

log() {
    echo "[$(TZ='Europe/Berlin' date '+%H:%M:%S')] $1"
}

echo "🔮 ORAKEL-BRIEFING - $(TZ='Europe/Berlin' date '+%d.%m.%Y')" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 1. KRYPTO (CoinGecko API - kostenlos)
echo "💰 KRYPTO-MÄRKTE:" >> "$OUTPUT_FILE"
CRYPTO_DATA=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=eur&include_24hr_change=true" 2>/dev/null || echo '{}')

BTC_PRICE=$(echo "$CRYPTO_DATA" | grep -o '"eur":[0-9.]*' | head -1 | cut -d':' -f2)
BTC_CHANGE=$(echo "$CRYPTO_DATA" | grep -o '"eur_24h_change":[-0-9.]*' | head -1 | cut -d':' -f2 | cut -d'.' -f1)
SOL_PRICE=$(echo "$CRYPTO_DATA" | grep -o '"eur":[0-9.]*' | tail -1 | cut -d':' -f2)
SOL_CHANGE=$(echo "$CRYPTO_DATA" | grep -o '"eur_24h_change":[-0-9.]*' | tail -1 | cut -d':' -f2 | cut -d'.' -f1)

[ -n "$BTC_PRICE" ] && echo "  • Bitcoin: €$BTC_PRICE (${BTC_CHANGE}%)" >> "$OUTPUT_FILE"
[ -n "$SOL_PRICE" ] && echo "  • Solana: €$SOL_PRICE (${SOL_CHANGE}% )" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 2. BÖRSEN (Yahoo Finance via curl)
echo "📈 BÖRSEN:" >> "$OUTPUT_FILE"

# DAX
DAX=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/^GDAXI?interval=1d&range=1d" 2>/dev/null | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d':' -f2)
[ -n "$DAX" ] && echo "  • DAX: $DAX" >> "$OUTPUT_FILE"

# Dow Jones
DOW=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/^DJI?interval=1d&range=1d" 2>/dev/null | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d':' -f2)
[ -n "$DOW" ] && echo "  • Dow Jones: $DOW" >> "$OUTPUT_FILE"

# Gold
GOLD=$(curl -s "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d" 2>/dev/null | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d':' -f2)
[ -n "$GOLD" ] && echo "  • Gold: $GOLD USD" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# 3. THÜRINGEN NEWS (via Brave Search)
echo "📰 THÜRINGEN LOKAL:" >> "$OUTPUT_FILE"
if [ -n "$BRAVE_API_KEY" ]; then
    # Brave News API
    NEWS=$(curl -s "https://api.search.brave.com/res/v1/news/search?q=Thüringen+Gotha+Erfurt+news&count=5" \
        -H "Accept: application/json" \
        -H "X-Subscription-Token: $BRAVE_API_KEY" 2>/dev/null | grep -o '"title":"[^"]*"' | head -5)
    
    if [ -n "$NEWS" ]; then
        echo "$NEWS" | sed 's/"title":"/  • /g; s/"//g' >> "$OUTPUT_FILE"
    else
        echo "  (News werden geladen...)" >> "$OUTPUT_FILE"
    fi
else
    echo "  ⚠️ Brave API Key nicht verfügbar" >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"
echo "⏰ Generiert: $(TZ='Europe/Berlin' date '+%H:%M')" >> "$OUTPUT_FILE"

log "Orakel-Briefing erstellt"
