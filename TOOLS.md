# TOOLS.md - Lokale Notizen

Skills definieren _wie_ Tools funktionieren. Diese Datei ist für _deine_ Details — die Sachen, die einzigartig für dein Setup sind.

## Was hier rein gehört

Dinge wie:

- Kameranamen und Standorte
- SSH-Hosts und Aliases
- Bevorzugte Stimmen für TTS
- Lautsprecher/Raum-Namen
- Geräte-Spitznamen
- Alles Umgebungsspezifische

## Beispiele

```markdown
### Kameras

- wohnzimmer → Hauptbereich, 180° Weitwinkel
- haustür → Eingang, bewegungsgetriggert

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Bevorzugte Stimme: "Nova" (warm, leicht britisch)
- Standard-Lautsprecher: Küche HomePod
```

## Warum getrennt?

Skills sind geteilt. Dein Setup ist deins. Die Trennung bedeutet, du kannst Skills aktualisieren ohne deine Notizen zu verlieren, und Skills teilen ohne deine Infrastruktur zu leaken.

---

Füge hinzu was dir bei der Arbeit hilft. Das ist dein Spickzettel.

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
