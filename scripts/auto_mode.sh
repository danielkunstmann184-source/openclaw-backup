#!/bin/bash
# Auto-Modus Status-Verwaltung

STATUS_FILE="/root/workspace/.auto_mode"

if [ "$1" = "on" ]; then
    echo "active" > "$STATUS_FILE"
    echo "✅ Auto-Modus AKTIVIERT"
elif [ "$1" = "off" ]; then
    echo "inactive" > "$STATUS_FILE"
    echo "✅ Auto-Modus DEAKTIVIERT"
elif [ "$1" = "status" ]; then
    if [ -f "$STATUS_FILE" ] && [ "$(cat "$STATUS_FILE")" = "active" ]; then
        echo "active"
    else
        echo "inactive"
    fi
else
    echo "Usage: $0 [on|off|status]"
fi
