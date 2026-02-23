# 🚨 HEARTBEAT CHECKLIST

Kurze Checks für regelmäßige Heartbeats. Token-sparend halten!

## Tägliche Checks (rotieren)

- [ ] **Backup-Status** → `tail logs/backup.log` — letztes Backup OK?
- [ ] **Git-Status** → Uncommitted Änderungen? Push nötig?
- [ ] **Cron-Jobs** → `cron list` — alle laufen?
- [ ] **API-Keys** → Brave/Notion/Resend funktionieren?
- [ ] **Memory-Datei** → Heutige Datei existiert? Einträge aktuell?

## Wöchentliche Checks (Sonntags)

- [ ] **GitHub-Push** → Repo aktuell?
- [ ] **TELOS-Review** → GOALS.md — Ziele noch aktuell?
- [ ] **Memory-Wartung** → MEMORY.md aus Tagesdateien aktualisieren
- [ ] **PEOPLE.md** → "Letzter Kontakt" aktualisieren?

## Tracking

```json
// Speichere in memory/heartbeat-state.json:
{
  "lastChecks": {
    "backup": 1772016000,
    "git": 1772016000,
    "cron": 1772016000,
    "api": 1771929600,
    "memory": 1771929600
  },
  "lastUpdated": "2026-02-23T10:00:00Z"
}
```

**Zeit-Formate:**
- Unix-Timestamp (Sekunden seit 1970)
- ISO 8601 für `lastUpdated`

## Wann zu melden

**Sprech wenn:**
- Backup fehlgeschlagen
- Cron-Job mit Fehler (⚠️ Zeit-Problem beachten: UTC vs MEZ = 1h Unterschied!)
- API-Key ungültig
- Wichtige Deadline <2h
- >8h seit letzter Nachricht
- **Dringlichkeit:** Egal welche Uhrzeit — wenn es wichtig ist, melde dich!

**Schweige (HEARTBEAT_OK) wenn:**
- Mensch offensichtlich beschäftigt
- Erst vor <30min gecheckt
- Nichts Neues

## ERINNERUNG

Session-Speicher = NICHT EXISTENT → IMMER sofort in Dateien schreiben!
