#!/usr/bin/env python3
"""
Relationship Manager - Pflege soziale Beziehungen
Verwaltet PEOPLE.md und erinnert an wichtige soziale Interaktionen
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

class RelationshipManager:
    def __init__(self):
        self.people_file = Path.home() / '.openclaw' / 'workspace' / 'PEOPLE.md'
    
    def ensure_people_file_exists(self):
        """Erstelle PEOPLE.md wenn nicht vorhanden"""
        if not self.people_file.exists():
            template = """# People - Wichtige Menschen im Leben

## Juliane (Partnerin) 💕
- **Beziehung**: Partnerin / Ehefrau
- **Wichtigkeit**: 10/10
- **Geburtstag**: 12.04.1995
- **Letzter Kontakt**: {today}
- **Kommunikationsstil**: Direkt, pragmatisch
- **Interessen**: 
  - LOVES: Familie, Ordnung, Planung
  - AVOIDS: Unzuverlässigkeit
- **Notizen**: 
  - Zwei gemeinsame Kinder: Fin und Jonas

## Fin (Sohn) 👦
- **Beziehung**: Sohn
- **Wichtigkeit**: 10/10
- **Geburtstag**: 30.10.2015
- **Letzter Kontakt**: {today}

## Jonas (Sohn) 👶
- **Beziehung**: Sohn
- **Wichtigkeit**: 10/10
- **Geburtstag**: 05.05.2023
- **Letzter Kontakt**: {today}

## Michael (Freund) 🤝
- **Beziehung**: Bester Freund
- **Wichtigkeit**: 9/10
- **Geburtstag**: Unbekannt
- **Letzter Kontakt**: {today}
- **Notizen**:
  - Seit 20 Jahren befreundet
  - Aktuell etwas distanziert

## Iwona (Mutter) 👩
- **Beziehung**: Mutter
- **Wichtigkeit**: 8/10
- **Geburtstag**: Unbekannt
- **Letzter Kontakt**: {today}

