# 🗂️ Dokumenten-Management mit KI

**Vision:** Digitale Ablage + KI-Agent für schnellen Zugriff und Verwaltung
**Erstellt:** 21.02.2026

---

## Ziel

Alle wichtigen Dokumente digitalisieren und einem OpenClaw-Agenten Zugang geben für:
- Schnelle Informationssuche
- Automatische Verwaltung
- Smarte Kategorisierung

---

## Technische Umsetzung

### 1. **Dokumenten-Erfassung**
| Methode | Tools |
|---------|-------|
| **Scanner** | Fujitsu ScanSnap, Doxie, oder Handy-Apps (Adobe Scan, Microsoft Lens) |
| **OCR** | Tesseract (lokal) oder AWS Textract |
| **Auto-Routing** | Hazel (Mac) oder Folder Actions (Windows/Linux) |

### 2. **Ablage-Struktur**
```
~/Dokumente/
├── 01_Finanzen/
│   ├── Steuern/
│   ├── Versicherungen/
│   └── Bank/
├── 02_Arbeit/
│   ├── Creditreform/
│   ├── Vertraege/
│   └── Loehne/
├── 03_Familie/
│   ├── Kinder/
│   ├── Gesundheit/
│   └── Wohnung/
├── 04_Auto/
├── 05_Sonstiges/
└── _INBOX/          # Neu hereinkommende Dokumente
```

### 3. **KI-Integration (MCP-Server)**

| Komponente | MCP-Server | Funktion |
|------------|------------|----------|
| **Dateizugriff** | Filesystem MCP | Lesen/Schreiben aller Dokumente |
| **Suche** | Vector DB MCP (Chroma/Pinecone) | Semantische Suche |
| **OCR** | Tesseract MCP | Text aus Bildern extrahieren |
| **Kategorisierung** | Lokales LLM (Ollama) | Auto-Sortierung in Ordner |

---

## Beispiel-Workflows

### Workflow 1: Neues Dokument einscannen
```
1. Dokument in Scanner legen
2. Auto-Speicherung in _INBOX/
3. KI erkennt: "Versicherungsvertrag Haftpflicht"
4. OCR extrahiert Text
5. KI verschiebt nach: 01_Finanzen/Versicherungen/Haftpflicht_2026.pdf
6. Indexierung in Vector-DB für Suche
```

### Workflow 2: Information finden
```
Du: "Wann läuft meine Kfz-Versicherung ab?"

KI:
→ Durchsucht Vector-DB nach "Kfz-Versicherung"
→ Findet: Dokument 04_Auto/Versicherung_Kfz_2025.pdf
→ OCR-Text: "Vertragslaufzeit: 01.03.2025 - 28.02.2026"
→ Antwort: "Läuft am 28.02.2026 ab — Verlängerung nötig!"
```

### Workflow 3: Deadline-Tracking
```
KI scannt täglich:
→ Rechnungen mit Fälligkeitsdatum
→ Vertragslaufzeiten
→ Termine aus Briefen

Erinnerung: "Stromrechnung über 142€ fällig in 3 Tagen"
```

---

## Speicher-Strategie: Bestehende Dropbox nutzen

**Status:** Daniel hat bereits Dropbox-Abo (bezahlt) mit unsortierten Fotos/Videos

**Ziel:** Dropbox strukturieren + dedizierter Bereich für Dokumente

---

## Dropbox-Struktur (Vorschlag)

```
Dropbox/
├── 📁 01_DOKUMENTE/              # ← NEU: Wichtige Dokumente (KI-verwaltet)
│   ├── 01_Finanzen/
│   │   ├── Steuern/
│   │   ├── Versicherungen/
│   │   └── Bank/
│   ├── 02_Arbeit/
│   │   ├── Creditreform/
│   │   ├── Vertraege/
│   │   └── Loehne/
│   ├── 03_Familie/
│   │   ├── Kinder/
│   │   ├── Gesundheit/
│   │   └── Wohnung/
│   ├── 04_Auto/
│   ├── 05_Sonstiges/
│   └── _INBOX/                   # Neue Dokumente hier rein
│
├── 📁 02_FOTOS_UND_VIDEOS/       # ← Bestehende Fotos/Videos strukturieren
│   ├── 2026/
│   │   ├── 01_Januar/
│   │   ├── 02_Februar/
│   │   └── ...
│   ├── 2025/
│   └── _UNSORTIERT/              # Bestehendes Chaos hier sammeln
│
└── 📁 03_SONSTIGES/              # Alles andere
    ├── Downloads/
├── _Backup/
```

### Trennung der Bereiche

| Bereich | Ordner | MCP-Server | Nutzung |
|---------|--------|------------|---------|
| **Dokumente** | `01_DOKUMENTE/` | ✅ Dropbox MCP | KI-gestützte Verwaltung |
| **Fotos/Videos** | `02_FOTOS_UND_VIDEOS/` | ❌ Kein MCP | Privat, manuell sortiert |
| **Sonstiges** | `03_SONSTIGES/` | Optional | Downloads, Temp |

**Wichtig:** Dokumente und private Medien **trennen** — Fotos brauchen keine KI-Verwaltung, Dokumente schon.

---

## Aufräum-Strategie für bestehende Dropbox

### Phase 1: Separieren (1-2 Stunden)
```
1. Neuen Ordner "01_DOKUMENTE" erstellen
2. Nach "Rechnung", "Vertrag", "Versicherung" in Dropbox suchen
3. Gefundene Dokumente → 01_DOKUMENTE/_INBOX/
4. Restliche Fotos/Videos → 02_FOTOS_UND_VIDEOS/_UNSORTIERT/
```

### Phase 2: Dokumente strukturieren (mit KI)
```
5. Dropbox MCP-Server einrichten
6. KI sortiert _INBOX automatisch in Unterordner
7. OCR für durchsuchbare PDFs
```

### Phase 3: Fotos später (manuell)
```
8. Fotos nach Datum sortieren (wenn Zeit ist)
9. Automatische Kamera-Uploads → 02_FOTOS_UND_VIDEOS/2026/...
```

---

## Vorteile dieser Struktur

| Problem | Lösung |
|---------|--------|
| Unsortierte Fotos | Getrennt von Dokumenten, keine KI nötig |
| Dokumente finden | KI durchsucht nur `01_DOKUMENTE/` |
| Dropbox voll | Nur Dokumente sind "Pflicht", Fotos können ausgelagert werden |
| Zugriff unterwegs | Dropbox-App für beide Bereiche |

---

## MCP-Server für Dropbox
