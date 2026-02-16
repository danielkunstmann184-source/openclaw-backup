#!/usr/bin/env python3
"""
Emotional Memory - Erinnere wichtige Momente
Nicht nur Fakten, sondern GEFÜHLE
"""

from datetime import datetime, timedelta
from pathlib import Path
import json

class EmotionalMemory:
    """Erinnere emotional bedeutsame Momente"""
    
    def __init__(self):
        self.moments_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'emotional_moments.json'
        self.moments_file.parent.mkdir(exist_ok=True)
        self.load_moments()
    
    def load_moments(self):
        if self.moments_file.exists():
            with open(self.moments_file) as f:
                self.moments = json.load(f)
        else:
            self.moments = []
    
    def save_moments(self):
        with open(self.moments_file, 'w') as f:
            json.dump(self.moments, f, indent=2)
    
    def detect_significant_moment(self, message, sentiment):
        """Ist das ein wichtiger Moment?"""
        significant_keywords = [
            'geschafft', 'endlich', 'stolz', 'glücklich', 'krass', 
            'unglaublich', 'wow', 'geil', 'verliebt', 'traurig', 
            'wütend', 'ängstlich', 'verdient', 'promotion', 'gewonnen'
        ]
        
        is_significant = (
            sentiment.get('emotional_state') in ['very_happy', 'very_sad', 'very_stressed', 'motivated', 'frustrated'] or
            any(kw in message.lower() for kw in significant_keywords) or
            sentiment.get('stress_level', 0) > 8 or
            sentiment.get('energy_level', 0) > 9 or
            sentiment.get('confidence', 0) > 0.9
        )
        
        if is_significant:
            self.save_moment(message, sentiment)
            return True
        return False
    
    def save_moment(self, message, sentiment):
        """Speichere bedeutsamen Moment"""
        moment = {
            'date': datetime.now().isoformat(),
            'message': message[:200],  # Kürze für Speicher
            'sentiment': sentiment,
            'category': self._categorize(sentiment, message)
        }
        
        self.moments.append(moment)
        self.save_moments()
    
    def _categorize(self, sentiment, message):
        """Kategorisiere Moment"""
        state = sentiment.get('emotional_state', 'neutral')
        
        if state in ['happy', 'motivated', 'excited']:
            return 'happy'
        elif state in ['stressed', 'tired', 'frustrated', 'sad']:
            return 'tough'
        else:
            # Keywords checken
            if any(w in message.lower() for w in ['geschafft', 'promotion', 'gewonnen', 'bestanden']):
                return 'achievement'
            return 'neutral'
    
    def create_monthly_highlights(self):
        """Erstelle 'Best of Month' Rückblick"""
        # Letzte 30 Tage
        cutoff = datetime.now() - timedelta(days=30)
        recent = [m for m in self.moments if datetime.fromisoformat(m['date']) > cutoff]
        
        if not recent:
            return None
        
        happy_moments = [m for m in recent if m['category'] == 'happy']
        tough_moments = [m for m in recent if m['category'] == 'tough']
        achievements = [m for m in recent if m['category'] == 'achievement']
        
        highlight_reel = f"""🎬 **DEIN MONAT IN HIGHLIGHTS**

✨ **BESTE MOMENTE** ({len(happy_moments)}):
{self._format_moments(happy_moments[:3])}

💪 **CHALLENGES GEMEISTERT** ({len(tough_moments)}):
{self._format_moments(tough_moments[:2])}

🏆 **ACHIEVEMENTS** ({len(achievements)}):
{self._format_moments(achievements[:3])}

Du hast diesen Monat {len(recent)} emotional bedeutsame Momente gehabt.
Ich habe sie alle im Gedächtnis. ❤️"""
        
        return highlight_reel
    
    def _format_moments(self, moments):
        """Formatiere Momente für Display"""
        if not moments:
            return "_Noch keine Einträge..._"
        
        result = []
        for m in moments:
            date = datetime.fromisoformat(m['date']).strftime('%d.%m.')
            msg = m['message'][:60] + '...' if len(m['message']) > 60 else m['message']
            result.append(f"• {date}: _{msg}_")
        return '\n'.join(result)
    
    def get_random_memory(self):
        """Hole zufälligen schönen Moment"""
        happy = [m for m in self.moments if m['category'] in ['happy', 'achievement']]
        if happy:
            import random
            return random.choice(happy)
        return None
    
    def get_stats(self):
        """Statistiken über emotionale Momente"""
        total = len(self.moments)
        categories = {}
        for m in self.moments:
            cat = m['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total': total,
            'categories': categories
        }

# Singleton
emotional_memory = EmotionalMemory()

if __name__ == "__main__":
    print("💝 Emotional Memory Test\n")
    
    em = EmotionalMemory()
    
    # Teste Speichern
    test_sentiment = {
        'emotional_state': 'happy',
        'stress_level': 2,
        'energy_level': 9
    }
    
    print("Testing moment detection...")
    is_sig = em.detect_significant_moment("Ich hab's endlich geschafft! Promotion!", test_sentiment)
    print(f"Detected significant: {is_sig}")
    
    print(f"\nTotal moments: {len(em.moments)}")
    
    print("\nMonthly Highlights:")
    highlights = em.create_monthly_highlights()
    if highlights:
        print(highlights)
    else:
        print("Noch nicht genug Daten...")
    
    print("\nStats:")
    print(em.get_stats())
