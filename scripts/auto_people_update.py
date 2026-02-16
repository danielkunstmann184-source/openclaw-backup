#!/usr/bin/env python3
"""
Auto-Update von PEOPLE.md mit Kimi!
Extrahiert automatisch Personen-Profile aus Memory-Dateien
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))
from modules.kimi_helper import kimi

def find_mentioned_people(days=30):
    """Finde alle erwähnten Personen in Memory"""
    memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
    
    # Lese letzte N Tage
    all_texts = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        file_path = memory_dir / f"{date.strftime('%Y-%m-%d')}.md"
        if file_path.exists():
            all_texts.append(file_path.read_text())
    
    if not all_texts:
        print("⚠️ Keine Memory-Dateien gefunden")
        return []
    
    print(f"🔍 Analysiere {len(all_texts)} Tage nach Personen...")
    
    # Nutze Kimi!
    people = kimi.find_mentioned_people(all_texts)
    
    return people

def generate_person_profile(name, days=30):
    """Generiere Profil für eine Person mit Kimi"""
    memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
    
    # Sammle Memory
    texts = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        file_path = memory_dir / f"{date.strftime('%Y-%m-%d')}.md"
        if file_path.exists():
            texts.append(file_path.read_text())
    
    # Nutze Kimi!
    profile = kimi.analyze_person_from_memory(name, texts)
    
    return profile

def update_people_md():
    """Aktualisiere PEOPLE.md automatisch"""
    print("🤖 Auto-People-Update mit Kimi\n")
    
    print("Schritt 1: Suche erwähnte Personen...")
    people = find_mentioned_people(days=30)
    
    if not people:
        print("⚠️ Keine Personen gefunden")
        return
    
    print(f"✅ Gefunden: {', '.join(people)}\n")
    
    people_file = Path.home() / '.openclaw' / 'workspace' / 'PEOPLE.md'
    
    # Lese existierende PEOPLE.md
    if people_file.exists():
        existing = people_file.read_text()
    else:
        existing = "# People - Wichtige Menschen im Leben\n\n"
    
    # Für jede neue Person: Generiere Profil
    added_count = 0
    for person in people:
        # Überspringe wenn bereits existiert
        if f"## {person}" in existing:
            print(f"⏭️  {person} existiert bereits")
            continue
        
        # Überspringe spezifische Nicht-Personen
        if person.lower() in ['telegram', 'notion', 'github', 'openclaw', 'whatsapp', 'discord']:
            print(f"⏭️  {person} ist kein Mensch")
            continue
        
        print(f"🧠 Generiere Profil für {person}...")
        profile = generate_person_profile(person)
        
        if 'error' in profile:
            print(f"❌ Fehler bei {person}: {profile['error']}")
            continue
        
        # Formatiere als Markdown
        importance = profile.get('importance', 5)
        relationship = profile.get('relationship', 'Unbekannt')
        
        section = f"""## {person}
- **Beziehung**: {relationship}
- **Wichtigkeit**: {importance}/10
- **Geburtstag**: Unbekannt
- **Letzter Kontakt**: {datetime.now().strftime('%Y-%m-%d')}
- **Kommunikationsstil**: {profile.get('communication_style', 'Unbekannt')}
"""
        
        # Interessen
        if 'interests' in profile:
            section += "- **Interessen**:\n"
            if profile['interests'].get('loves'):
                section += f"  - LOVES: {', '.join(profile['interests']['loves'][:5])}\n"
            if profile['interests'].get('avoids'):
                section += f"  - AVOIDS: {', '.join(profile['interests']['avoids'][:3])}\n"
        
        # Notizen
        if 'notes' in profile:
            section += f"- **Notizen**: {profile['notes'][:200]}\n"
        
        section += "\n"
        
        existing += section
        added_count += 1
        print(f"✅ {person} hinzugefügt\n")
    
    # Schreibe zurück
    people_file.write_text(existing)
    
    if added_count > 0:
        print(f"\n🎉 {added_count} neue Personen zu PEOPLE.md hinzugefügt!")
    else:
        print("\nℹ️  Keine neuen Personen gefunden")

def list_existing_people():
    """Liste alle existierenden Personen"""
    people_file = Path.home() / '.openclaw' / 'workspace' / 'PEOPLE.md'
    
    if not people_file.exists():
        return []
    
    content = people_file.read_text()
    import re
    
    # Finde alle ## Headers
    matches = re.findall(r'## ([^\n]+)', content)
    return [m.strip() for m in matches if not m.strip().startswith('People')]

if __name__ == '__main__':
    print("="*60)
    print("🧠 AUTO-PEOPLE-UPDATE")
    print("Extrahiert Personen automatisch aus deinen Memory-Dateien")
    print("="*60)
    
    # Zeige existierende Personen
    existing = list_existing_people()
    if existing:
        print(f"\n📋 Existierende Personen: {', '.join(existing)}")
    
    # Starte Update
    print()
    update_people_md()
