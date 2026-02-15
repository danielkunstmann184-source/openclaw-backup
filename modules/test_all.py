#!/usr/bin/env python3
"""
Digital Twin Setup - Initialisiert alle Module und testet Funktionalität
"""

import sys
from pathlib import Path

# Füge workspace zu Path hinzu
sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

def test_sentiment_tracker():
    """Teste Sentiment Tracker"""
    print("\n" + "="*50)
    print("🧪 TEST 1: Sentiment Tracker")
    print("="*50)
    
    try:
        from modules.sentiment_tracker import SentimentTracker
        
        tracker = SentimentTracker()
        
        test_messages = [
            "Fuck, alles stress, keine Zeit für nichts!",
            "Geil, heute lief alles super! 🎉",
            "Bin so müde und kaputt",
            "Let's go, voll motiviert heute! 💪",
            "Nur eine normale Nachricht"
        ]
        
        for msg in test_messages:
            result = tracker.analyze_message(msg)
            print(f"✓ '{msg[:40]}...' → {result['emotional_state'].upper()}")
        
        print("\n📊 Zusammenfassung:")
        print(tracker.get_mood_summary())
        
        should_check, reason = tracker.should_check_wellbeing()
        if should_check:
            print(f"\n⚠️ Wohlbefinden-Check: {reason}")
        
        print("\n✅ Sentiment Tracker: OK")
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        return False

def test_adaptive_response():
    """Teste Adaptive Response"""
    print("\n" + "="*50)
    print("🧪 TEST 2: Adaptive Response")
    print("="*50)
    
    try:
        from modules.adaptive_response import AdaptiveResponse
        
        ar = AdaptiveResponse()
        
        test_cases = [
            ("Das ist eine Testnachricht für die Formatierung.", 'stressed'),
            ("Das ist eine Testnachricht für die Formatierung.", 'happy'),
            ("Das ist eine Testnachricht für die Formatierung.", 'tired'),
            ("Das ist eine Testnachricht für die Formatierung.", 'motivated'),
        ]
        
        for msg, state in test_cases:
            adapted = ar.adapt_message(msg, override_state=state)
            print(f"✓ [{state.upper()}] {adapted[:80]}...")
        
        print(f"\n✅ Adaptive Response: OK")
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        return False

def test_predictor():
    """Teste Predictor"""
    print("\n" + "="*50)
    print("🧪 TEST 3: Predictor")
    print("="*50)
    
    try:
        from modules.predictor import Predictor
        
        p = Predictor()
        
        print("📊 Evening Briefing:")
        briefing = p.generate_evening_briefing()
        print(briefing[:300] + "...")
        
        print("\n📈 Cognitive Load morgen:")
        cognitive = p.predict_cognitive_load()
        print(f"  Load: {cognitive['load']}/10")
        print(f"  Empfehlung: {cognitive['recommendation']}")
        
        print("\n💡 Contextual Suggestions:")
        for sugg in p.get_contextual_suggestions():
            print(f"  • {sugg['message']}")
        
        print(f"\n✅ Predictor: OK")
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_relationship_manager():
    """Teste Relationship Manager"""
    print("\n" + "="*50)
    print("🧪 TEST 4: Relationship Manager")
    print("="*50)
    
    try:
        from modules.relationship_manager import RelationshipManager
        
        rm = RelationshipManager()
        rm.ensure_people_file_exists()
        
        print("📋 Alle Personen:")
        people = rm.parse_people()
        for person in people:
            print(f"  • {person['name']} ({person['relationship']}) - {person['importance']}/10")
        
        print("\n⚠️ Vernachlässigte Beziehungen:")
        neglected = rm.check_neglected_relationships()
        if neglected:
            for item in neglected[:3]:  # Top 3
                print(f"  • {item['message']}")
        else:
            print("  ✅ Alle Beziehungen aktuell")
        
        print("\n🎂 Kommende Geburtstage:")
        birthdays = rm.check_upcoming_birthdays(days_ahead=365)
        if birthdays:
            for item in birthdays[:3]:  # Top 3
                print(f"  • {item['message']}")
        else:
            print("  Keine bevorstehenden Geburtstage bekannt")
        
        print(f"\n✅ Relationship Manager: OK")
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_tracker():
    """Teste Health Tracker"""
    print("\n" + "="*50)
    print("🧪 TEST 5: Health Tracker")
    print("="*50)
    
    try:
        from modules.health_tracker import HealthTracker
        
        ht = HealthTracker()
        
        print("🏥 Gesundheits-Summary:")
        print(ht.get_health_summary())
        
        print("\n💡 Gesundheits-Vorschläge:")
        suggestions = ht.get_health_suggestions()
        if suggestions:
            for sugg in suggestions:
                print(f"  • [{sugg['priority']}/10] {sugg['message']}")
        else:
            print("  Keine dringenden Vorschläge")
        
        print(f"\n✅ Health Tracker: OK")
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hauptfunktion - führt alle Tests aus"""
    print("\n" + "🚀"*25)
    print("  DIGITAL TWIN - SETUP & TEST")
    print("🚀"*25)
    
    results = {
        'sentiment': test_sentiment_tracker(),
        'adaptive': test_adaptive_response(),
        'predictor': test_predictor(),
        'relationship': test_relationship_manager(),
        'health': test_health_tracker()
    }
    
    # Zusammenfassung
    print("\n" + "="*50)
    print("📊 TEST-ZUSAMMENFASSUNG")
    print("="*50)
    
    for name, success in results.items():
        status = "✅ OK" if success else "❌ FEHLER"
        print(f"  {name:20} {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n{passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n🎉 ALLE MODULE FUNKTIONIEREN!")
        print("\nNächste Schritte:")
        print("  1. Sentiment-Tracking ist jetzt aktiv")
        print("  2. PEOPLE.md wurde erstellt (bitte anpassen)")
        print("  3. Health-Tracking bereit (manuelle Eingabe)")
        print("  4. Predictions laufen bei jedem Briefing")
        return 0
    else:
        print("\n⚠️  EINIGE TESTS FEHLGESCHLAGEN")
        return 1

if __name__ == "__main__":
    sys.exit(main())
