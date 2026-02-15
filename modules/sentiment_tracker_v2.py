#!/usr/bin/env python3
"""
Sentiment Tracker V2 - Mit Kimi-Power!
Verwendet Kimi 2.5 für echtes Verständnis statt Keyword-Matching
"""

import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))
from modules.kimi_helper import kimi

class SentimentTrackerV2:
    def __init__(self):
        self.db_path = Path.home() / '.openclaw' / 'workspace' / 'data' / 'sentiment_v2.json'
        self.db_path.parent.mkdir(exist_ok=True)
        self.load_history()
        
        # Nutze Kimi ab dieser Länge (kurze Messages = schnelle Keyword-Analyse)
        self.use_kimi_threshold = 8
    
    def load_history(self):
        if self.db_path.exists():
            with open(self.db_path) as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_history(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def analyze_message(self, message):
        """
        Analysiere mit Kimi für bessere Ergebnisse!
        
        Returns: dict mit Sentiment-Analyse
        """
        word_count = len(message.split())
        
        # Für sehr kurze Messages: Schnelle Keyword-Analyse (spart API-Calls)
        if word_count < self.use_kimi_threshold:
            return self._simple_analysis(message)
        
        # Für längere Messages: Nutze Kimi!
        else:
            return self._kimi_analysis(message)
    
    def _simple_analysis(self, message):
        """Schnelle Keyword-Analyse für kurze Messages"""
        message_lower = message.lower()
        
        # Schnelle Indikatoren
        stress_words = ['stress', 'scheiße', 'fuck', 'nervt', 'ärger', 'müde', 'kaputt']
        positive_words = ['super', 'geil', 'toll', 'läuft', 'freue', 'happy', 'gut']
        
        stress_count = sum(1 for w in stress_words if w in message_lower)
        positive_count = sum(1 for w in positive_words if w in message_lower)
        
        if stress_count > positive_count:
            emotional_state = 'stressed'
            stress_level = min(stress_count * 3, 10)
            energy_level = max(5 - stress_count, 1)
        elif positive_count > 0:
            emotional_state = 'happy'
            stress_level = max(5 - positive_count, 1)
            energy_level = min(5 + positive_count, 10)
        else:
            emotional_state = 'neutral'
            stress_level = 5
            energy_level = 5
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'message_preview': message[:50] + '...' if len(message) > 50 else message,
            'sentiment': 'positive' if emotional_state == 'happy' else 'negative' if emotional_state == 'stressed' else 'neutral',
            'stress_level': stress_level,
            'energy_level': energy_level,
            'emotional_state': emotional_state,
            'method': 'simple',
            'confidence': 0.6
        }
        
        self.history.append(result)
        self.save_history()
        return result
    
    def _kimi_analysis(self, message):
        """NEU: Power-Analyse mit Kimi! 🚀"""
        analysis = kimi.analyze_sentiment_advanced(message)
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'message_preview': message[:50] + '...' if len(message) > 50 else message,
            'sentiment': self._sentiment_from_state(analysis.get('emotional_state', 'neutral')),
            'stress_level': analysis.get('stress_level', 5),
            'energy_level': analysis.get('energy_level', 5),
            'emotional_state': analysis.get('emotional_state', 'neutral'),
            'reasoning': analysis.get('reasoning', ''),
            'method': 'kimi',
            'confidence': analysis.get('confidence', 0.8)
        }
        
        self.history.append(result)
        self.save_history()
        return result
    
    def _sentiment_from_state(self, state):
        """Map emotional state zu sentiment"""
        positive_states = ['happy', 'motivated', 'excited', 'relaxed']
        negative_states = ['stressed', 'tired', 'frustrated', 'sad', 'angry']
        
        if state in positive_states:
            return 'positive'
        elif state in negative_states:
            return 'negative'
        else:
            return 'neutral'
    
    def get_recent_mood(self, hours=24):
        """Aggregiere Stimmung der letzten X Stunden"""
        cutoff = datetime.now() - __import__('datetime').timedelta(hours=hours)
        recent = [
            h for h in self.history
            if datetime.fromisoformat(h['timestamp']) > cutoff
        ]
        
        if not recent:
            return {
                'overall_sentiment': 'neutral',
                'avg_stress': 5,
                'avg_energy': 5,
                'dominant_state': 'neutral',
                'sample_size': 0,
                'kimi_enhanced': False
            }
        
        # Aggregiere
        avg_stress = sum(h['stress_level'] for h in recent) / len(recent)
        avg_energy = sum(h['energy_level'] for h in recent) / len(recent)
        
        # Häufigster Zustand
        states = [h['emotional_state'] for h in recent]
        dominant_state = max(set(states), key=states.count)
        
        # Sentiment
        sentiments = [h['sentiment'] for h in recent]
        pos = sentiments.count('positive')
        neg = sentiments.count('negative')
        
        if pos > neg:
            overall = 'positive'
        elif neg > pos:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        # Kimi-Anteil
        kimi_count = sum(1 for h in recent if h.get('method') == 'kimi')
        
        return {
            'overall_sentiment': overall,
            'avg_stress': round(avg_stress, 1),
            'avg_energy': round(avg_energy, 1),
            'dominant_state': dominant_state,
            'sample_size': len(recent),
            'kimi_enhanced': kimi_count > 0,
            'kimi_percentage': round(kimi_count / len(recent) * 100, 1)
        }
    
    def should_check_wellbeing(self):
        """Sollte ich nach dem Wohlbefinden fragen?"""
        mood = self.get_recent_mood(hours=48)
        
        if mood['avg_stress'] > 7:
            return (True, "Du wirkst sehr gestresst. Alles okay? Kann ich helfen?")
        
        if mood['avg_energy'] < 3:
            return (True, "Du scheinst erschöpft. Genug Pause gemacht?")
        
        if mood['dominant_state'] in ['stressed', 'tired', 'frustrated'] and mood['sample_size'] > 5:
            return (True, "Ich merke, es läuft nicht so rund. Willst du darüber reden?")
        
        return (False, None)
    
    def get_mood_summary(self):
        """Gibt Zusammenfassung der aktuellen Stimmung"""
        mood = self.get_recent_mood()
        
        emoji_map = {
            'happy': '😊', 'motivated': '🚀', 'neutral': '😐',
            'tired': '😴', 'stressed': '😰', 'frustrated': '😤',
            'relaxed': '😌', 'excited': '🤩', 'angry': '😠'
        }
        
        emoji = emoji_map.get(mood['dominant_state'], '😐')
        kimi_badge = "🧠" if mood.get('kimi_enhanced') else ""
        
        summary = f"{emoji} Stimmung (24h): {mood['dominant_state'].upper()} {kimi_badge}\n"
        summary += f"Stress: {mood['avg_stress']}/10 | Energie: {mood['avg_energy']}/10\n"
        summary += f"Basis: {mood['sample_size']} Nachrichten"
        
        if mood.get('kimi_enhanced'):
            summary += f" ({mood['kimi_percentage']}% mit Kimi analysiert)"
        
        return summary

# Singleton
sentiment_tracker_v2 = SentimentTrackerV2()

if __name__ == "__main__":
    print("🧪 Sentiment Tracker V2 Test\n")
    
    tracker = SentimentTrackerV2()
    
    # Teste kurze Message (simple)
    print("1. Kurze Message (Simple Analysis):")
    r1 = tracker.analyze_message("Scheiße, alles Mist!")
    print(f"   → {r1['emotional_state'].upper()} | Method: {r1['method']}")
    
    # Teste lange Message (Kimi)
    print("\n2. Lange Message (Kimi Analysis):")
    long_msg = "Mein Chef hat mich wieder vollgemüllt mit Arbeit, ich kotze! Drei neue Projekte auf einmal, das ist doch nicht mehr normal."
    r2 = tracker.analyze_message(long_msg)
    print(f"   → {r2['emotional_state'].upper()} | Method: {r2['method']}")
    if r2.get('reasoning'):
        print(f"   Reasoning: {r2['reasoning']}")
    
    print("\n3. Zusammenfassung:")
    print(tracker.get_mood_summary())
