# API-Keys Konfiguration

**Standort:** `~/.config/openclaw/`

## Warum nicht im Workspace?

API-Keys sind sensible Daten. Der Workspace wird in Git versioniert. Selbst mit `.gitignore` besteht das Risiko eines versehentlichen Commits.

**Lösung:** Keys außerhalb des Workspace-Ordners speichern.

## Aktuelle Keys

| Datei | Inhalt | Verwendung |
|-------|--------|------------|
| `~/.config/openclaw/.env.notion` | `NOTION_API_KEY=ntn_...` | Notion Tagebuch |
| `~/.config/openclaw/.env.api` | `BRAVE_API_KEY=...` | Brave Search |
| `~/.config/openclaw/.env.resend` | `RESEND_API_KEY=...` | Email-Versand |

## Scripts aktualisieren

Bei neuen Scripts dieses Pattern verwenden:

```bash
CONFIG_DIR="$HOME/.config/openclaw"
if [ -f "$CONFIG_DIR/.env.notion" ]; then
    source "$CONFIG_DIR/.env.notion"
else
    echo "❌ Config nicht gefunden"
    exit 1
fi
```

## Backup

Die Keys werden **nicht** mit dem Git-Repo gesichert. Bei Server-Neustart/Neuinstallation:

1. Keys aus sicherer Quelle wiederherstellen
2. Oder neu generieren (Notion: notion.so/my-integrations)

**Empfohlene Backup-Strategie:**
- Passwort-Manager (1Password, Bitwarden)
- Verschlüsselte Datei auf externem Medium
- Nicht im Git-Repo!
