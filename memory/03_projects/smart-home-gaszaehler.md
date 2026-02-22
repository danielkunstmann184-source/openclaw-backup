# Smart Home: Gaszähler-Monitoring

**Projektstart:** 22. Februar 2026  
**Status:** 💡 Ideenphase / Planung  
**Budget:** ~€100-120

---

## 🎯 Ziel
Automatische Überwachung des Gaszählers (GGT GT4) mit:
- Täglicher Verbrauchsanzeige
- Push-Benachrichtigungen bei erhöhtem Verbrauch
- Langzeitstatistiken über Wochen/Monate
- Integration in Smart Home Dashboard

---

## 🔧 Technische Lösung

### Gaszähler-Details
- **Modell:** GGT GT4 (Baujahr 1998)
- **Impuls:** 1 imp = 0,01 m³ (10 Liter)
- **Auslesung:** Magnetischer Reed-Schalter (außen anbringen)

### Hardware-Setup

#### 1. Home Assistant Zentrale
**Option A: Home Assistant Green (Empfohlen)**
- Preis: ~€100
- Vorteile: Fertiggerät, SSD eingebaut, langlebig, einfache Einrichtung

**Option B: Raspberry Pi 4 (4GB)**
- Preis: ~€70 + Zubehör
- Vorteile: Günstiger, mehr Bastel-Faktor

#### 2. ESP32 DevKit
- Preis: ~€8
- Mikrocontroller am Gaszähler
- Zählt Impulse über Reed-Schalter
- Sendet Daten per WiFi an Home Assistant

#### 3. Reed-Schalter
- Preis: ~€3-5
- Magnetischer Sensor
- Schließt bei jedem Impuls des Zählers
- Nicht-invasiv (außen anbringen)

#### 4. Zubehör
- Jumper-Kabel: ~€4
- USB-Stromversorgung
- Optional: 3D-gedrucktes Gehäuse

**Gesamtkosten:** ~€115 (mit Green) oder ~€95 (mit Pi)

---

## 📱 Dashboard: iPad 2

**Gerät:** iPad 2 (Modell A1396, 32GB, Baujahr 2011)

### Einsatzzweck
Das iPad wird als **permanentes Dashboard** für Home Assistant genutzt:

**Mögliche Anzeigen:**
- Aktueller Gaszählerstand & täglicher Verbrauch
- Heizungssteuerung & Temperatur
- Lichtsteuerung (später erweiterbar)
- Wetterdaten
- System-Status (Alerts, Notifications)

**Setup:**
- iPad an Dockingstation/Ständer anschließen
- Stromversorgung permanent
- Safari Browser → `http://homeassistant.local:8123`
- Home Assistant Dashboard im Vollbild/Kiosk-Modus
- Platzierung: Flur, Küche oder Wohnzimmer

**Vorteile:**
- 0€ zusätzliche Kosten (vorhandenes Gerät)
- Immer im Blick
- Touch-Steuerung für Smart Home
- Reaktiviert altes iPad sinnvoll

**Nachteile:**
- Nur Home Assistant Web-Interface (keine native App auf iOS 9)
- Kein Split-Screen Multitasking
- Browser-basiert = etwas langsamer als App

---

## 🛒 Einkaufsliste

### Option A: Home Assistant Green
- [ ] Home Assistant Green (~€100)
- [ ] ESP32 DevKit C (~€8)
- [ ] Reed-Schalter 10er Pack (~€4)
- [ ] Jumper-Kabel Set (~€4)
- [ ] LAN-Kabel (falls nicht vorhanden)

### Option B: Raspberry Pi 4
- [ ] Raspberry Pi 4 (4GB) (~€70)
- [ ] MicroSD-Karte 64GB A2 (~€10)
- [ ] ESP32 DevKit C (~€8)
- [ ] Reed-Schalter (~€4)
- [ ] Jumper-Kabel (~€4)

**Wo kaufen:** Amazon, Reichelt, BerryBase, home-assistant.io/green

---

## 📝 Nächste Schritte

1. [ ] **Hardware bestellen** (Entscheidung: Green oder Pi?)
2. [ ] **Home Assistant aufsetzen**
3. [ ] **ESP32 programmieren** (Peter hilft beim Code)
4. [ ] **Montage am Zähler** (Reed-Schalter anbringen)
5. [ ] **Dashboard einrichten** (iPad vorbereiten)
6. [ ] **Automatisierungen erstellen** (Alerts, tägliche Reports)

---

## 🚀 Erweiterungsmöglichkeiten

Nach dem Gaszähler kann das Smart Home wachsen:

| Bereich | Möglichkeiten |
|---------|---------------|
| **Beleuchtung** | Philips Hue, IKEA Tradfri, Shelly |
| **Heizung** | Smarte Thermostate, Zeitpläne |
| **Sensoren** | Temperatur, Feuchtigkeit, Bewegung, Fenster |
| **Sicherheit** | Kameras, Türsensoren, Alarm |
| **Strom** | Smarte Steckdosen, Verbrauch messen |
| **Media** | TV, Spotify, Sprachsteuerung |

---

## 💡 Warum das Projekt Sinn macht

- **Kostenersparnis:** Frühzeitig erkennen wenn Verbrauch explodiert
- **Transparenz:** Genau wissen, wann/wie viel verbraucht wird
- **Smart Home Basis:** Einstieg in Heimautomatisierung
- **Zukunftssicher:** Erweiterbar für weitere Geräte

---

## 📅 Erinnerungen

- **22.02.2026 20:08 Uhr:** Projekt-Entscheidung (Hardware bestellen?)

---

*Letzte Aktualisierung: 2026-02-22*