# Memory Architecture Upgrade (coolmanns)

**Quelle:** https://github.com/coolmanns/openclaw-memory-architecture

**Status:** 💡 Idee / Roadmap für später

## Warum interessant?

11-Layer Memory Architecture statt aktueller 5-Layer:
- SQLite + FTS5 für strukturierte Fakten
- Semantic Search mit Embeddings
- Auto-Pruning (alte Daten automatisch löschen)
- Gating Policies (Fehlervermeidung)
- Continuity Plugin (Cross-Session)
- Stability Plugin (Selbstüberwachung)

## Implementierungsphasen

**Phase 1:** SQLite + FTS5 für Fakten (Geburtstage, Termine)
**Phase 2:** Gating Policies für wiederkehrende Fehler
**Phase 3:** Semantic Search (Embeddings)
**Phase 4:** Continuity/Stability Plugins

## Offene Fragen
- Aufwand: 2-3 Tage für komplette Umstellung
- Priorität: Mittel (aktueller System funktioniert)
- Timing: Wenn aktuelles System an Grenzen stößt

---
*Erfasst: 2026-02-17*