## Ralf (Vater) 👨
- **Beziehung**: Vater
- **Wichtigkeit**: 7/10
- **Geburtstag**: Unbekannt
- **Letzter Kontakt**: {today}
""".format(today=datetime.now().strftime('%Y-%m-%d'))
            
            self.people_file.write_text(template)
            print(f"✅ PEOPLE.md erstellt unter {self.people_file}")
    
    def parse_people(self):
        """
        Parse PEOPLE.md
        Returns: list von Personen-Dictionaries
        """
        self.ensure_people_file_exists()
        
        if not self.people_file.exists():
            return []
        
        content = self.people_file.read_text()
        people = []
        
        # Split by ## headers
        sections = re.split(r'\n## ', content)
        
        for section in sections[1:]:  # Skip first (title)
            person = self._parse_person_section(section)
            if person:
                people.append(person)
        
        return people
    
    def _parse_person_section(self, section):
        """Parse eine Person-Sektion"""
        lines = section.strip().split('\n')
        
        # Name aus erster Zeile
        name_line = lines[0]
        name_match = re.match(r'([^\(]+)', name_line)
        if not name_match:
            return None
        
        name = name_match.group(1).strip()
        
        person = {
            'name': name,
            'raw_section': section,
            'relationship': 'Unbekannt',
            'importance': 5,
            'last_contact': None,
            'birthday': None
        }
        
        # Parse Felder
        for line in lines[1:]:
            line = line.strip()
            
            # Beziehung
            if line.startswith('- **Beziehung**:'):
                person['relationship'] = line.split(':')[1].strip()
            
            # Wichtigkeit
            elif line.startswith('- **Wichtigkeit**:'):
                importance_match = re.search(r'(\d+)/10', line)
                if importance_match:
                    person['importance'] = int(importance_match.group(1))
            
            # Letzter Kontakt
            elif line.startswith('- **Letzter Kontakt**:'):
                date_str = line.split(':')[1].strip()
                try:
                    person['last_contact'] = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    person['last_contact'] = None
            
            # Geburtstag
            elif line.startswith('- **Geburtstag**:'):
                birthday = line.split(':')[1].strip()
                person['birthday'] = birthday
        
        return person
    
    def check_neglected_relationships(self):
        """
        Wer wurde vernachlässigt?
        Returns: list von Personen die kontaktiert werden sollten
        """
        people = self.parse_people()
        neglected = []
        
        for person in people:
            if not person.get('last_contact'):
                continue
            
            days_since = (datetime.now() - person['last_contact']).days
            importance = person.get('importance', 5)
            
            # Regel: Je wichtiger, desto öfter Kontakt
            max_days = {
                10: 3,    # Sehr wichtig: alle 3 Tage
                9: 7,     # Wichtig: wöchentlich
                8: 10,
                7: 14,    # Wichtig: alle 2 Wochen
                6: 14,
                5: 21,    # Normal: alle 3 Wochen
                4: 30,
                3: 30,
                2: 60,
                1: 90
            }
            
            threshold = max_days.get(importance, 30)
            
            if days_since > threshold:
                neglected.append({
                    'person': person,
                    'days_since': days_since,
                    'message': f"📞 {person['name']} ({person['relationship']}): {days_since} Tage nicht kontaktiert",
                    'priority': importance
                })
        
        # Sortiere nach Wichtigkeit & Zeit
        neglected.sort(
            key=lambda x: (x['priority'] * -1, x['days_since']),
            reverse=False
        )
        
        return neglected
    
    def check_upcoming_birthdays(self, days_ahead=30):
        """
        Kommende Geburtstage
        Returns: list von Birthdays in den nächsten X Tagen
        """
        people = self.parse_people()
        upcoming = []
        today = datetime.now()
        
        for person in people:
            birthday_str = person.get('birthday')
            if not birthday_str or birthday_str == 'Unbekannt':
                continue
            
            # Parse Geburtstag
            birthday = self._parse_birthday(birthday_str, today.year)
            
            if not birthday:
                continue
            
            # Wenn schon vorbei, nächstes Jahr
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            
            days_until = (birthday - today).days
            
            if 0 <= days_until <= days_ahead:
                upcoming.append({
                    'person': person,
                    'days_until': days_until,
                    'date': birthday,
                    'message': self._get_birthday_message(person, days_until),
                    'priority': 10 if days_until <= 3 else 8
                })
        
        upcoming.sort(key=lambda x: x['days_until'])
        return upcoming
    
    def _parse_birthday(self, birthday_str, year):
        """Parse Geburtstag-String zu datetime"""
        # Versuche verschiedene Formate
        formats = [
            '%d.%m.%Y',      # 12.04.1995
            '%d.%m',         # 12.04
            '%d. %B %Y',     # 12. April 1995
            '%d. %B',        # 12. April
        ]
        
        for fmt in formats:
            try:
                birthday = datetime.strptime(birthday_str, fmt)
                # Setze Jahr wenn nicht im Format
                if '%Y' not in fmt:
                    birthday = birthday.replace(year=year)
                return birthday
            except:
                continue
        
        return None
    
    def _get_birthday_message(self, person, days_until):
        """Generiere Birthday-Reminder Message"""
        name = person['name']
        relationship = person.get('relationship', '')
        
        if days_until == 0:
            return f"🎉 HEUTE hat {name} ({relationship}) Geburtstag!"
        elif days_until == 1:
            return f"🎂 MORGEN: {name}'s Geburtstag - noch Zeit für Geschenk?"
        elif days_until <= 3:
            return f"📅 In {days_until} Tagen: {name}'s Geburtstag"
        elif days_until <= 7:
            return f"💡 In einer Woche: {name}'s Geburtstag"
        else:
            return f"📆 In {days_until} Tagen: {name}'s Geburtstag"
    
    def update_last_contact(self, person_name, date=None):
        """
        Update "Letzter Kontakt" für eine Person
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime('%Y-%m-%d')
        
        # Lese File
        content = self.people_file.read_text()
        
        # Finde Person-Sektion und update
        pattern = rf'(## {re.escape(person_name)}.*?- \*\*Letzter Kontakt\*\*:) \d{{4}}-\d{{2}}-\d{{2}}'
        replacement = rf'\1 {date_str}'
        
        updated = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Schreibe zurück
        self.people_file.write_text(updated)
        print(f"✅ Letzter Kontakt für {person_name} aktualisiert: {date_str}")
    
    def add_person(self, name, relationship, importance=5, birthday=None, notes=""):
        """
        Füge neue Person zu PEOPLE.md hinzu
        """
        self.ensure_people_file_exists()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        new_entry = f"""
## {name}
- **Beziehung**: {relationship}
- **Wichtigkeit**: {importance}/10
- **Geburtstag**: {birthday or 'Unbekannt'}
- **Letzter Kontakt**: {today}
- **Notizen**: {notes}
"""
        
        # Append to file
        with open(self.people_file, 'a') as f:
            f.write(new_entry)
        
        print(f"✅ {name} zu PEOPLE.md hinzugefügt")
    
    def get_relationship_summary(self):
        """Gibt eine Zusammenfassung aller Beziehungen"""
        people = self.parse_people()
        
        summary = "👥 **Deine wichtigen Menschen:**\n\n"
        
        for person in people:
            name = person['name']
            relationship = person['relationship']
            importance = person['importance']
            
            if person['last_contact']:
                days_since = (datetime.now() - person['last_contact']).days
                status = f"{days_since} Tage"
            else:
                status = "Unbekannt"
            
            # Emoji basierend auf Wichtigkeit und Zeit
            if importance >= 9:
                emoji = "❤️"
            elif importance >= 7:
                emoji = "🤝"
            else:
                emoji = "👤"
            
            summary += f"{emoji} **{name}** ({relationship}) - Kontakt: {status}\n"
        
        return summary

# Singleton
relationship_manager = RelationshipManager()

if __name__ == "__main__":
    # Test
    print("🧪 Relationship Manager Test\n")
    
    rm = RelationshipManager()
    rm.ensure_people_file_exists()
    
    print("📋 Alle Personen:")
    for person in rm.parse_people():
        print(f"• {person['name']} ({person['relationship']}) - Wichtigkeit: {person['importance']}/10")
    
    print("\n⚠️ Vernachlässigte Beziehungen:")
    neglected = rm.check_neglected_relationships()
    if neglected:
        for item in neglected:
            print(f"• {item['message']}")
    else:
        print("✅ Alle Beziehungen aktuell")
    
    print("\n🎂 Kommende Geburtstage:")
    birthdays = rm.check_upcoming_birthdays(days_ahead=365)
    if birthdays:
        for item in birthdays:
            print(f"• {item['message']}")
    else:
        print("Keine bevorstehenden Geburtstage bekannt")
