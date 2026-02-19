# BMad Method × OpenClaw — 12-Agenten Entwicklungsteam

**Quelle:** https://github.com/ErwanLorteau/BMAD_Openclaw  
**Status:** 🟡 Idee / Möglichkeit für spätere Projekte  

---

## Was ist das?

**BMad Method × OpenClaw** ist ein strukturiertes Framework für AI-getriebene Software-Entwicklung mit **12 spezialisierten Agents**, die komplette Projekte durchführen — von der Idee bis zum fertigen Code.

### Die 12 Agents:

| Phase | Agent | Aufgabe |
|-------|-------|---------|
| **Planung** | Product Owner | Produkt-Brief erstellen |
| **Planung** | Business Analyst | PRD (Requirements, User Journeys) |
| **Planung** | Architect | Architektur-Dokument (Stack, Datenmodell, APIs) |
| **Planung** | UX Designer | UX Design Spec (Screens, Flows) |
| **Planung** | Scrum Master | Epics & Stories mit Acceptance Criteria |
| **Planung** | Readiness Check | GO/NO-GO Entscheidung vor Implementierung |
| **Umsetzung** | Create Story | Story-Dateien mit Tasks erstellen |
| **Umsetzung** | Dev Story | Implementation + Tests (red-green-refactor) |
| **Umsetzung** | Code Review | Adversarial Review (3-10 Issues minimum) |
| **Umsetzung** | UX Review | UX-Compliance Check |
| **Umsetzung** | QA Tester | Test Execution & Validation |
| **Umsetzung** | Retrospective | Sprint Retrospective & Learnings |

---

## Der Workflow

```
Idee → Product Owner → Business Analyst → Architect → UX Designer
→ Scrum Master → Readiness Check → GO/NO-GO
→ Stories erstellen → Code → Review → QA → Retrospective
```

---

## Technik

- Nutzt `sessions_spawn` (Sub-Agents) statt CLI
- Jeder Agent läuft als isolierte OpenClaw-Session
- State lives in files (nicht im Memory) → Crash-Recovery möglich
- Parallel-Arbeit mehrerer Agents gleichzeitig

---

## Vorteile gegenüber normalem Coden

| Feature | BMad × OpenClaw |
|---------|-----------------|
| **Parallele Arbeit** | Mehrere Agents gleichzeitig |
| **Crash-Recovery** | Agent stirbt → Orchestrator startet neu |
| **Token-Kosten** | Niedriger (isolierte Sub-Agents) |
| **Qualität** | Red-green-refactor, adversarial review, QA-Checks |
| **Zeit** | Idee → Prototyp in Tagen statt Wochen |

---

## Praktische Use Cases für mich

### 💼 Beruflich (Creditreform)

| Projekt | Beschreibung | Nutzen |
|---------|--------------|--------|
| **Kunden-Tracking-Tool** | Eigene Software statt Excel für Lead-Management | Bessere Übersicht, automatisierte Reports |
| **Automatisierte Reports** | Tool das Provisionen/Statistiken berechnet | Zeitersparnis, weniger Fehler |
| **Vertriebs-Dashboard** | Visualisierung der Akquise-Zahlen | Motivation, Ziele tracken |

### 🏠 Privat / Familie

| Projekt | Beschreibung | Nutzen |
|---------|--------------|--------|
| **Familien-Organizer** | App für Termine, Einkaufslisten, To-Dos | Alle auf einem Stand, weniger Chaos |
| **Haushalts-Budget-Tracker** | Eigene Software statt Tabellen | Bessere Finanzkontrolle |
| **Digitales Familienalbum** | Mit KI-gestützter Fotosuche | Erinnerungen bewahren, einfach finden |

### 🤖 Robotik-Projekt (mit Fin)

| Projekt | Beschreibung | Nutzen |
|---------|--------------|--------|
| **Steuerungs-Software** | Code für den Raspberry Pi Roboter | Funktioniert sofort |
| **Sprachbefehle-System** | Logik für "Licht an", "Foto machen" | Kindgerechte Bedienung |
| **Sensor-Dashboard** | Anzeige für Temperatur, Feuchtigkeit | Daten visualisieren |

### 💡 Business-Ideen

| Projekt | Beschreibung | Nutzen |
|---------|--------------|--------|
| **MVP testen** | Idee → funktionierender Prototyp in 1 Woche | Schnell validieren |
| **Landing Page** | Professionelle Website für ein Produkt | Online-Präsenz |
| **Automatisierungs-Tool** | Script das repetitive Aufgaben erledigt | Zeit sparen |

---

## Wichtige Unterscheidung

| Mein aktuelles Setup | BMad Method |
|---------------------|-------------|
| **Zweck:** Persönlicher Assistent, Organisation, Erinnerungen | **Zweck:** Software-Entwicklung, Code-Generierung |
| **Ich:** Nutze Tools, speichere Infos, helfe bei Entscheidungen | **Ich:** Werde zu einem 12-Personen-Entwicklungsteam |
| **Ergebnis:** Bessere Organisation, weniger vergessen | **Ergebnis:** Funktionierende Software, Apps, Tools |

---

## Wann lohnt es sich?

✅ **Sinnvoll wenn:**
- Konkretes Software-Projekt geplant
- Keine Lust/Zeit selbst zu coden
- Professionelles Ergebnis gewünscht
- Budget für Token/API-Kosten vorhanden

❌ **Nicht nötig wenn:**
- Alles läuft mit bestehenden Tools
- Kein konkretes Projekt in Aussicht
- Einfache Aufgaben (reichen meine aktuellen Skills)

---

## Nächste Schritte (falls interessiert)

1. **Repo clonen** in Workspace
2. **Config anpassen** für konkretes Projekt
3. **Ersten Workflow starten** (z.B. Product Owner für Idee X)
4. **Schritt für Schritt** durch die 12 Agents

---

**Erstellt:** 2026-02-19  
**Quelle:** https://github.com/ErwanLorteau/BMAD_Openclaw
