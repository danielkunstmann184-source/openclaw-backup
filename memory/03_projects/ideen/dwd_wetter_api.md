# DWD Wetter API Integration

**Status:** 💭 Idee | **Priorität:** Mittel | **Erstellt:** 2026-02-14

---

## 🎯 Ziel

Deutscher Wetterdienst (DWD) API nutzen für präzise, kostenlose Wetterdaten in Deutschland.

---

## Was wir wissen

### API-Quellen
- **Open Data Portal:** https://opendata.dwd.de/
- **Warnwetter-App API:** https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/
- **Alternative:** https://app-prod-ws.warnwetter.de/v16/

### Für Friedrichroda/Thüringer Wald
- **Station:** Kleiner Inselsberg (Nähe Brotterode/Bad Tabarz)
- **DWD-Stationsnummer:** 2618
- **WMO-Kennung:** M620
- **Höhe:** 732 m ü. NN

### Getestet
- ❌ Stations-ID 2618 → Access Denied
- ❌ Direkte API-Calls → 403/404 Fehler

### Mögliche Probleme
- API-Struktur geändert seit 2019 (Doku-Datum)
- Authentifizierung erforderlich?
- Falsche Endpunkt-URLs?

---

## Alternativen

| Option | Kosten | Genauigkeit | Einfachheit |
|--------|--------|-------------|-------------|
| **DWD API** | Kostenlos | ⭐⭐⭐ Sehr hoch | Komplex |
| **Weatherstack** | Free Tier | ⭐⭐ Gut | Einfach |
| **OpenWeatherMap** | Free Tier | ⭐⭐ Gut | Einfach |
| **wttr.in** (aktuell) | Kostenlos | ⭐⭐ Gut | Funktioniert |

---

## Nächste Schritte

1. Aktuelle DWD API-Doku finden (neuer als 2019)
2. Korrekte Endpunkte identifizieren
3. Stations-ID validieren
4. Test-Abfrage erfolgreich durchführen
5. Integration in Wetter-Cron

---

## Fazit

DWD ist die beste Datenquelle für deutsches Wetter, aber die Integration erfordert mehr Recherche. **Kein Blocker** - später angehen.

*Aktuelles System (wttr.in) funktioniert stabil.*
