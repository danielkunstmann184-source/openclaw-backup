# Open Library API Integration

**Status:** 💭 Idee | **Priorität:** Niedrig-Mittel | **Erstellt:** 2026-02-14

---

## 🎯 Ziel

Internet Archive / Open Library API in OpenClaw integrieren, um kostenlosen Zugriff auf Bücher zu ermöglichen.

---

## Was möglich ist

### 1. Bücher suchen
- API-Endpunkt: `/search.json`
- Suche nach Titel, Autor, ISBN, Thema
- JSON-Response mit Metadaten

### 2. Buch-Details abrufen
- API-Endpunkt: `/books/{olid}.json`
- Cover-Bilder
- Verfügbarkeit (online lesen, ausleihen, download)
- Volltext (wenn verfügbar)

### 3. Lesen/Borgen
- Direktlinks zu archive.org
- Download-Links (PDF/ePub)
- Ausleih-Funktion über API

---

## Beispiele für Daniel

### Fachbücher / Business
- Marketing, Verkauf, Kommunikation
- Unternehmensführung
- Historische Wirtschaftsbücher

### Klassiker
- Deutsche Literatur (Goethe, Schiller, Kafka)
- Weltliteratur
- Philosophie

### Seltenes
- Alte Fachbücher
- Historische Dokumente
- Bücher, die nicht mehr erhältlich sind

---

## API-Endpunkte

```
BASE: https://openlibrary.org

Suche:
/search.json?q={query}
/search.json?author={author}
/search.json?subject={topic}

Buch-Details:
/books/{olid}.json
/works/{olid}.json

Cover:
/covers/b/id/{cover_id}-L.jpg
```

---

## Nutzungsszenarien

| Szenario | Befehl |
|----------|--------|
| Buch suchen | "Suche Buch über Verkaufstechniken" |
| Autor finden | "Finde Bücher von Dale Carnegie" |
| Thema | "Suche nach Time Management Büchern" |
| Details | "Zeige mir Details zu Buch XYZ" |
| Lesen | "Öffne Buch zum Lesen" |

---

## Nächste Schritte

1. Test-Queries über API
2. Integration in Chat-Workflow
3. Cover-Anzeige implementieren
4. Download/Ausleihe ermöglichen

---

*Kostenlos, keine API-Key nötig, fair-use Limits*
