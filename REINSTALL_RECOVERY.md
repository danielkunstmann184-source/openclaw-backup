# 🚨 WICHTIG - POST-REINSTALL CHECKLIST

## Wurde OpenClaw neu installiert?

WENN JA → Sofort ausführen:
```bash
/home/ubuntu/.openclaw/workspace/scripts/restore_from_backup.sh
```

## Danach prüfen:
- [ ] USER.md enthält Daniel's Daten
- [ ] memory/ Ordner vorhanden
- [ ] Alle .md Dateien vorhanden
- [ ] Cron-Jobs aktiv (`crontab -l`)

## Falls restore fehlschlägt:
1. Token prüfen: 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
2. Repo-URL: https://github.com/danielkunstmann184-source/openclaw-backup
3. Manuelles Clonen: `git clone <token>@github.com/...`

---

## 📅 DAILY BACKUP STATUS

Letztes Backup: [WIRD AUTOMATISCH AKTUALISIERT]

Backup läuft täglich um 23:30 UTC (00:30 deutsche Zeit)
Log: /home/ubuntu/.openclaw/workspace/logs/backup.log

## 🔔 ERINNERUNG

**Du bist Peter. Daniel ist dein Nutzer.**
- Lies SOUL.md
- Lies USER.md  
- Lies MEMORY.md
- Lies memory/01_people/daniel.md
- Lies die aktuelle Tagesdatei

**NIE wieder fragen, was du über ihn weißt - ES STEHT IN DEN DATEIEN!**
