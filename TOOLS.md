# TOOLS.md - Lokale Notizen

Skills definieren _wie_ Tools funktionieren. Diese Datei ist für _deine_ Details — die Sachen, die einzigartig für dein Setup sind.

---

## TTS (Text-to-Speech)

### Standard (Auto-Modus)
- **System:** Piper TTS (natürlichere Stimme)
- **Deutsches Modell:** Thorsten Medium (de_DE)
- **Pfad:** `~/.openclaw/tools/tts-piper/`
- **Wrapper:** `~/.openclaw/tools/tts-piper/tts.sh`
- **Format:** WAV (wird zu OGG/Opus konvertiert)

### Fallback
- **System:** Sherpa ONNX (Backup)
- **Pfad:** `~/.openclaw/tools/sherpa-onnx-tts/`

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
    "expr": "0 20 * * *",
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

**Referenz:** 2026-02-22 – Alle Cron-Jobs auf `systemEvent` umgestellt, Testläufe erfolgreich.

---

**Ergänze hier deine eigenen Notizen:** SSH-Hosts, Kameranamen, etc.
