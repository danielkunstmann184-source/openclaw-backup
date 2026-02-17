#!/bin/bash
# PRE-RESPONSE CHECK SCRIPT
# Run this before EVERY response to Daniel

WORKSPACE="/home/ubuntu/.openclaw/workspace"
TODAY=$(date '+%Y-%m-%d')

echo "=== PRE-RESPONSE CHECK ==="
echo "Date: $TODAY"
echo ""

# Check 1: Core files exist
echo "[1/5] Core files..."
[ -f "$WORKSPACE/USER.md" ] && echo "  ✅ USER.md" || echo "  ❌ USER.md MISSING"
[ -f "$WORKSPACE/SOUL.md" ] && echo "  ✅ SOUL.md" || echo "  ❌ SOUL.md MISSING"
[ -f "$WORKSPACE/MEMORY.md" ] && echo "  ✅ MEMORY.md" || echo "  ❌ MEMORY.md MISSING"

# Check 2: Daniel's data
echo "[2/5] Daniel's profile..."
[ -f "$WORKSPACE/memory/01_people/daniel.md" ] && echo "  ✅ daniel.md" || echo "  ❌ daniel.md MISSING"

# Check 3: Today's file
echo "[3/5] Today's memory..."
[ -f "$WORKSPACE/memory/$TODAY.md" ] && echo "  ✅ $TODAY.md" || echo "  ⚠️  $TODAY.md not created yet"

# Check 4: Active projects
echo "[4/5] Projects..."
[ -f "$WORKSPACE/memory/03_projects/aktiv.md" ] && echo "  ✅ aktiv.md" || echo "  ❌ aktiv.md MISSING"

# Check 5: People
echo "[5/5] Relationships..."
[ -f "$WORKSPACE/PEOPLE.md" ] && echo "  ✅ PEOPLE.md" || echo "  ❌ PEOPLE.md MISSING"

echo ""
echo "=== READY TO RESPOND ==="
