# TOOLS.md - Aktive Tools & Konfiguration

_Lokale Notizen für mein Setup. Nur was wirklich genutzt wird._

---

## 🎙️ TTS (Text-to-Speech)

**Aktives System:** gTTS (Google Text-to-Speech)
- **Sprache:** Deutsch (natürlich)
- **Script:** `/root/workspace/scripts/tts_auto.sh`
- **Output:** OGG (Telegram-optimiert)

**Verwendung:**
```bash
bash /root/workspace/scripts/tts_auto.sh "Dein Text" /pfad/zur/datei.ogg
```

**Wann aktiv:** Auto-Modus ("Peter, ich bin jetzt im Auto")

---

## 🎤 Sprache-zu-Text

**System:** Whisper (OpenAI)
- **Lokal installiert** (kein API-Key nötig)
- **Sprachen:** Deutsch, Englisch
- **Nutzen:** Deine Sprachnachrichten transkribieren

---

## 🔍 Websuche

**System:** Brave Search API
- **API-Key:** In `~/.config/openclaw/.env.brave`
- **Verwendung:** Aktuelle Infos, News, Preise

---

## ⏰ Automation (Systemd-Timer)

| Timer | Zeit | Funktion |
|-------|------|----------|
| super-briefing | 07:00 MEZ | Morgen-Info mit allem |
| health-check | 06:00 MEZ | System-Überwachung |
| auto-backup | 22:00 MEZ | Git-Backup |
| notion-diary | 23:00 MEZ | Tagebuch-Eintrag |

**Status prüfen:**
```bash
systemctl list-timers
```

---

## 🤖 OpenClaw Cron-Jobs

**Konfiguration (aktuell):**
- `sessionTarget`: `isolated`
- `wakeMode`: `now`
- `model`: `kimi-coding/k2p5`
- `delivery`: `telegram` (zuverlässig)

**Alle Jobs:** Siehe `memory/cron-jobs-config.md`

---

## 🌤️ Wetter

**API:** Open-Meteo (kostenlos, kein Key)
- **Ort:** Friedrichroda (50.86, 10.57)
- **Nutzung:** Super-Briefing

---

## 💰 Krypto-Preise

**API:** CoinGecko (kostenlos)
- **Coins:** Bitcoin, Solana
- **Währung:** USD
- **Nutzung:** Super-Briefing

---

## 📝 Notion

**Tagebuch-Integration:**
- **Script:** `/root/workspace/scripts/diary_entry.sh`
- **API-Key:** `~/.config/openclaw/.env.notion`
- **Datenbank:** Tägliche Einträge

---

## 🔧 Wartung

**Logs prüfen:**
```bash
tail /root/workspace/logs/super_briefing_complete.txt
tail /root/workspace/logs/health_check.log
tail /root/workspace/logs/backup.log
```

**Git-Status:**
```bash
cd /root/workspace && git status
```

---

## 🌐 Community Ressourcen

**awesome-openclaw-skills:**
https://github.com/sundial-org/awesome-openclaw-skills

Curated Liste von Skills, Tools und Erweiterungen aus der Community.
Für spätere Ideen und Experimente — nicht aktiv genutzt, aber als Inspiration gespeichert.

---

*Diese Datei wird bei neuen Tools aktualisiert.*
