# Cron-Jobs Konfiguration

_Export aller aktiven Cron-Jobs — Stand: 2026-02-24_

**Wichtige Einstellungen:**
- `sessionTarget`: `main` (immer)
- `wakeMode`: `now` (sofortige Ausführung)
- `payload.kind`: `systemEvent` (kein API-Key nötig)
- `tz`: `Europe/Berlin` (MEZ-Zeit)

---

## Template (Neuer Job)

```json
{
  "name": "Job-Name",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Deine Nachricht..."
  }
}
```

**Einmaliger Job mit Löschung:**
```json
{
  "deleteAfterRun": true,
  ...
}
```

---

## Aktive Jobs

### 1. Morgen-Briefing
```json
{
  "name": "Morgen-Briefing - MAIN",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 7 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "🌅 Guten Morgen! Das ist dein tägliches Briefing:\n\nLies memory/YYYY-MM-DD.md für heute und MEMORY.md für Kontext.\n\nDann gib ein kurzes Briefing:\n🧠 Sentiment-Check\n📅 Wichtige Termine\n👥 Social-Checks\n💪 Health-Check\n🌤️ Wetter + Kleidung"
  }
}
```

### 2. Evening-Briefing
```json
{
  "name": "Evening-Briefing - MAIN",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "🌙 Evening-Briefing - Zeit für den Tagesrückblick:\n\n📊 Wie war dein Tag?\n📅 Vorbereitung für morgen\n🧠 Cognitive Load\n⚠️ Warnung bei frühen Terminen"
  }
}
```

### 3. Täglicher Check-in
```json
{
  "name": "Täglicher Check-in - MAIN",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 21 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "🌙 Täglicher Check-in:\n\n• Risiken genommen heute?\n• Impulsive Entscheidungen?\n• Gefühle stabil?\n• Trading/Wallet-Themen?\n\nAntworte ehrlich. Kein Urteil."
  }
}
```

### 4. Notion Tagebuch Eintrag
```json
{
  "name": "Notion Tagebuch Eintrag - MAIN",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 23 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "📝 Neuer Tagebucheintrag in Notion erstellt!\n\nTitel: YYYYMMDD_Tagesreflexion\nStruktur: Morgens → Arbeit → Abend → Dankbarkeit → Ausblick\n\nÖffne Notion und ergänze Details."
  }
}
```

### 5. Daily Summary
```json
{
  "name": "Daily Summary - MAIN",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "35 23 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "📊 Daily Summary erstellt!\n\nTageszusammenfassung wurde in memory/YYYY-MM-DD.md gespeichert.\nAlle wichtigen Ereignisse, Termine und Entscheidungen persistiert."
  }
}
```

### 6. Täglicher Tagebucheintrag
```json
{
  "name": "Täglicher Tagebucheintrag",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "45 23 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "📝 Neuer Tagebucheintrag erstellt!\n\nIch habe soeben einen neuen Eintrag in dein Notion-Tagebuch geschrieben:\n• Titel: YYYYMMDD_Tagesreflexion\n• Struktur: Morgens → Arbeit → Abend → Dankbarkeit → Ausblick\n\nDer Eintrag wartet auf deine Details. Öffne Notion und ergänze, was heute wichtig war.\n\nSchlaf gut, Daniel. 🌙"
  }
}
```

### 7. Auto People Update
```json
{
  "name": "Auto People Update - MAIN",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "15 6 * * 6",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "🔄 Auto People Update läuft!\n\nPEOPLE.md wird aus Memory-Dateien aktualisiert.\nNeue Personen werden hinzugefügt."
  }
}
```

### 8. Weekly Social-Check
```json
{
  "name": "Weekly Social-Check",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 10 * * 0",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "👥 Weekly Social-Check - Zeit für deine Beziehungen:\n\n🔍 Überprüfung auf vernachlässigte Kontakte:\n- Wichtigkeit 10/10: Alle 3 Tage\n- Wichtigkeit 9/10: Alle 7 Tage\n- Wichtigkeit 8/10: Alle 10 Tage\n\n🎂 Kommende Geburtstage:\n- Prüfe PEOPLE.md\n\nSoll ich dir sagen, bei wem du dich melden solltest?"
  }
}
```

### 9. Pattern-Scanner
```json
{
  "name": "Pattern-Scanner",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * 0",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "🔍 Weekly Pattern-Scanner - Mustererkennung aus deinen Daten:\n\n📊 Analyse der letzten Woche aus MEMORY.md:\n- Häufige Stimmungen?\n- Regelmäßige Aktivitäten?\n- Termin-Muster?\n- Verbesserungspotenziale?\n\nSoll ich die Muster der letzten Woche analysieren?"
  }
}
```

### 10. Deadline Weimar Unterlagen
```json
{
  "name": "Deadline Weimar Unterlagen - MAIN",
  "enabled": true,
  "deleteAfterRun": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "at",
    "at": "2026-02-28T13:05:00.000Z"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ DEADLINE!\n\nWeimar: Unterlagen nachreichen!\n• Unterschriebene Unterlagen per E-Mail senden\n\nNicht vergessen! 📧"
  }
}
```

### 11. Patrizia Setup
```json
{
  "name": "Patrizia Setup - MAIN",
  "enabled": true,
  "deleteAfterRun": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "at",
    "at": "2026-02-28T07:05:00.000Z"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ Patrizia OpenClaw-Agent einrichten!\n\nSetup:\n• Hetzner CX21 (€5,35/Monat)\n• Getrennter Server\n• Eigenständiger Agent\n\nInfos sammeln: Name, Kanal, Persönliches"
  }
}
```

---

## Zeit-Referenz

| UTC (Server) | MEZ (Deutschland) | Hinweis |
|--------------|-------------------|---------|
| 06:00 | 07:00 | Morgen-Briefing (07:05) |
| 19:00 | 20:00 | Evening-Briefing (20:05) |
| 20:00 | 21:00 | Täglicher Check-in (21:05) |
| 22:00 | 23:00 | Notion/Daily/Tagebucheintrag |

**Regel:** Einmalige Jobs (`kind: "at"`) müssen in UTC angegeben werden. Wiederkehrende Jobs (`kind: "cron"`) nutzen `tz: "Europe/Berlin"`.

---

## Fehlerbehebung

### Frühere Fehler (jetzt behoben)
- ❌ `wakeMode: next-heartbeat` → ✅ `wakeMode: now`
- ❌ `payload.kind: agentTurn` → ✅ `payload.kind: systemEvent`
- ❌ `sessionTarget: isolated` → ✅ `sessionTarget: main`

### Häufiger Fehler
```
FailoverError: No API key found for provider "anthropic"
```
**Ursache:** `agentTurn` statt `systemEvent` verwendet.  
**Lösung:** Immer `systemEvent` für Erinnerungen nutzen.
