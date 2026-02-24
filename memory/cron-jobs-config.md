# Cron-Jobs Konfiguration

_Export aller aktiven Cron-Jobs — Stand: 2026-02-24 (v2 - agentTurn + Delivery)_

**Wichtige Einstellungen:**
- `sessionTarget`: `isolated` (eigene Session für zuverlässige Delivery)
- `wakeMode`: `now` (sofortige Ausführung)
- `payload.kind`: `agentTurn` (für Telegram-Delivery notwendig)
- `model`: `kimi-coding/k2p5` (explizit gesetzt)
- `delivery`: `telegram` (direkte Auslieferung an Chat)
- `tz`: `Europe/Berlin` (MEZ-Zeit)

---

## Template (Neuer Job)

```json
{
  "name": "Job-Name",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: Deine Nachricht..."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
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

### 0. Cron-Job Config-Guard
```json
{
  "name": "Cron-Job Config-Guard - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "0 6 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🛡️ Cron-Job Config-Guard - Tägliche Überprüfung:\n\nPrüfe alle Cron-Jobs auf korrekte Einstellungen:\n• sessionTarget: isolated ✓\n• wakeMode: now ✓\n• model: kimi-coding/k2p5 ✓\n• delivery: telegram ✓\n\nWenn Abweichungen gefunden → Warnung an Daniel"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 0.5. Overnight Thinking Mode
```json
{
  "name": "Overnight Thinking Mode - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "35 6 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🧠 Overnight Thinking Mode beendet\n\nIch habe über Nacht gearbeitet:\n• Memory-Dateien analysiert\n• Muster erkannt\n• Offene Punkte identifiziert\n• Erkenntnisse gewonnen\n\nBereit für den Tag! Was steht an?"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 1. Morgen-Briefing
```json
{
  "name": "Morgen-Briefing - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🌅 Guten Morgen! Das ist dein Tages-Setup:\n\n📋 WAS STEHT HEUTE AN?\n• Termine aus memory/YYYY-MM-DD.md\n• Wichtige To-Dos\n• Deadlines & Follow-ups\n\n🎯 FOKUS\n• Top-Priorität heute?\n• Creditreform: Neue Mitglieder, Follow-ups\n• Persönlich: Sport, Familie, Erledigungen\n\n🧠 MINDSET CHECK\n• Wie fühlst du dich? (Skala 1-10)\n• Gut ausgeschlafen?\n\n🌤️ WETTER + KLEIDUNG\n\nLass uns den Tag rocken! 💪"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 2. Evening-Briefing
```json
{
  "name": "Evening-Briefing - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "0 20 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🌙 Evening-Briefing - Zeit für den Tagesrückblick:\n\n📊 Wie war dein Tag?\n📅 Vorbereitung für morgen\n🧠 Cognitive Load\n⚠️ Warnung bei frühen Terminen"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 3. Täglicher Check-in
```json
{
  "name": "Täglicher Check-in - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "0 21 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🌙 Täglicher Check-in:\n\n• Risiken genommen heute?\n• Impulsive Entscheidungen?\n• Gefühle stabil?\n• Trading/Wallet-Themen?\n\nAntworte ehrlich. Kein Urteil."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 4. Notion Tagebuch Eintrag
```json
{
  "name": "Notion Tagebuch Eintrag - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "0 23 * * *",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 📝 NOTION_DIARY_TRIGGER\n\nErstelle Tagebucheintrag automatisch:\n- Script: /root/workspace/scripts/diary_entry.sh\n- Aktion: Eintrag mit Content aus memory/YYYY-MM-DD.md erstellen\n\nNach Ausführung: Kurze Bestätigung an Daniel senden."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

**Aktion beim Trigger:**
1. Script `diary_entry.sh` ausführen
2. Script liest `memory/YYYY-MM-DD.md`
3. Erstellt Notion-Eintrag mit Inhalt
4. Kurze Telegram-Bestätigung senden

### 5. Auto People Update
```json
{
  "name": "Auto People Update - MAIN",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "15 6 * * 6",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🔄 Auto People Update läuft!\n\nPEOPLE.md wird aus Memory-Dateien aktualisiert.\nNeue Personen werden hinzugefügt."
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 6. Weekly Social-Check
```json
{
  "name": "Weekly Social-Check",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 10 * * 0",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 👥 Weekly Social-Check - Zeit für deine Beziehungen:\n\n🔍 Überprüfung auf vernachlässigte Kontakte:\n- Wichtigkeit 10/10: Alle 3 Tage\n- Wichtigkeit 9/10: Alle 7 Tage\n- Wichtigkeit 8/10: Alle 10 Tage\n\n🎂 Kommende Geburtstage:\n- Prüfe PEOPLE.md\n\nSoll ich dir sagen, bei wem du dich melden solltest?"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 7. Pattern-Scanner
```json
{
  "name": "Pattern-Scanner",
  "enabled": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * 0",
    "tz": "Europe/Berlin"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: 🔍 Weekly Pattern-Scanner - Mustererkennung aus deinen Daten:\n\n📊 Analyse der letzten Woche aus MEMORY.md:\n- Häufige Stimmungen?\n- Regelmäßige Aktivitäten?\n- Termin-Muster?\n- Verbesserungspotenziale?\n\nSoll ich die Muster der letzten Woche analysieren?"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 8. Deadline Weimar Unterlagen
```json
{
  "name": "Deadline Weimar Unterlagen - MAIN",
  "enabled": true,
  "deleteAfterRun": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "at",
    "at": "2026-02-28T13:05:00.000Z"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: ⏰ DEADLINE!\n\nWeimar: Unterlagen nachreichen!\n• Unterschriebene Unterlagen per E-Mail senden\n\nNicht vergessen! 📧"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

### 9. Patrizia Setup
```json
{
  "name": "Patrizia Setup - MAIN",
  "enabled": true,
  "deleteAfterRun": true,
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "schedule": {
    "kind": "at",
    "at": "2026-02-28T07:05:00.000Z"
  },
  "model": "kimi-coding/k2p5",
  "payload": {
    "kind": "agentTurn",
    "message": "Output exactly: ⏰ Patrizia OpenClaw-Agent einrichten!\n\nSetup:\n• Hetzner CX21 (€5,35/Monat)\n• Getrennter Server\n• Eigenständiger Agent\n\nInfos sammeln: Name, Kanal, Persönliches"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "8309014037"
  }
}
```

---

## Zeit-Referenz

| UTC (Server) | MEZ (Deutschland) | Job |
|--------------|-------------------|-----|
| 05:00 | 06:00 | Cron-Job Config-Guard |
| 05:35 | 06:35 | Overnight Thinking Mode |
| 06:00 | 07:00 | Morgen-Briefing |
| 19:00 | 20:00 | Evening-Briefing |
| 20:00 | 21:00 | Täglicher Check-in |
| 22:00 | 23:00 | Notion Tagebuch (automatisch) |
| 05:15 | 06:15 | Auto People Update (Samstag) |
| 09:05 | 10:05 | Weekly Social-Check (Sonntag) |
| 19:05 | 20:05 | Pattern-Scanner (Sonntag) |

**Regel:** Einmalige Jobs (`kind: "at"`) müssen in UTC angegeben werden. Wiederkehrende Jobs (`kind: "cron"`) nutzen `tz: "Europe/Berlin"`.

---

## ✅ Alle Jobs Eingerichtet (11 total)

| # | Name | Zeit | Target | Delivery | Status |
|---|------|------|--------|----------|--------|
| 0 | 🛡️ Cron-Job Config-Guard | 06:00 täglich | isolated | telegram ✅ | ✅ Aktiv |
| 0.5 | 🧠 Overnight Thinking Mode | 06:35 täglich | isolated | telegram ✅ | ✅ Aktiv |
| 1 | 🌅 Morgen-Briefing | 07:00 täglich | isolated | telegram ✅ | ✅ Aktiv |
| 2 | 🌙 Evening-Briefing | 20:00 täglich | isolated | telegram ✅ | ✅ Aktiv |
| 3 | 🧠 Täglicher Check-in | 21:00 täglich | isolated | telegram ✅ | ✅ Aktiv |
| 4 | 📝 Notion Tagebuch | 23:00 täglich | isolated | telegram ✅ | ✅ Aktiv |
| 5 | 🔄 Auto People Update | Sa 06:15 | isolated | telegram ✅ | ✅ Aktiv |
| 6 | 👥 Weekly Social-Check | So 10:05 | isolated | telegram ✅ | ✅ Aktiv |
| 7 | 🔍 Pattern-Scanner | So 20:05 | isolated | telegram ✅ | ✅ Aktiv |
| 8 | ⏰ Patrizia Setup | Fr 28.02. 08:05 | isolated | telegram ✅ | ✅ Einmalig |
| 9 | ⏰ Deadline Weimar | Fr 28.02. 14:05 | isolated | telegram ✅ | ✅ Einmalig |

---

## Fehlerbehebung

### Frühere Fehler (jetzt behoben)
- ❌ `sessionTarget: main` + `systemEvent` → Keine garantierte Delivery
- ❌ `wakeMode: next-heartbeat` → Verspätete Ausführung
- ❌ Fehlende `model` Angabe → Anthropic-Key Fehler
- ✅ `sessionTarget: isolated` + `agentTurn` + `model` + `delivery` → Zuverlässig

### Häufiger Fehler behoben
```
FailoverError: No API key found for provider "anthropic"
```
**Ursache:** Kein explizites `model` in Cron-Job gesetzt.
**Lösung:** Immer `--model kimi-coding/k2p5` angeben.

---

## 🛡️ Sicherheitsmaßnahmen

### Manuelle Prüfung vor Änderungen
**Vor jedem neuen Job oder Update:**
1. In `memory/cron-jobs-config.md` das Template kopieren
2. Einstellungen gegen Checkliste prüfen:
   - [ ] `sessionTarget`: `isolated`
   - [ ] `wakeMode`: `now`
   - [ ] `model`: `kimi-coding/k2p5`
   - [ ] `payload.kind`: `agentTurn`
   - [ ] `delivery.channel`: `telegram`
   - [ ] `tz`: `Europe/Berlin` (bei wiederkehrenden Jobs)

### Backup
Diese Datei (`memory/cron-jobs-config.md`) ist die **Source of Truth**.
Bei Verlust der Jobs kann ich sie hieraus wiederherstellen.

**Letztes Update:** 2026-02-24 (v2 - agentTurn + Delivery)
