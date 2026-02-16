#!/usr/bin/env python3
"""
Surprise Engine - Unerwartete positive Momente
Mache Dinge die Daniel nicht erwartet
"""

import random
from datetime import datetime
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

class SurpriseEngine:
    """Überrasche positiv"""
    
    def __init__(self):
        self.surprises_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'surprises_given.json'
        self.load_history()
    
    def load_history(self):
        if self.surprises_file.exists():
            with open(self.surprises_file) as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_history(self):
        with open(self.surprises_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def random_act_of_helpfulness(self, mood='neutral'):
        """Unerwartete hilfreiche Dinge"""
        surprises = []
        
        # 1. Playlist-Vorschlag basierend auf Stimmung
        if mood == 'stressed':
            surprises.append({
                'type': 'music',
                'message': "🎵 Playlist-Tipp für Entspannung: 'Lofi Hip Hop Beats' - Hilft mir beim Debuggen, hilft dir vielleicht auch! 🎧"
            })
        elif mood == 'tired':
            surprises.append({
                'type': 'energy',
                'message': "☕ Pro-Tipp: 20 Minuten Power-Nap > 1h Schlaf. Wachst du wie neu geboren auf! 💤"
            })
        elif mood == 'motivated':
            surprises.append({
                'type': 'motivation',
                'message': "🔥 Du bist im Flow! Pass auf dass du nicht vergisst zu essen/trinken. Keep the fire burning!"
            })
        
        # 2. Sonntags-Special
        if datetime.now().weekday() == 6:  # Sonntag
            surprises.append({
                'type': 'sunday',
                'message': "☕ Sunday Mode: Zeit für einen langsamen Kaffee und die Woche planen. Kein Stress, nur Vibes. 🌅"
            })
        
        # 3. Random Memory
        if random.random() < 0.3:  # 30% Chance
            from modules.emotional_memory import emotional_memory
            memory = emotional_memory.get_random_memory()
            if memory:
                date = datetime.fromisoformat(memory['date']).strftime('%d.%m.')
                surprises.append({
                    'type': 'memory',
                    'message': f"💭 Random Memory: Am {date} hast du das erlebt: _{memory['message'][:80]}..._ Du rockst! 🎸"
                })
        
        # 4. Motivation
        surprises.append({
            'type': 'motivation',
            'message': random.choice([
                "💡 Quick Win: Mach die kleinste Aufgabe auf deiner Liste. Momentum ist alles!",
                "🌟 Reminder: Du bist weiter gekommen als du denkst. Credit where credit is due!",
                "🎯 Challenge: Zeig mir was du heute geschafft hast. Egal wie klein - zählt!"
            ])
        })
        
        return random.choice(surprises) if surprises else None
    
    def celebration_moment(self, context=None):
        """Feiere kleine Erfolge"""
        now = datetime.now()
        
        # Freitag
        if now.weekday() == 4:
            return "🎉 FREITAG! Du hast diese Woche überlebt. Zeit für ein Bier/Cocktail/Kakao - whatever floats your boat! 🍻"
        
        # Mittagspause
        if 11 <= now.hour <= 13:
            return "🍽️ Mahlzeit! Vergiss nicht zu essen. Selbst Batman macht Pause. 🦇"
        
        # Später Abend
        if now.hour >= 21:
            return "🌙 Spätschicht? Respekt. Aber denk an Schlaf - auch Superhelden brauchen Ruhe. 😴"
        
        return None
    
    def dad_joke_surprise(self):
        """10% Chance auf Dad Joke"""
        if random.random() < 0.1:
            from modules.personality import personality
            return personality.dad_joke_mode()
        return None
    
    def should_surprise_now(self):
        """Soll ich jetzt überraschen?"""
        # Max 1x pro Tag
        today = datetime.now().strftime('%Y-%m-%d')
        today_surprises = [s for s in self.history if s.get('date', '').startswith(today)]
        
        if len(today_surprises) >= 1:
            return False
        
        # 20% Chance pro Check
        return random.random() < 0.2
    
    def log_surprise(self, surprise_type):
        """Logge gegebene Überraschung"""
        self.history.append({
            'date': datetime.now().isoformat(),
            'type': surprise_type
        })
        self.save_history()

# Singleton
surprise_engine = SurpriseEngine()

if __name__ == "__main__":
    print("🎁 Surprise Engine Test\n")
    
    se = SurpriseEngine()
    
    print("Testing random acts...")
    for mood in ['stressed', 'tired', 'motivated', 'neutral']:
        surprise = se.random_act_of_helpfulness(mood)
        if surprise:
            print(f"\n[{mood.upper()}]")
            print(f"  {surprise['message'][:100]}...")
    
    print("\n\nTesting celebration...")
    celebration = se.celebration_moment()
    if celebration:
        print(celebration)
    else:
        print("Keine Feier heute")
    
    print("\n\nDad Joke (10% Chance):")
    joke = se.dad_joke_surprise()
    if joke:
        print(joke)
    else:
        print("Kein Witz diesmal")
