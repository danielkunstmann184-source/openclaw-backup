#!/usr/bin/env python3
"""
Auto-Update von PEOPLE.md - FIXED VERSION
Extrahiert Personen aus Memory-Dateien mit einfacher Keyword-Suche
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import re

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

def extract_people_from_text(text):
    """Extrahiere Personen-Namen aus Text mit einfachen Heuristiken"""
    # Bekannte Personen aus deinen Daten
    known_people = {
        'Juliane', 'Juli', 'Fin', 'Jonas', 'Finn',
        'Iwona', 'Ralf', 'Ramona', 'Steffen',
        'Michael', 'Max', 'Jerome', 'Fabian',
        'Patricia', 'Susanne', 'Sebastian', 'Denis',
        'Doreen'
    }
    
    found = set()
    for person in known_people:
        # Suche als ganzes Wort (nicht Teil eines anderen Worts)
        if re.search(r'\b' + re.escape(person) + r'\b', text, re.IGNORECASE):
            found.add(person)
    
    return found

def get_person_info(name):
    """Gibt bekannte Info zu einer Person zurück"""
    people_db = {
        'Juliane': {
            'relationship': 'Partnerin',
            'importance': 10,
            'birthday': '12.04.1995',
            'notes': 'Mutter von Fin und Jonas'
        },
        'Juli': {
            'relationship': 'Partnerin',
            'importance': 10,
            'birthday': '12.04.1995',
            'notes': 'Kurzform von Juliane'
        },
        'Fin': {
            'relationship': 'Sohn',
            'importance': 10,
            'birthday': '30.10.2015',
            'notes': 'Älterer Sohn, Wechselrhythmus jedes 2. Wochenende'
        },
        'Finn': {
            'relationship': 'Sohn',
            'importance': 10,
            'birthday': '30.10.2015',
            'notes': 'Kurzform von Fin'
        },
        'Jonas': {
            'relationship': 'Sohn',
            'importance': 10,
            'birthday': '05.05.2023',
            'notes': 'Jüngerer Sohn'
        },
        'Michael': {
            'relationship': 'Bester Freund',
            'importance': 9,
            'birthday': 'Unbekannt',
            'notes': 'Seit 20 Jahren befreundet'
        },
        'Iwona': {
            'relationship': 'Mutter',
            'importance': 8,
            'birthday': '09.05.1970',
            'notes': 'Arbeitsschutzklage in Bearbeitung'
        },
        'Ralf': {
            'relationship': 'Vater',
            'importance': 7,
            'birthday': '21.07.1967',
            'notes': 'Getrennt, Partnerin Susanne'
        },
        'Ramona': {
            'relationship': 'Schwiegermutter',
            'importance': 6,
            'birthday': 'Unbekannt',
            'notes': 'Mutter von Juliane'
        },
        'Steffen': {
            'relationship': 'Schwiegervater',
            'importance': 6,
            'birthday': 'Unbekannt',
            'notes': 'Vater von Juliane'
        },
        'Max': {
            'relationship': 'Schwager',
            'importance': 7,
            'birthday': 'Unbekannt',
            'notes': 'Mann deiner Schwester, Holland-Crew'
        },
        'Jerome': {
            'relationship': 'Kumpel',
            'importance': 6,
            'birthday': 'Unbekannt',
            'notes': 'Kumpel von Max, Holland-Crew'
        },
        'Fabian': {
            'relationship': 'Kumpel',
            'importance': 6,
            'birthday': 'Unbekannt',
            'notes': 'Bester Freund von Max, Holland-Crew'
        },
        'Patricia': {
            'relationship': 'Halbschwester',
            'importance': 5,
            'birthday': '1990',
            'notes': '4 Jahre älter, mütterlicherseits'
        },
        'Susanne': {
            'relationship': 'Stiefmutter',
            'importance': 4,
            'birthday': 'Unbekannt',
            'notes': 'Partnerin von Ralf'
        },
        'Sebastian': {
            'relationship': 'Stiefvater',
            'importance': 4,
            'birthday': '04.06.',
            'notes': 'Partner von Iwona'
        },
        'Denis': {
            'relationship': 'Chef',
            'importance': 7,
            'birthday': 'Unbekannt',
            'notes': 'Chef bei Creditreform'
        },
        'Doreen': {
            'relationship': 'Arbeitskollegin',
            'importance': 6,
            'birthday': 'Unbekannt',
            'notes': 'Creditreform, Erste Hilfe Kurs am 18.02.'
        }
    }
    
    return people_db.get(name, {
        'relationship': 'Kontakt',
        'importance': 5,
        'birthday': 'Unbekannt',
        'notes': 'Aus Memory-Dateien extrahiert'
    })

def scan_memory_files(days=30):
    """Scanne Memory-Dateien nach Personen"""
    memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
    
    all_people = set()
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        file_path = memory_dir / f"{date.strftime('%Y-%m-%d')}.md"
        if file_path.exists():
            text = file_path.read_text()
            found = extract_people_from_text(text)
            all_people.update(found)
    
    return all_people

def update_people_md():
    """Aktualisiere PEOPLE.md"""
    print("🤖 Auto-People-Update\n")
    
    # Scan nach Personen
    print("🔍 Scanning Memory-Dateien...")
    people = scan_memory_files(days=30)
    
    if not people:
        print("⚠️ Keine Personen gefunden")
        return
    
    print(f"✅ Gefunden: {', '.join(sorted(people))}\n")
    
    people_file = Path.home() / '.openclaw' / 'workspace' / 'PEOPLE.md'
    
    # Lese existierende PEOPLE.md
    if people_file.exists():
        existing = people_file.read_text()
    else:
        existing = "# People - Wichtige Menschen im Leben\n\n"
    
    # Für jede neue Person
    added_count = 0
    updated_count = 0
    
    for person in sorted(people):
        # Prüfe ob bereits existiert
        if f"## {person}" in existing or f"## {person} (" in existing:
            # Aktualisiere Letzter Kontakt
            old_contact = re.search(rf'## {re.escape(person)}.*?\*\*Letzter Kontakt\*\*: (\d{{4}}-\d{{2}}-\d{{2}})', existing, re.DOTALL)
            if old_contact:
                old_date = old_contact.group(1)
                new_date = datetime.now().strftime('%Y-%m-%d')
                if old_date != new_date:
                    existing = existing.replace(
                        f"**Letzter Kontakt**: {old_date}",
                        f"**Letzter Kontakt**: {new_date}"
                    )
                    updated_count += 1
                    print(f"🔄 {person} - Letzter Kontakt aktualisiert")
            continue
        
        # Überspringe Kurzformen wenn Langform existiert
        if person == 'Finn' and '## Fin ' in existing:
            continue
        if person == 'Juli' and '## Juliane' in existing:
            continue
        
        print(f"➕ Füge {person} hinzu...")
        info = get_person_info(person)
        
        section = f"""## {person}
- **Beziehung**: {info['relationship']}
- **Wichtigkeit**: {info['importance']}/10
- **Geburtstag**: {info['birthday']}
- **Letzter Kontakt**: {datetime.now().strftime('%Y-%m-%d')}
- **Notizen**: {info['notes']}

"""
        
        existing += section
        added_count += 1
        print(f"✅ {person} hinzugefügt")
    
    # Schreibe zurück
    people_file.write_text(existing)
    
    print(f"\n🎉 Fertig: {added_count} hinzugefügt, {updated_count} aktualisiert")

if __name__ == '__main__':
    print("="*60)
    print("🧠 AUTO-PEOPLE-UPDATE")
    print("="*60)
    update_people_md()
