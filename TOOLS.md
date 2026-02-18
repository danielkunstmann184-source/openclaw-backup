# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---


## TTS (Text-to-Speech)

- **System:** Sherpa ONNX (lokal, offline)
- **Deutsches Modell:** Thorsten (de_DE)
- **Pfad:** `~/.openclaw/tools/sherpa-onnx-tts/`
- **Format:** Ogg/Opus (Telegram-kompatibel)

## Auto-Modus

- **Aktivierung:** "Peter, ich bin jetzt im Auto"
- **Deaktivierung:** "Peter, Autofahrt beendet"
- **Effekt:** Kurze Antworten + automatische Sprachausgabe
- **Konfiguration:** `memory/04_preferences/auto_mode.md`

## 🔔 Cron-Jobs - Best Practices

Für **zuverlässige** Erinnerungen:

| Einstellung | Wert | Warum |
|-------------|------|-------|
| `sessionTarget` | `isolated` | Funktioniert auch ohne aktive Main-Session |
| `wakeMode` | `now` | Sofortige Ausführung, kein Warten auf Heartbeat |
| `delivery.mode` | `announce` | Sichtbare Notification |
| `delivery.channel` | `telegram` | Direkte Zustellung |
| `payload.kind` | `agentTurn` | Volle Agent-Funktionalität |

**Beispiel-Struktur:**
```json
{
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "delivery": {
    "mode": "announce",
    "channel": "telegram"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Erinnerungstext...",
    "model": "kimi-coding/k2p5"
  }
}
```

## 🚀 Sofort-Speichern

Nutze: `./scripts/save_day.sh` oder sage "Speichern"

Persistiert sofort:
- `memory/YYYY-MM-DD.md` (Tagesdatei)
- Git-Commit
- GitHub-Push
