# Notion Tagebuch-Automatisierung

**Status:** 🟡 Geplant / Backlog  
**Priorität:** Niedrig-Mittel  

## Ziel

Das `diary_entry.sh` Script erweitern, sodass es automatisch:
1. Die lokale `memory/YYYY-MM-DD.md` liest
2. Den Inhalt in Notion-Blöcke konvertiert  
3. Den Tagebucheintrag damit füllt (statt Platzhaltern)

## Ansatz

### Einfache Lösung (reicht laut Daniel)
- Markdown-Datei als Plain Text lesen
- In Notion als `code` Block oder einfache Absätze einfügen
- Keine komplexe Format-Konvertierung nötig

### Aufwand
- **Zeit:** ~1-2 Stunden
- **Komplexität:** Mittel (API-Calls, File-Reading, Error Handling)

## Todo

- [ ] Script erweitern: Lese `memory/YYYY-MM-DD.md`
- [ ] Content in Notion-Blöcke umwandeln
- [ ] Existierenden Eintrag updaten (statt nur Platzhalter erstellen)
- [ ] Error Handling (was wenn Datei nicht existiert?)
- [ ] Testen mit verschiedenen Tagesdateien

## Alternative: Manuelle Übertragung

Bis die Automatisierung fertig ist: Ich übertrage auf Anfrage die Details manuell (wie heute geschehen).

---

**Erstellt:** 2026-02-19  
**Letzte Aktualisierung:** 2026-02-19
