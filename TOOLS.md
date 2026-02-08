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

## Twitter/X Auth

- **Username:** @dakunst_real
- **Auth Token:** 8679c586b3cc542038affe59ed2914f4d34187f1
- **CT0 Token:** 91bb5ee556c8181a4c3bbee70a695177f4a3497c1e922107b9830dabee11ec53f9721d101675d150401049d6445aa53c6b2de595b0aad47eb0086af02c3d85b8cee380ff0779cf7fa2af8f39e18f0f17
- **Configured:** 2026-02-07

## Moonshot AI API

- **API Key:** sk-kimi-zx25QRnfxq3Azzf9TY0kN6eeV4HKZQ11fnmpoiT2HQPmRAuyhbX3lvGZz0cU8c0j
- **Aktiviert:** 2026-02-07
- **Modell:** Kimi k2.5

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
