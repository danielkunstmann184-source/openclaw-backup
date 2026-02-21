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

## Hardware-Setup

### Option A: Minimal (Laptop)
- Scanner: Handy + Adobe Scan
- Speicher: Laptop-SSD + Cloud-Backup
- KI: Lokales Ollama
- Kosten: ~0€

### Option B: Komfort (NAS)
- Scanner: Fujitsu ScanSnap ix1600 (~400€)
- Speicher: Synology NAS (~300-500€)
- KI: Docker auf NAS oder Laptop
- Kosten: ~700-900€ einmalig

### Option C: Power-User
- Scanner: Professionell mit ADF
- NAS: Leistungsstark (8GB+ RAM)
- GPU: Für schnelles OCR
- Kosten: ~1500€+

---

## MCP-Server Stack

```yaml
# docker-compose.yml Beispiel
services:
  # Dokumenten-Verwaltung
  filesystem-mcp:
    image: mcp/filesystem
    volumes:
      - ~/Dokumente:/docs:ro
  
  # Vector-Datenbank für Suche
  chroma:
    image: chromadb/chroma
    volumes:
      - ./chroma-data:/data
  
  # OCR für gescannte PDFs
  tesseract-mcp:
    image: mcp/tesseract
  
  # KI-Modell (lokal)
  ollama:
    image: ollama/ollama
    volumes:
      - ollama:/root/.ollama
```

---

## Nächste Schritte

- [ ] Scanner aussuchen (Handy vs. dediziert)
- [ ] Ablage-Struktur finalisieren
- [ ] Test mit 10-20 Dokumenten
- [ ] MCP-Server aufsetzen (Docker)
- [ ] Integration mit OpenClaw

---

## Zugehörige Dateien

- `memory/99_tracking/lauf_log_2026.md` — Beispiel für Tracking
- `memory/03_projects/` — Projekte könnten hier verknüpft werden
- `PEOPLE.md` — Kontakte für Versicherungen/Behörden
