# Google Kalender Integration - Anleitung

*Schritt-für-Schritt zur Einrichtung deines Google Kalenders mit OpenClaw*

---

## Was du brauchst

1. **Google Konto** (gmail.com oder Google Workspace)
2. **Zugriff auf Google Calendar API** (kostenlos)
3. **Etwa 10-15 Minuten Zeit**

---

## Schritt 1: Google Cloud Projekt erstellen

1. Gehe zu [Google Cloud Console](https://console.cloud.google.com/)
2. Melde dich mit deinem Google-Konto an
3. Klicke oben auf das Projekt-Dropdown → **„Neues Projekt“**
4. Gib einen Namen ein (z.B. „OpenClaw Calendar“)
5. Klicke auf **„Erstellen“**

---

## Schritt 2: Google Calendar API aktivieren

1. Wähle dein neues Projekt aus (oben im Dropdown)
2. Gehe zu **„APIs & Dienste“** → **„Bibliothek“**
3. Suche nach **„Google Calendar API“**
4. Klicke drauf und dann auf **„Aktivieren“**

---

## Schritt 3: OAuth-Anmeldedaten erstellen

1. Gehe zu **„APIs & Dienste“** → **„Anmeldedaten“**
2. Klicke auf **„+ Anmeldedaten erstellen“** → **„OAuth-Client-ID“**
3. Wenn gefragt: **„OAuth-Zustimmungsbildschirm konfigurieren“**
   - Wähle **„Extern“** (oder „Intern“ bei Google Workspace)
   - Fülle Pflichtfelder aus (App-Name, E-Mail)
   - Speichern
4. Zurück zu **„Anmeldedaten“** → **„OAuth-Client-ID erstellen“**
   - Anwendungstyp: **„Desktop-App“**
   - Name: z.B. „OpenClaw Desktop"
5. Klicke auf **„Erstellen“**
6. **Client-ID und Client-Secret herunterladen** (JSON-Datei)

---

## Schritt 4: gog Skill installieren

Im Terminal ausführen:

```bash
npx clawhub install gog
```

---

## Schritt 5: Authentifizierung

1. Die heruntergeladene JSON-Datei (z.B. `client_secret_xxx.json`) auf dem Server speichern
2. Im Terminal:
   ```bash
   gog auth init --client-secret /pfad/zu/client_secret_xxx.json
   ```
3. Ein Link wird angezeigt → Im Browser öffnen
4. Mit deinem Google-Konto anmelden und Berechtigungen erteilen
5. Der Token wird lokal gespeichert

---

## Schritt 6: Test

```bash
# Kalender-Liste anzeigen
gog calendar list

# Termine für heute anzeigen
gog calendar events --today

# Neues Meeting erstellen
gog calendar add "Meeting mit Kunde" --start "2026-02-10T14:00" --duration 60m
```

---

## Schritt 7: OpenClaw Integration

Sobald `gog` funktioniert, kann ich:
- Deine Termine automatisch prüfen
- Vor wichtigen Meetings erinnern
- Neue Termine für dich erstellen
- Den Heartbeat mit Kalender-Checks befüllen

---

## Troubleshooting

**Fehler: „Access blocked“**
→ In Google Cloud Console: OAuth-Zustimmungsbildschirm → **„Testnutzer hinzufügen“** und deine E-Mail eintragen

**Keine Termine sichtbar**
→ Prüfe, ob du den richtigen Kalender ausgewählt hast (`gog calendar list` zeigt alle)

---

*Sobald du bei Schritt 5 bist oder Hilfe brauchst, sag Bescheid!*
