#!/bin/bash
# PRE-RESPONSE CHECK SCRIPT - FIXED VERSION
# Run this before EVERY response to Daniel

WORKSPACE="/home/ubuntu/.openclaw/workspace"
TODAY=$(date '+%Y-%m-%d')
ERRORS=0

echo "=== PRE-RESPONSE CHECK ==="
echo "Date: $TODAY"
echo ""

# Check 1: Core files exist
echo "[1/6] Core files..."
[ -f "$WORKSPACE/USER.md" ] && echo "  ✅ USER.md" || { echo "  ❌ USER.md MISSING"; ERRORS=$((ERRORS+1)); }
[ -f "$WORKSPACE/SOUL.md" ] && echo "  ✅ SOUL.md" || { echo "  ❌ SOUL.md MISSING"; ERRORS=$((ERRORS+1)); }
[ -f "$WORKSPACE/MEMORY.md" ] && echo "  ✅ MEMORY.md" || { echo "  ❌ MEMORY.md MISSING"; ERRORS=$((ERRORS+1)); }
[ -f "$WORKSPACE/ZERO_FORGET_PROTOCOL.md" ] && echo "  ✅ ZERO_FORGET_PROTOCOL.md" || { echo "  ⚠️ ZERO_FORGET_PROTOCOL.md MISSING"; }
[ -f "$WORKSPACE/HEARTBEAT.md" ] && echo "  ✅ HEARTBEAT.md" || { echo "  ⚠️ HEARTBEAT.md MISSING"; }

# Check 2: Daniel's data
echo "[2/6] Daniel's profile..."
[ -f "$WORKSPACE/memory/01_people/daniel.md" ] && echo "  ✅ daniel.md" || { echo "  ❌ daniel.md MISSING"; ERRORS=$((ERRORS+1)); }

# Check 3: Today's file (auto-create if missing)
echo "[3/6] Today's memory..."
if [ -f "$WORKSPACE/memory/$TODAY.md" ]; then
    echo "  ✅ $TODAY.md"
else
    echo "  ⚠️ $TODAY.md not created yet - CREATING..."
    cat > "$WORKSPACE/memory/$TODAY.md" << EOF
# $TODAY — $(date '+%A' | sed 's/Monday/Montag/;s/Tuesday/Dienstag/;s/Wednesday/Mittwoch/;s/Thursday/Donnerstag/;s/Friday/Freitag/;s/Saturday/Samstag/;s/Sunday/Sonntag/')

## 🚗 Tagesablauf / Termine

## ✅ To-Dos

## 📝 Notizen

## 🔮 Für morgen

---
*Auto-created: $(date)*
EOF
    echo "  ✅ $TODAY.md CREATED"
fi

# Check 4: Active projects
echo "[4/6] Projects..."
[ -f "$WORKSPACE/memory/03_projects/aktiv.md" ] && echo "  ✅ aktiv.md" || { echo "  ⚠️ aktiv.md MISSING"; }

# Check 5: People
echo "[5/6] Relationships..."
[ -f "$WORKSPACE/PEOPLE.md" ] && echo "  ✅ PEOPLE.md" || { echo "  ⚠️ PEOPLE.md MISSING"; }

# Check 6: Backup-System
echo "[6/6] Backup-System..."
[ -f "$WORKSPACE/.github_token" ] && echo "  ✅ .github_token" || { echo "  ❌ .github_token MISSING"; ERRORS=$((ERRORS+1)); }
[ -f "$WORKSPACE/scripts/daily_backup.sh" ] && echo "  ✅ daily_backup.sh" || { echo "  ❌ daily_backup.sh MISSING"; ERRORS=$((ERRORS+1)); }
[ -x "$WORKSPACE/scripts/daily_backup.sh" ] && echo "  ✅ daily_backup.sh executable" || { echo "  ⚠️ daily_backup.sh not executable"; chmod +x "$WORKSPACE/scripts/daily_backup.sh"; echo "  ✅ Fixed"; }

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== ✅ READY TO RESPOND ==="
    exit 0
else
    echo "=== ⚠️ $ERRORS CRITICAL ISSUES FOUND ==="
    exit 1
fi
