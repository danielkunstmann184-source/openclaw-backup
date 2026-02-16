#!/usr/bin/env python3
"""
Fallback System - Funktioniere IMMER, auch ohne Kimi
Kritisch für Production!
"""

import time
from pathlib import Path

class FallbackSystem:
    def __init__(self):
        self.kimi_available = True
        self.fallback_count = 0
        self.max_fallback_alerts = 3
        self.last_health_check = None
    
    def check_kimi_health(self):
        """Teste ob Kimi erreichbar ist"""
        try:
            from modules.kimi_helper import kimi
            response = kimi.ask("test", max_tokens=5, timeout=10)
            self.kimi_available = bool(response)
            self.last_health_check = time.time()
            return self.kimi_available
        except Exception as e:
            print(f"⚠️ Kimi Health Check failed: {e}")
            self.kimi_available = False
            return False
    
    def get_response_strategy(self):
        """Welche Strategie nutze ich?"""
        if self.kimi_available:
            self.fallback_count = 0
            return 'kimi'
        else:
            self.fallback_count += 1
            
            # Alert nach 3 Fallbacks
            if self.fallback_count == self.max_fallback_alerts:
                self.alert_user("⚠️ Kimi ist seit mehreren Stunden nicht erreichbar. Ich nutze Fallback-Strategien. Funktioniere trotzdem! 💪")
            
            return 'fallback'
    
    def fallback_sentiment(self, message):
        """Simple Sentiment wenn Kimi down"""
        try:
            from modules.sentiment_tracker import sentiment_tracker
            return sentiment_tracker.analyze_message(message)
        except:
            # Ultra-Fallback
            return {
                'sentiment': 'neutral',
                'stress_level': 5,
                'energy_level': 5,
                'emotional_state': 'neutral',
                'method': 'ultra_fallback'
            }
    
    def fallback_patterns(self):
        """Nutze gecachte Patterns"""
        import json
        patterns_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'learned_patterns_v2.json'
        if patterns_file.exists():
            try:
                with open(patterns_file) as f:
                    data = json.load(f)
                return data.get('patterns', {})
            except:
                pass
        return {}
    
    def fallback_briefing(self):
        """Simple Briefing ohne Kimi"""
        return """🌅 Guten Morgen!

⚠️ Kimi ist gerade nicht erreichbar, daher ein einfaches Briefing:

📅 Checke deine Termine in MEMORY.md
🌡️ Checke das Wetter selbst  
💡 Ich bin trotzdem für dich da!

Sobald Kimi wieder läuft, gibt's wieder smarte Briefings.

💪 Peter (im Fallback-Modus)"""
    
    def alert_user(self, message):
        """Sende Alert an User"""
        # Wird in Telegram-Integration genutzt
        print(f"🚨 ALERT: {message}")
        return message

# Singleton
fallback_system = FallbackSystem()

if __name__ == "__main__":
    print("🧪 Fallback System Test\n")
    
    fs = FallbackSystem()
    
    print("Testing Kimi Health...")
    health = fs.check_kimi_health()
    print(f"Kimi available: {health}")
    
    print(f"\nStrategy: {fs.get_response_strategy()}")
    
    print("\nTesting Fallback Sentiment...")
    result = fs.fallback_sentiment("Das ist ein Test")
    print(f"Result: {result}")
    
    print("\n✅ Fallback System ready!")
