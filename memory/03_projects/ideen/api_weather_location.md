# API-Integration: Wetter & Standort

**Status:** 💭 Idee | **Priorität:** Mittel | **Erstellt:** 2026-02-14

---

## 🎯 Ziel

OpenClaw mit echten API-Daten erweitern - keine Workarounds mehr, sondern professionelle Datenquellen.

---

## 1. Weatherstack API

### Was es kann
- Echte Wetterdaten weltweit
- Aktuelles Wetter, Vorhersage, historische Daten
- JSON-Format, einfache Integration

### Für uns
- **Fix für Wetter-Cron:** Statt `$(curl wttr.in...)` → echte API-Antwort
- Zuverlässige Temperaturdaten für Friedrichroda & Gotha
- Wettervorhersage für Termine (z.B. "Morgen Regen in Arnstadt")

### Kosten
- **Free Tier:** 1000 Calls/Monat
- Das reicht für tägliche Abfragen (2 Städte = ~60 Calls/Monat)

### Beispiel-Output
```json
{
  "location": {"name": "Friedrichroda", "country": "Germany"},
  "current": {
    "temperature": 4,
    "weather_descriptions": ["Overcast"],
    "wind_speed": 20
  }
}
```

---

## 2. IP Geolocation API

### Was es kann
- Standort aus IP-Adresse ermitteln
- Stadt, Region, Land, Zeitzone
- Automatische Erkennung ohne Nutzereingabe

### Für uns
- **Automatische Standorterkennung:** Wo ist Daniel gerade?
- Kontextabhängige Erinnerungen:
  - "Du bist in Gotha → Wetter für Gotha"
  - "Du bist unterwegs → Verkehrsinfo?"
- Reise-Tracking (optional)

### Kosten
- **Free Tier:** 1000-10000 Calls/Monat (je nach Anbieter)

### Beispiel-Output
```json
{
  "ip": "xxx.xxx.xxx.xxx",
  "city": "Friedrichroda",
  "region_name": "Thuringia",
  "country_name": "Germany",
  "latitude": 50.85,
  "longitude": 10.56
}
```

---

## 🚀 Implementierungsplan

### Phase 1: Weatherstack
1. Account erstellen (kostenlos)
2. API Key sicher speichern
3. Wetter-Cron Job anpassen
4. Testlauf

### Phase 2: IP Geolocation
1. Anbieter wählen (ip-api.com, ipgeolocation.io, etc.)
2. Integration in Check-ins
3. Standortbasierte Features

---

## 💡 Zukünftige Ideen

Mit diesen APIs könnten wir später:
- Automatische Wetter-Warnungen ("Sturm morgen → Termin verschieben?")
- Reise-Tracking ("Du warst heute in Erfurt → Tagebuch-Eintrag?")
- Kontextabhängige Erinnerungen basierend auf Standort

---

*Next Step: Account bei Weatherstack erstellen?*
