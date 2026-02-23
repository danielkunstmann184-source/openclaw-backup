# TOOLS.md - Lokale Notizen

Skills definieren _wie_ Tools funktionieren. Diese Datei ist für _deine_ Details — die Sachen, die einzigartig für dein Setup sind.

---

## TTS (Text-to-Speech)

### Standard (Sprachnachrichten)
- **System:** ElevenLabs API (natürlichste Stimme)
- **Voice ID:** `xH6rAlU6xUCcDlplBaJQ`
- **API-Key:** In `.env.api` hinterlegt
- **Workflow:** ElevenLabs zuerst → Fallback bei Limit

### Fallback 1 (Lokal)
- **System:** Piper TTS (offline, kostenlos)
- **Deutsches Modell:** Thorsten Medium (de_DE)
- **Pfad:** `~/.openclaw/tools/tts-piper/`
- **Wrapper:** `~/.openclaw/tools/tts-piper/tts.sh`

### Fallback 2 (Notfall)
- **System:** Sherpa ONNX
- **Pfad:** `~/.openclaw/tools/sherpa-onnx-tts/`

### Reihenfolge bei Sprachausgabe
1. **ElevenLabs** (API) — Primär, beste Qualität
2. **Piper TTS** (lokal) — bei ElevenLabs-Limit
3. **Sherpa ONNX** (lokal) — Notfall-Option

### Nutzung im Auto-Modus
```bash
# Wrapper verwenden (empfohlen)
~/.openclaw/tools/tts-piper/tts.sh "Dein Text" /tmp/output.wav

# Dann zu Telegram-Format konvertieren
ffmpeg -i /tmp/output.wav -c:a libopus -b:a 24k /tmp/output.ogg
```

## Auto-Modus

- **Aktivierung:** "Peter, ich bin jetzt im Auto"
- **Deaktivierung:** "Peter, Autofahrt beendet"
- **Effekt:** Kurze Antworten + automatische Sprachausgabe (Piper TTS)

## Cron-Jobs

Siehe **AGENTS.md** → "⏰ Cron-Job Best Practices"

### 🔧 Funktionierende Konfiguration (Memo für mich)

**Wichtig:** `payload.kind` muss `"systemEvent"` sein!

```json
{
  "name": "Job-Name",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "next-heartbeat",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",  // ← DAS IST DER KEY!
    "text": "Deine Nachricht..."
  }
}
```

**Warum?**
- `"systemEvent"` = Text wird injiziert, kein API-Key nötig ✅
- `"agentTurn"` = Startet neuen Agenten, braucht API-Key ❌

**Fehler bei "agentTurn":** `FailoverError: No API key found for provider "anthropic"`

**Lösung:** Immer `systemEvent` verwenden für Erinnerungen/Briefings.

**Einmalige Jobs mit Löschung:**
```json
"deleteAfterRun": true
```

**Zeit-Regel:**
- `tz: Europe/Berlin` für wiederkehrende Jobs (Cron)
- UTC-Minus-1h für einmalige Jobs (z.B. 16:15 MEZ = 15:15 UTC)

**Referenz:** 2026-02-23 – Alle 12 Cron-Jobs auf `systemEvent` + MEZ-Zeit umgestellt

---

**Ergänze hier deine eigenen Notizen:** SSH-Hosts, Kameranamen, etc.
