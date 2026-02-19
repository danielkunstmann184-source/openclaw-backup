# 🔒 PETER'S ZERO-FORGET PROTOCOL

**Ziel: Nie wieder etwas "vergessen"**

## Regel #1: Vor JEDER Antwort an Daniel

**MANDATORY FILE CHECK - Immer in dieser Reihenfolge:**

1. **Lies `USER.md`** → Wer ist Daniel?
2. **Lies `memory/01_people/daniel.md`** → Was ist sein aktueller Kontext?
3. **Lies `memory/YYYY-MM-DD.md`** (heute) → Was steht heute an?
4. **Lies `memory/03_projects/aktiv.md`** → Welche Projekte laufen?
5. **Lies `PEOPLE.md`** → Wer sind wichtige Kontakte?

**ERST DANN** darfst du antworten.

---

## Regel #2: Sofortiges Speichern (NO EXCEPTIONS)

| Wenn Daniel sagt... | Dann speichere SOFORT in... |
|---------------------|----------------------------|
| "Morgen habe ich..." | `memory/YYYY-MM-DD.md` (Folgetag) |
| "Heute war..." | `memory/YYYY-MM-DD.md` (heute) |
| "Ich muss noch..." | `memory/YYYY-MM-DD.md` → To-Do-Liste |
| "[Name] ist..." | `memory/01_people/[name].md` + `PEOPLE.md` |
| Wichtige Entscheidung | `MEMORY.md` |
| Projekt-Update | `memory/03_projects/aktiv.md` |

**Nach dem Speichern:** "✅ Gespeichert." sagen.

---

## Regel #3: Uncertainty Protocol

**Wenn du etwas nicht weißt:**
- ❌ NICHT raten
- ❌ NICHT "vielleicht" sagen
- ✅ Stattdessen: "Das steht nicht in meinen Dateien. Sag es mir, dann speichere ich es SOFORT."

---

## Regel #4: Session-Start Ritual

**Bei JEDEM Start:**
1. `HEARTBEAT.md` lesen
2. Falls Workspace leer → `scripts/restore_from_backup.sh` ausführen (siehe "Notfall-Wiederherstellung" unten)
3. Alle core .md Dateien laden (SOUL, USER, MEMORY)
4. Aktuelles Datum prüfen → `memory/YYYY-MM-DD.md` lesen

---

## 🚨 Notfall-Wiederherstellung (Post-Reinstall)

**Wurde OpenClaw neu installiert?**

WENN JA → Sofort ausführen:
```bash
/home/ubuntu/.openclaw/workspace/scripts/restore_from_backup.sh
```

### Danach prüfen:
- [ ] USER.md enthält Daniel's Daten
- [ ] memory/ Ordner vorhanden
- [ ] Alle .md Dateien vorhanden
- [ ] Cron-Jobs aktiv (`crontab -l`)

### Falls Restore fehlschlägt:
1. Token prüfen: Siehe `.github_token` im Workspace
2. Repo-URL: `https://github.com/danielkunstmann184-source/openclaw-backup`
3. Manuelles Clonen: `git clone <token>@github.com/...`

**WICHTIG:** GitHub Token befindet sich in `.github_token` — nicht in diesem Dokument speichern!

---

## Regel #5: Auto-Backup Validation

**Täglich um 23:30:**
- Backup läuft automatisch
- Log prüfen: `tail logs/backup.log`
- Falls fehlgeschlagen → SOFORT retry + Daniel informieren

---

## KEINE AUSREDEN.

**"Ich habe vergessen" = SYSTEM FEHLER**

Wenn ich etwas nicht weiß, liegt das daran, dass:
1. Es nicht in den Dateien steht, ODER
2. Ich die Dateien nicht gelesen habe

Beides ist INAKZEPTABEL.

---

**Das Einzige, was zählt:**
DATEIEN LESEN → DATEIEN SCHREIBEN → BACKUP PRÜFEN

**Nichts anderes.**
