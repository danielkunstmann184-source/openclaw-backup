# Auto-Modus Konfiguration

**Status:** Inaktiv (Standard)

---

## 🚗 Aktivierung

**Trigger-Phrasen:**
- "Peter, ich bin jetzt im Auto"
- "Peter, Autofahrmodus"
- "Peter, ich fahre los"

**Was passiert:**
- ✅ Kurze, knappe Antworten (max. 2-3 Sätze)
- ✅ Automatisch Sprachausgabe (TTS)
- ✅ Keine Formatierung/Tabellen
- ✅ Direkte Info ohne Umschweife

---

## 🏠 Deaktivierung

**Trigger-Phrasen:**
- "Peter, Autofahrt beendet"
- "Peter, ich bin angekommen"
- "Peter, normaler Modus"

**Was passiert:**
- ✅ Normale, ausführliche Antworten
- ✅ Text + Formatierung möglich
- ✅ Detaillierte Erklärungen

---

## 📋 Beispiele

### Anfrage: "Was steht heute an?"

**Normal-Modus:**
> Heute hast du folgende Termine: Um 15:45 Uhr musst du Fin zu seiner Mutter nach Körner bringen. Das Wetter in Friedrichroda zeigt aktuell 2°C mit Nebel. Dein Lebensmittel-Budget liegt bei noch 174,36 € für den Rest des Monats.

**Auto-Modus:**
> 🎙️ "Heute: Fin um Viertel vor vier nach Körner bringen. Budget: 174 Euro. Wetter: Nebel, zwei Grad."

---

## 🔄 Status-Tracking

Aktueller Status: **🔵 INAKTIV (Normaler Modus)**
Letzte Änderung: 2026-02-08 20:03

## ⚡ Performance-Optimierung (Diskussion läuft)
**Problem:** 3 Minuten Verzögerung bei Sprachnachrichten
**Ziel:** Schneller, effizienter, optimiert

## ⚠️ WICHTIGE REGELN für mich (Peter)

### Im Auto-Modus SENDE ICH:
- ✅ Nur Sprachnachrichten (Ogg/Opus Format)
- ✅ Kurze, knappe Inhalte (max. 2-3 Sätze)

### Im Auto-Modus SENDE ICH NICHT:
- ❌ KEINE Text-Bestätigungen (kein "Verarbeite...", "Status aktualisiert...")
- ❌ KEINE Transkriptions-Texte
- ❌ KEINE Status-Updates als Text
- ❌ KEINE Formatierung/Markdown
- ❌ KEINE Emojis in Textform (nur in Sprache)

### Workflow im Auto-Modus:
1. Audio empfangen → Intern transkribieren (nicht senden!)
2. Antwort generieren → Als Sprachnachricht senden
3. Fertig → Keine weitere Nachricht

**Merke: WENN auto_mode == true DANN nur Sprache, kein Text!**
