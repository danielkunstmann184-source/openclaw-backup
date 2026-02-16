#!/usr/bin/env python3
"""
Adaptive Response - Passe Antworten an Stimmung an
"""

from .sentiment_tracker import sentiment_tracker

class AdaptiveResponse:
    def __init__(self):
        self.response_styles = {
            'frustrated': {
                'max_length': 120,
                'tone': 'calm',
                'use_emojis': False,
                'offer_help': True,
                'be_direct': True,
                'templates': [
                    "{message}\n\nIch sehe, das ist frustrierend. Brauchst du eine Pause oder Hilfe?",
                    "{message}\n\nLass uns Schritt für Schritt rangehen. Was ist das Dringendste?",
                    "{message}\n\nAtme kurz durch. Was kann ich tun?"
                ]
            },
            'stressed': {
                'max_length': 100,
                'tone': 'direct',
                'use_emojis': False,
                'offer_help': True,
                'be_direct': True,
                'templates': [
                    "{message}\n\nBrauchst du Unterstützung?",
                    "{message}\n\nWas ist Priorität #1?",
                    "{message}\n\nKurz & knapp - was jetzt wichtig ist."
                ]
            },
            'tired': {
                'max_length': 80,
                'tone': 'gentle',
                'use_emojis': True,
                'suggest_break': True,
                'templates': [
                    "{message} 😊\n\nVielleicht eine kurze Pause?",
                    "{message} 💤\n\nGenug geschlafen?",
                    "{message}\n\nMorgen ist auch noch ein Tag."
                ]
            },
            'motivated': {
                'max_length': 150,
                'tone': 'energetic',
                'use_emojis': True,
                'suggest_tasks': True,
                'templates': [
                    "{message} Let's go! 🚀",
                    "{message} Zeit zu rocken! 💪",
                    "{message} Auf geht's! 🔥"
                ]
            },
            'happy': {
                'max_length': 200,
                'tone': 'casual',
                'use_emojis': True,
                'allow_smalltalk': True,
                'templates': [
                    "{message} 🎉",
                    "{message} Super zu hören! 😊",
                    "{message} Das läuft! 🚀"
                ]
            },
            'neutral': {
                'max_length': 150,
                'tone': 'friendly',
                'use_emojis': True,
                'templates': [
                    "{message}",
                    "{message} 👍",
                    "{message} 🎯"
                ]
            },
            'neutral-negative': {
                'max_length': 120,
                'tone': 'supportive',
                'use_emojis': False,
                'templates': [
                    "{message}",
                    "{message}\n\nAlles in Ordnung?",
                    "{message}"
                ]
            }
        }
    
    def adapt_message(self, message, override_state=None):
        """
        Passe eine Nachricht an die aktuelle Stimmung an
        
        Args:
            message: Die ursprüngliche Nachricht
            override_state: Optional - erzwinge einen bestimmten State
            
        Returns: str: Angepasste Nachricht
        """
        # Hole aktuelle Stimmung
        if override_state:
            state = override_state
        else:
            mood = sentiment_tracker.get_recent_mood()
            state = mood['dominant_state']
        
        style = self.response_styles.get(state, self.response_styles['neutral'])
        
        # Wähle Template (rotiere oder wähle basierend auf Länge)
        import random
        template = random.choice(style['templates'])
        
        # Kürze Message falls nötig
        if len(message) > style['max_length']:
            message = message[:style['max_length']-3] + '...'
        
        # Wende Template an
        adapted = template.format(message=message)
        
        return adapted
    
    def should_reduce_notifications(self):
        """
        Sollte ich weniger Benachrichtigungen senden?
        
        Returns: bool
        """
        mood = sentiment_tracker.get_recent_mood()
        
        # Bei Stress: Reduziere nicht-kritische Benachrichtigungen
        if mood['avg_stress'] > 6:
            return True
        
        # Bei niedriger Energie: Auch reduzieren
        if mood['avg_energy'] < 4:
            return True
        
        # Bei Frustration: Sehr reduziert
        if mood['dominant_state'] == 'frustrated':
            return True
        
        return False
    
    def get_greeting(self):
        """
        Wähle passende Begrüßung basierend auf Stimmung
        
        Returns: str: Begrüßung
        """
        mood = sentiment_tracker.get_recent_mood()
        state = mood['dominant_state']
        
        greetings = {
            'frustrated': "Hey 👋",
            'stressed': "Hey 👋",
            'tired': "Moin 😊",
            'happy': "Hey! 🎉",
            'motivated': "Let's go! 🚀",
            'neutral': "Hey 👋",
            'neutral-negative': "Hey"
        }
        
        return greetings.get(state, "Hey")
    
    def add_mood_emoji(self, message):
        """
        Füge passenden Emoji basierend auf Stimmung hinzu
        """
        mood = sentiment_tracker.get_recent_mood()
        state = mood['dominant_state']
        
        emoji_map = {
            'frustrated': '😤',
            'stressed': '😰',
            'tired': '😴',
            'happy': '😊',
            'motivated': '🚀',
            'neutral': '👋',
            'neutral-negative': '😐'
        }
        
        emoji = emoji_map.get(state, '')
        
        # Füge Emoji am Ende hinzu, wenn nicht schon vorhanden
        if emoji and not any(e in message for e in emoji_map.values()):
            return f"{message} {emoji}"
        
        return message
    
    def format_for_stress_level(self, message, stress_level=None):
        """
        Formatiere Nachricht basierend auf Stress-Level
        """
        if stress_level is None:
            mood = sentiment_tracker.get_recent_mood()
            stress_level = mood['avg_stress']
        
        if stress_level > 7:
            # Hocher Stress: Bulletpoints, kurz, klar
            lines = message.split('\n')
            bullet_lines = []
            for line in lines:
                if line.strip() and not line.strip().startswith('•'):
                    bullet_lines.append(f"• {line.strip()}")
                else:
                    bullet_lines.append(line)
            return '\n'.join(bullet_lines)
        
        elif stress_level > 5:
            # Mittlerer Stress: Nummerierte Listen
            lines = message.split('\n')
            numbered_lines = []
            counter = 1
            for line in lines:
                if line.strip() and not line.strip()[0].isdigit():
                    numbered_lines.append(f"{counter}. {line.strip()}")
                    counter += 1
                else:
                    numbered_lines.append(line)
            return '\n'.join(numbered_lines)
        
        return message

# Singleton
adaptive_response = AdaptiveResponse()

if __name__ == "__main__":
    # Test
    print("🧪 Adaptive Response Test\n")
    
    test_cases = [
        ("Das ist eine Testnachricht für die Formatierung.", 'stressed'),
        ("Das ist eine Testnachricht für die Formatierung.", 'happy'),
        ("Das ist eine Testnachricht für die Formatierung.", 'tired'),
        ("Das ist eine Testnachricht für die Formatierung.", 'motivated'),
    ]
    
    ar = AdaptiveResponse()
    
    for msg, state in test_cases:
        adapted = ar.adapt_message(msg, override_state=state)
        print(f"[{state.upper()}] {adapted}\n")
