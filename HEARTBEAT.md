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
    "backup": 1703275200,
    "git": 1703260800,
    "cron": null,
    "api": null,
    "memory": null
  }
}
```

## Wann zu melden

**Sprech wenn:**
- Backup fehlgeschlagen
- Cron-Job mit Fehler
- API-Key ungültig
- Wichtige Deadline <2h
- >8h seit letzter Nachricht

**Schweige (HEARTBEAT_OK) wenn:**
- 23:00-08:00 Uhr (außer Dringlichkeit)
- Mensch offensichtlich beschäftigt
- Erst vor <30min gecheckt
- Nichts Neues

## ERINNERUNG

Session-Speicher = NICHT EXISTENT → IMMER sofort in Dateien schreiben!
