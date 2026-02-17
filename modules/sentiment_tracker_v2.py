#!/usr/bin/env python3
"""
Sentiment Tracker V2 - ROBUST MIT FALLBACK
Nutzt Kimi wenn verfügbar, sonst einfache Keyword-Analyse
"""

import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

# Versuche Kimi zu importieren
try:
    from config.kimi_config import KIMI_API_KEY, USE_KIMI_FALLBACK
    from modules.kimi_helper import kimi
    KIMI_AVAILABLE = bool(KIMI_API_KEY and len(KIMI_API_KEY) > 20)
except:
    KIMI_AVAILABLE = False

class SentimentTrackerV2:
    def __init__(self):
        self.db_path = Path.home() / '.openclaw' / 'workspace' / 'data' / 'sentiment_v2.json'
        self.db_path.parent.mkdir(exist_ok=True)
        self.load_data()
        
        # Einfache Keywords für Fallback
        self.keywords = {
            'happy': ['geil', 'super', 'toll', 'klasse', 'genial', 'läuft', 'perfekt'],
            'motivated': ['bock', 'auf geht\'s', 'let\'s go', 'motiviert', 'startklar'],
            'stressed': ['stress', 'scheiße', 'fuck', 'verdammt', 'keine zeit', 'hektisch'],
            'tired': ['müde', 'kaputt', 'erschöpft', 'schlafen', 'pennen'],
            'frustrated': ['ärgerlich', 'nervt', 'frust', 'verärgert', 'wütend'],
            'positive': ['gut', 'schön', 'freue', 'glücklich', 'zufrieden']
        }
    
    def load_data(self):
        if self.db_path.exists():
            with open(self.db_path) as f:
                self.data = json.load(f)
        else:
            self.data = []
    
    def save_data(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def analyze_message(self, message):
        """Analysiere Message - mit Kimi oder Fallback"""
        message_lower = message.lower()
        
        # Versuche Kimi (wenn verfügbar)
        if KIMI_AVAILABLE and USE_KIMI_FALLBACK:
            try:
                return self._analyze_with_kimi(message)
            except Exception as e:
                print(f"⚠️ Kimi failed, using fallback: {e}")
        
        # Fallback: Keyword-basiert
        return self._analyze_with_keywords(message)
    
    def _analyze_with_kimi(self, message):
        """Nutze Kimi für komplexe Analyse"""
        prompt = f"""Analysiere diese Nachricht auf Stimmung, Stress-Level (0-10) und Energie-Level (0-10).
        Antworte NUR im Format: sentiment|stress|energy
        
        Sentiment-Optionen: happy, motivated, neutral, tired, stressed, frustrated, positive, negative
        
        Nachricht: "{message}"
        """
        
        try:
            response = kimi.ask(prompt, max_tokens=50)
            parts = response.strip().split('|')
            
            if len(parts) >= 3:
                sentiment = parts[0].strip()
                stress = int(parts[1].strip()) if parts[1].strip().isdigit() else 5
                energy = int(parts[2].strip()) if parts[2].strip().isdigit() else 5
                
                return {
                    'sentiment': sentiment,
                    'stress_level': max(0, min(10, stress)),
                    'energy_level': max(0, min(10, energy)),
                    'method': 'kimi',
                    'timestamp': datetime.now().isoformat()
                }
        except:
            pass
        
        # Wenn Kimi-Antwort ungültig, Fallback
        return self._analyze_with_keywords(message)
    
    def _analyze_with_keywords(self, message):
        """Einfache Keyword-basierte Analyse"""
        message_lower = message.lower()
        
        # Zähle Treffer
        scores = {}
        for sentiment, words in self.keywords.items():
            scores[sentiment] = sum(1 for word in words if word in message_lower)
        
        # Bestimme dominante Stimmung
        if scores:
            dominant = max(scores, key=scores.get)
            if scores[dominant] > 0:
                sentiment = dominant
            else:
                sentiment = 'neutral'
        else:
            sentiment = 'neutral'
        
        # Heuristiken für Stress/Energie
        stress = 5
        energy = 5
        
        if 'stress' in message_lower or 'scheiße' in message_lower:
            stress = 8
            energy = 3
        elif 'müde' in message_lower or 'kaputt' in message_lower:
            stress = 6
            energy = 2
        elif 'super' in message_lower or 'geil' in message_lower:
            stress = 3
            energy = 8
        
        return {
            'sentiment': sentiment,
            'stress_level': stress,
            'energy_level': energy,
            'method': 'keyword',
            'timestamp': datetime.now().isoformat()
        }
    
    def track_message(self, message):
        """Track eine Message"""
        analysis = self.analyze_message(message)
        self.data.append(analysis)
        self.save_data()
        return analysis
    
    def get_recent_sentiment(self, days=7):
        """Holt Stimmung der letzten X Tage"""
        cutoff = datetime.now() - __import__('datetime').timedelta(days=days)
        recent = [d for d in self.data if __import__('datetime').datetime.fromisoformat(d['timestamp']) > cutoff]
        return recent
    
    def get_average_stress(self, days=7):
        """Durchschnittlicher Stress-Level"""
        recent = self.get_recent_sentiment(days)
        if not recent:
            return 5
        return sum(d['stress_level'] for d in recent) / len(recent)
    
    def get_dominant_sentiment(self, days=7):
        """Häufigste Stimmung"""
        recent = self.get_recent_sentiment(days)
        if not recent:
            return 'neutral'
        
        from collections import Counter
        sentiments = [d['sentiment'] for d in recent]
        return Counter(sentiments).most_common(1)[0][0]

# Singleton
tracker = SentimentTrackerV2()

if __name__ == "__main__":
    # Test
    test_messages = [
        "Fuck, alles stress!",
        "Geil, super gelaufen!",
        "Was steht heute an?",
        "Ich bin so müde"
    ]
    
    print("🧪 Sentiment Tracker V2 Test\n")
    print(f"Kimi verfügbar: {KIMI_AVAILABLE}\n")
    
    for msg in test_messages:
        result = tracker.analyze_message(msg)
        print(f"'{msg}'")
        print(f"  → {result['sentiment']} (Stress: {result['stress_level']}, Energie: {result['energy_level']}, Methode: {result['method']})\n")
