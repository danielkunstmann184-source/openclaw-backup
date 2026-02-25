# HEARTBEAT.md - Automatische Checks

_Proaktive System-Überwachung ohne Spam._

---

## 🔄 Health-Check läuft automatisch

**Systemd-Timer:** `health-check.timer` (täglich 06:00)
- Prüft alle systemd-Timer
- Prüft Git-Status
- Prüft API-Keys
- Auto-Reparatur wo möglich

**Manuell prüfen:**
```bash
systemctl list-timers
tail /root/workspace/logs/health_check.log
```

---

## ✅ Wöchentliche Review (Sonntags)

- **TELOS-Check:** Ziele in GOALS.md noch aktuell?
- **Memory-Wartung:** Wichtiges aus Tagesdateien in MEMORY.md übertragen
- **PEOPLE.md:** "Letzter Kontakt" aktualisieren

---

## 📊 Tracking

Status in: `memory/heartbeat-state.json`

---

## 💬 Wann melde ich mich?

**Sprech wenn:**
- Backup fehlgeschlagen
- System-Check zeigt kritischen Fehler
- Wichtige Deadline <2h
- >8h seit letzter Nachricht

**Schweige (HEARTBEAT_OK) wenn:**
- Alles läuft normal
- Du bist offensichtlich beschäftigt
- Erst vor <30min gecheckt

---

*Nichts vergessen: Session-Speicher = Nicht existent. Wichtiges immer sofort speichern.*
