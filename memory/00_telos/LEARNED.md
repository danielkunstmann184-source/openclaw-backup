# LEARNED.md - Wichtige Erkenntnisse

**Was habe ich gelernt? Welche Lessons sind wertvoll?**

---

## 📚 Erkenntnisse über KI/Memory-Systeme

### Wie KI-Agenten sich erinnern (18.02.2026)
**Quelle:** damiangalarza.com - "How AI Agents Remember Things"

**Kern-Erkenntnis:** Storage ist einfach - das Schwierige ist zu wissen, **wann zu schreiben und wann zu laden**.

**Die 3 Memory-Typen:**
1. **Episodic** - Ereignisse (Tageslogs)
2. **Semantic** - Fakten/Präferenzen (MEMORY.md)
3. **Procedural** - Workflows/Routinen

**4 Mechanismen bei OpenClaw:**
- Bootstrap Loading (Session-Start)
- Pre-Compaction Flush (vor Context-Überlauf)
- Session Snapshot (bei /new)
- "Remember this" (manuelles Speichern)

**Anwendung auf unser System:**
- ✅ Unser Setup deckt alle 3 Typen ab
- ✅ TELOS-System = Semantic Memory
- ✅ Tagesdateien = Episodic Memory
- ✅ Cron-Jobs = "when to load"
- ✅ Automatisches Speichern = "when to write"

---

## 🏥 Neue Fähigkeiten

### Erste-Hilfe-Ausbildung (18.02.2026)
- **Erkenntnis:** Erste Hilfe ist einfacher als gedacht, aber Übung ist entscheidend
- **Lesson:** ABCDE-Schema strukturiert das Handeln in Notsituationen
- **Fähigkeit:** Betrieblicher Ersthelfer (DRK-zertifiziert)
- **Anwendung:** Im Alltag, bei Arbeit, unterwegs - immer bereit zu helfen

---

## 🧠 Lebenslehren

### Über Sucht und Bewältigung
- **Erkenntnis:** Glücksspielsucht ist eine Krankheit, keine Charakterschwäche
- **Lesson:** Hilfe annehmen ist keine Schande
- **Anwendung:** Heute bewusst risikoaversiv, 24h-Regel bei impulsiven Entscheidungen

### Über Familie
- **Erkenntnis:** Zeit mit den Kindern ist unersetzlich
- **Lesson:** Beruflicher Erfolg ohne Familie ist hohl
- **Anwendung:** Feierabend streng einhalten, Wochenende für Familie reserviert

### Über Finanzen
- **Erkenntnis:** Budget-Disziplin schafft Freiheit
- **Lesson:** Tracken was ausgegeben wird
- **Anwendung:** Gemeinsames Budget mit Juliane, wöchentliche Checks

---

## 💼 Berufliche Erkenntnisse

### Über Vertrieb
- **Erkenntnis:** Beziehungen sind wichtiger als harte Verkaufstaktiken
- **Lesson:** Ehrliche Beratung schlägt aggressive Akquise
- **Anwendung:** Fokus auf langfristige Kundenbeziehungen

### Über Zeitmanagement
- **Erkenntnis:** Systeme schlagen Willenskraft
- **Lesson:** Automatisierung wo möglich
- **Anwendung:** Cron-Erinnerungen, Tagesdateien, Checklisten

---

## 🔄 Aus Fehlern gelernt

| Fehler | Erkenntnis | Änderung |
|--------|-----------|----------|
| Impulsive Trading-Entscheidungen | Nie ohne 24h Schlaf entscheiden | Warte-Regel implementiert |
| "Ich merke mir das" | Session-Speicher ist flüchtig | Sofort in Dateien schreiben |
| Zu viele Projekte parallel | Fokus über Multitasking | Priorisierung nach Impact |

---

## 📚 Erkenntnisse durch OpenClaw/PAI

- **KI als Second Brain funktioniert** - aber nur mit konsequenter Persistenz
- **Cron-Jobs sind mächtig** - aber nur mit zuverlässiger Delivery
- **TELOS-Struktur hilft** - klare Ziele und Werte fokussieren

---

## 🎯 Wichtige Prinzipien (Zusammenfassung)

1. **Ehrlichkeit zuerst** - Mit sich selbst und anderen
2. **Familie vor Karriere** - Aber beides möglich mit Balance
3. **Systeme über Willenskraft** - Automatisierung ist Schlüssel
4. **Lernen aus Fehlern** - Jeder Fehler ist eine Lesson
5. **Geduld bei Entscheidungen** - 24h-Regel für wichtige Dinge

---

*Diese Liste wächst mit jeder Erfahrung.*
