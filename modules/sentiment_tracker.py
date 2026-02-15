#!/usr/bin/env python3
"""
Sentiment Tracker - Erkennt Stimmungen des Users
Speichert emotionale Zustände in JSON für adaptive Antworten
"""

import re
from datetime import datetime, timedelta
import json
from pathlib import Path

class SentimentTracker:
    def __init__(self):
        self.db_path = Path.home() / '.openclaw' / 'workspace' / 'data' / 'sentiment.json'
        self.db_path.parent.mkdir(exist_ok=True)
        self.load_history()
    
    def load_history(self):
        """Lade bisherige Sentiment-Daten"""
        if self.db_path.exists():
            with open(self.db_path) as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_history(self):
        """Speichere Sentiment-Daten"""
        with open(self.db_path, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def analyze_message(self, message, source="telegram"):
        """
        Analysiere eine Nachricht und erkenne Stimmung
        
        Returns: dict mit sentiment, stress_level, energy_level, emotional_state
        """
        message_lower = message.lower()
        
        # Deutsche und englische Indikatoren
        stress_indicators = [
            'fuck', 'scheiße', 'stress', 'nervt', 'keine zeit', 'deadline', 
            'dringend', 'chaos', 'überfordert', 'shit', 'verdammt', 'mist',
            'kacke', 'ärger', 'frust', 'panik', 'scheisse', 'stressig'
        ]
        
        positive_indicators = [
            'geil', 'nice', 'super', 'perfekt', 'läuft', 'freue mich', 
            'cool', 'genial', 'hammer', 'toll', 'spitze', 'awesome',
            'fantastisch', 'wunderbar', 'hervorragend', 'prima', 'top'
        ]
        
        tired_indicators = [
            'müde', 'erschöpft', 'kaputt', 'keine energie', 'schlapp', 
            'ko', 'ausgelaugt', 'schlafen', 'pennen', 'ruhe', 'pause',
            'k.o.', 'fertig', 'platt'
        ]
        
        motivated_indicators = [
            "let's go", 'machen wir', 'bock', 'auf geht\'s', 'los', 'ran',
            'los gehts', 'auf gehts', 'starten', 'durchstarten', 'motiviert',
            'feuer', 'gas geben', 'vollgas'
        ]
        
        frustrated_indicators = [
            'fuck', 'scheiße', 'verdammt', 'mist', 'kacke', 'ärgerlich',
            'nervig', 'blöd', 'doof', 'ärgere mich', 'wütend', 'sauer',
            'kotzt an', 'kotzen', 'aggro', 'aggressiv'
        ]
        
        # Zähle Indikatoren
        stress_count = sum(1 for ind in stress_indicators if ind in message_lower)
        positive_count = sum(1 for ind in positive_indicators if ind in message_lower)
        tired_count = sum(1 for ind in tired_indicators if ind in message_lower)
        motivated_count = sum(1 for ind in motivated_indicators if ind in message_lower)
        frustrated_count = sum(1 for ind in frustrated_indicators if ind in message_lower)
        
        # Nachrichtenlänge (gestresst = oft kurz und schnippisch)
        msg_length = len(message.split())
        is_short = msg_length < 5
        
        # Emojis analysieren
        emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]")
        emojis = emoji_pattern.findall(message)
        has_positive_emoji = any(e in ['😊','😄','😃','😁','🎉','🎊','🚀','💪','👍','❤️','🔥','✨','🌟','💯'] for e in emojis)
        has_negative_emoji = any(e in ['😔','😟','😠','😡','😢','😭','😤','😫','😩','🤬','💔','😰','😨'] for e in emojis)
        
        # Interpunktion (!!! = emotional)
        excessive_punctuation = message.count('!') > 2 or message.count('?') > 2
        
        # Berechne emotionalen Zustand
        if frustrated_count > 0 and stress_count > 0:
            emotional_state = 'frustrated'
            energy_level = max(0, 8 - frustrated_count)
            stress_level = min(10, 5 + frustrated_count * 2)
        elif tired_count > 0:
            emotional_state = 'tired'
            energy_level = max(0, 5 - tired_count * 2)
            stress_level = min(10, 4 + tired_count)
        elif stress_count > positive_count:
            emotional_state = 'stressed'
            energy_level = 7  # Gestresst = oft noch energiegeladen
            stress_level = min(10, stress_count * 3)
        elif motivated_count > 0:
            emotional_state = 'motivated'
            energy_level = 9
            stress_level = max(0, 5 - motivated_count)
        elif positive_count > 0 or has_positive_emoji:
            emotional_state = 'happy'
            energy_level = 7
            stress_level = max(0, 5 - positive_count)
        elif has_negative_emoji:
            emotional_state = 'neutral-negative'
            energy_level = 3
            stress_level = 6
        else:
            emotional_state = 'neutral'
            energy_level = 5
            stress_level = 5
        
        # Sentiment
        if positive_count > stress_count and positive_count > frustrated_count:
            sentiment = 'positive'
        elif stress_count > 0 or frustrated_count > 0 or tired_count > 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'message_preview': message[:50] + '...' if len(message) > 50 else message,
            'sentiment': sentiment,
            'stress_level': stress_level,
            'energy_level': energy_level,
            'emotional_state': emotional_state,
            'source': source,
            'indicators_found': {
                'stress': stress_count,
                'positive': positive_count,
                'tired': tired_count,
                'motivated': motivated_count,
                'frustrated': frustrated_count
            }
        }
        
        # Speichere in History
        self.history.append(result)
        self.save_history()
        
        return result
    
    def get_recent_mood(self, hours=24):
        """
        Analysiere die Stimmung der letzten X Stunden
        
        Returns: dict mit aggregierter Stimmung
        """
        cutoff = datetime.now() - timedelta(hours=hours)
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
                'sample_size': 0
            }
        
        # Aggregiere
        avg_stress = sum(h['stress_level'] for h in recent) / len(recent)
        avg_energy = sum(h['energy_level'] for h in recent) / len(recent)
        
        # Häufigster emotionaler Zustand
        states = [h['emotional_state'] for h in recent]
        dominant_state = max(set(states), key=states.count)
        
        # Overall Sentiment
        sentiments = [h['sentiment'] for h in recent]
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        
        if positive_count > negative_count:
            overall_sentiment = 'positive'
        elif negative_count > positive_count:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'overall_sentiment': overall_sentiment,
            'avg_stress': round(avg_stress, 1),
            'avg_energy': round(avg_energy, 1),
            'dominant_state': dominant_state,
            'sample_size': len(recent)
        }
    
    def should_check_wellbeing(self):
        """
        Sollte ich nach dem Wohlbefinden fragen?
        
        Returns: tuple (bool, str) - (Sollte fragen?, Grund)
        """
        mood = self.get_recent_mood(hours=48)
        
        # High stress über längere Zeit
        if mood['avg_stress'] > 7:
            return (True, "Du wirkst die letzten 2 Tage sehr gestresst. Alles okay? Brauchst du Unterstützung?")
        
        # Niedrige Energie anhaltend
        if mood['avg_energy'] < 3:
            return (True, "Du wirkst sehr müde in letzter Zeit. Genug geschlafen? Soll ich dich an eine Pause erinnern?")
        
        # Dominant negative
        if mood['dominant_state'] in ['stressed', 'tired', 'frustrated'] and mood['sample_size'] > 5:
            return (True, "Ich merke, dass es dir nicht so gut geht. Kann ich irgendwie helfen?")
        
        return (False, None)
    
    def get_mood_summary(self):
        """Gibt eine Zusammenfassung der aktuellen Stimmung"""
        mood = self.get_recent_mood(hours=24)
        
        emoji_map = {
            'happy': '😊',
            'motivated': '🚀',
            'neutral': '😐',
            'tired': '😴',
            'stressed': '😰',
            'frustrated': '😤',
            'neutral-negative': '😕'
        }
        
        emoji = emoji_map.get(mood['dominant_state'], '😐')
        
        summary = f"{emoji} Stimmung (24h): {mood['dominant_state'].upper()}\n"
        summary += f"Stress: {mood['avg_stress']}/10 | Energie: {mood['avg_energy']}/10\n"
        summary += f"Basis: {mood['sample_size']} Nachrichten"
        
        return summary

# Singleton-Instanz für einfachen Zugriff
sentiment_tracker = SentimentTracker()

if __name__ == "__main__":
    # Test
    test_messages = [
        "Fuck, alles stress, keine Zeit für nichts!",
        "Geil, heute lief alles super! 🎉",
        "Bin so müde und kaputt",
        "Let's go, voll motiviert heute! 💪",
        "Nur eine normale Nachricht"
    ]
    
    tracker = SentimentTracker()
    
    print("🧪 Sentiment Tracker Test\n")
    for msg in test_messages:
        result = tracker.analyze_message(msg)
        print(f"📝 '{msg[:40]}...'")
        print(f"   → {result['emotional_state'].upper()} (Stress: {result['stress_level']}/10, Energie: {result['energy_level']}/10)\n")
    
    print("\n📊 Zusammenfassung:")
    print(tracker.get_mood_summary())
    
    should_check, reason = tracker.should_check_wellbeing()
    if should_check:
        print(f"\n⚠️  Wohlbefinden-Check: {reason}")
