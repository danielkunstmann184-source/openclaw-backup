#!/usr/bin/env python3
"""
System Check - Teste alle Komponenten
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

def test_kimi():
    """Teste Kimi-Verbindung"""
    print("🧪 Teste Kimi-Verbindung...")
    try:
        from modules.kimi_helper import kimi
        response = kimi.ask("Antworte nur mit 'OK'", max_tokens=10)
        if response and 'OK' in response:
            print("✅ Kimi funktioniert!")
            return True
        else:
            print(f"⚠️ Kimi antwortet: {response}")
            return False
    except Exception as e:
        print(f"❌ Kimi-Fehler: {e}")
        return False

def test_sentiment():
    """Teste Sentiment-Analyse"""
    print("\n🧪 Teste Sentiment-Analyse...")
    try:
        from modules.sentiment_tracker_v2 import SentimentTrackerV2
        
        tracker = SentimentTrackerV2()
        test_cases = [
            ("Fuck, alles stress!", "negative"),
            ("Geil, super gelaufen!", "positive"),
            ("Was steht heute an?", "neutral")
        ]
        
        passed = 0
        for message, expected in test_cases:
            result = tracker.analyze_message(message)
            actual = result['sentiment']
            if actual == expected:
                print(f"✅ '{message[:20]}...' → {actual}")
                passed += 1
            else:
                print(f"⚠️ '{message[:20]}...' → Expected: {expected}, Got: {actual}")
        
        return passed >= 2
    except Exception as e:
        print(f"❌ Sentiment-Fehler: {e}")
        return False

def test_files():
    """Teste ob wichtige Files existieren"""
    print("\n🧪 Teste File-Struktur...")
    files = [
        ('SOUL.md', True),
        ('USER.md', True),
        ('MEMORY.md', True),
        ('PEOPLE.md', False),
        ('modules/kimi_helper.py', True),
        ('modules/sentiment_tracker_v2.py', True),
        ('data/sentiment_v2.json', False),
    ]
    
    workspace = Path.home() / '.openclaw' / 'workspace'
    all_exist = True
    
    for file, required in files:
        path = workspace / file
        exists = path.exists()
        if exists:
            print(f"✅ {file}")
        elif required:
            print(f"❌ {file} fehlt (REQUIRED!)")
            all_exist = False
        else:
            print(f"⚠️ {file} fehlt (optional)")
    
    return all_exist

def main():
    print("=" * 50)
    print("🤖 PETER SYSTEM CHECK")
    print("=" * 50)
    
    results = {
        'kimi': test_kimi(),
        'sentiment': test_sentiment(),
        'files': test_files(),
    }
    
    print("\n" + "=" * 50)
    print("📊 ERGEBNIS:")
    
    all_good = all(results.values())
    if all_good:
        print("✅ ALLE SYSTEME FUNKTIONIEREN!")
        print("🚀 Bereit für Production!")
    else:
        print("⚠️ EINIGE SYSTEME HABEN PROBLEME")
        print("Fehlerhafte Komponenten:")
        for component, status in results.items():
            if not status:
                print(f"  - {component}")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
