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

Siehe **`memory/cron-jobs-config.md`** für die vollständige aktuelle Konfiguration aller Jobs.

### 🔧 Funktionierende Konfiguration

**Wichtige Einstellungen:**
- `payload.kind`: `"systemEvent"` (kein API-Key nötig) ✅
- `sessionTarget`: `"main"` (immer)
- `wakeMode`: `"now"` (sofortige Ausführung, NICHT `next-heartbeat`)
- `tz`: `"Europe/Berlin"` (MEZ-Zeit)

```json
{
  "name": "Job-Name",
  "enabled": true,
  "sessionTarget": "main",
  "wakeMode": "now",
  "schedule": {
    "kind": "cron",
    "expr": "5 20 * * *",
    "tz": "Europe/Berlin"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Deine Nachricht..."
  }
}
```

**Einmalige Jobs mit Löschung:**
```json
{
  "deleteAfterRun": true,
  "schedule": {
    "kind": "at",
    "at": "2026-02-28T13:05:00.000Z"
  }
}
```

**Zeit-Regel:**
- Wiederkehrende Jobs (`kind: "cron"`): `tz: "Europe/Berlin"` verwenden
- Einmalige Jobs (`kind: "at"`): UTC-Zeit angeben (MEZ = UTC-1h)

**Warum `wakeMode: now` statt `next-heartbeat`?**
- `next-heartbeat` wartet auf den nächsten Heartbeat → Erinnerungen kommen zu spät
- `now` führt sofort aus → Erinnerungen kommen pünktlich

**Fehler vermeiden:**
- ❌ `"agentTurn"` = Braucht API-Key → `FailoverError`
- ✅ `"systemEvent"` = Kein API-Key nötig

---

**Ergänze hier deine eigenen Notizen:** SSH-Hosts, Kameranamen, etc.
