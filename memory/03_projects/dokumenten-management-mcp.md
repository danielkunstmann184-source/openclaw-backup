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

## Speicher-Strategie: Cloud-First

**Wichtig:** Dokumente werden NICHT nur lokal gespeichert, sondern primär in der Cloud für:
- ✅ Zugriff von überall (auch unterwegs)
- ✅ Backup falls Laptop kaputt/Festplatte defekt
- ✅ Synchronisation zwischen mehreren Geräten

### Cloud-Optionen

| Anbieter | Speicher | Preis/Monat | MCP-Server | Verschlüsselung |
|----------|----------|-------------|------------|-----------------|
| **Google Drive** | 15 GB (kostenlos) | €0-10 | ✅ Google Drive MCP | Client-seitig |
| **Dropbox** | 2 GB (kostenlos) | €0-12 | ✅ Dropbox MCP | Client-seitig |
| **OneDrive** | 5 GB (kostenlos) | €0-7 | ✅ OneDrive MCP | Client-seitig |
| **iCloud Drive** | 5 GB (kostenlos) | €0-10 | ⚠️ Eingeschränkt | Client-seitig |
| **pCloud** | 10 GB (kostenlos) | €0-10 | ❌ Kein MCP | Zero-Knowledge |
| **Synology NAS + Cloud** | Eigen | €0 | ✅ Filesystem MCP | Selbst kontrolliert |

### Empfohlene Lösung: Google Drive + Lokaler Cache

**Warum Google Drive?**
- 15 GB kostenlos (für Dokumente ausreichend)
- Beste MCP-Server-Unterstützung
- Zuverlässige Sync-Clients
- Gute Suche (auch ohne KI)

**Architektur:**
```
Scanner/Handy
     ↓
Google Drive (Cloud-Original)
     ↓
Laptop/PC (lokaler Cache)
     ↓
MCP-Server (Filesystem MCP)
     ↓
OpenClaw-Agent (KI-Zugriff)
```

### Backup-Strategie (3-2-1 Regel)

| Ebene | Speicherort | Art |
|-------|-------------|-----|
| **Original** | Google Drive | Primär (Cloud) |
| **Kopie 1** | Laptop | Lokaler Cache |
| **Kopie 2** | USB-Stick / externes HDD | Offline-Backup |

**Automatisierung:**
- Google Drive Sync = Echtzeit
- Rclone/Restic = Nightly Backup auf externes HDD

---

## Hardware-Setup (Cloud-First)

### Option A: Minimal (Cloud-only)
- **Scanner:** Handy + Adobe Scan (speichert direkt in Google Drive)
- **Speicher:** Google Drive 15 GB (kostenlos)
- **KI:** OpenClaw auf AWS (wie jetzt) oder Laptop
- **Backup:** Google Drive + optional USB-Stick
- **Kosten:** ~0€

### Option B: Komfort (Cloud + lokale KI)
- **Scanner:** Fujitsu ScanSnap ix1600 (~400€) → direkt zu Google Drive
- **Cloud:** Google Drive 100 GB (€2/Monat) oder 2 TB (€10/Monat)
- **KI:** Laptop (dein 2019er) mit MCP-Servern
- **Backup:** Google Drive + externes HDD (monatlich)
- **Kosten:** ~400€ einmalig + €2-10/Monat

### Option C: Power-User (Self-hosted Cloud)
- **Scanner:** Fujitsu ScanSnap ix1600 (~400€)
- **Cloud:** Synology NAS mit Cloud-Access (~500€)
- **Backup:** NAS + externe HDD + optional Backblaze B2
- **KI:** Docker auf NAS (24/7 verfügbar)
- **Kosten:** ~900€ einmalig + ~€5/Monat

---

## MCP-Server Stack (Cloud-Version)

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
