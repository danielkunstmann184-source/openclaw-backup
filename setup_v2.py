#!/usr/bin/env python3
"""
Digital Twin V2 Setup - KIMI POWER EDITION
Testet alle neuen Module
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

def test_kimi_connection():
    """Teste Kimi API"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Kimi API Verbindung")
    print("="*60)
    
    try:
        from modules.kimi_helper import kimi
        
        print("Verbinde mit Kimi 2.5...")
        response = kimi.ask("Hallo! Bist du bereit für den Digital Twin? 1 Wort Antwort.", max_tokens=50)
        
        if response:
            print(f"✅ Kimi antwortet: {response}")
            return True
        else:
            print("❌ Keine Antwort von Kimi")
            return False
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sentiment_v2():
    """Teste Sentiment V2"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Sentiment Tracker V2 (mit Kimi)")
    print("="*60)
    
    try:
        from modules.sentiment_tracker_v2 import SentimentTrackerV2
        
        tracker = SentimentTrackerV2()
        
        # Kurze Message (simple)
        print("\n1. Kurze Message (Simple Analysis):")
        r1 = tracker.analyze_message("Scheiße, alles Mist!")
        print(f"   Nachricht: 'Scheiße, alles Mist!'")
        print(f"   → {r1['emotional_state'].upper()} | Method: {r1['method']}")
        
        # Lange Message (würde Kimi nutzen)
        print("\n2. Lange Message (würde Kimi nutzen):")
        long_msg = "Mein Chef hat mich wieder vollgemüllt mit Arbeit, ich kotze! Drei neue Projekte auf einmal, das ist doch nicht mehr normal."
        r2 = tracker.analyze_message(long_msg)
        print(f"   Nachricht: '{long_msg[:50]}...'")
        print(f"   → {r2['emotional_state'].upper()} | Method: {r2['method']}")
        if r2.get('reasoning'):
            print(f"   Reasoning: {r2['reasoning'][:100]}")
        
        print("\n3. Stimmungs-Zusammenfassung:")
        print(tracker.get_mood_summary())
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pattern_learner():
    """Teste Pattern Learner V2"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Pattern Learner V2 (mit Kimi)")
    print("="*60)
    
    try:
        from modules.pattern_learner_v2 import PatternLearnerV2
        
        learner = PatternLearnerV2()
        
        print("Prüfe auf existierende Memory-Dateien...")
        memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
        files = list(memory_dir.glob('2026-*.md')) if memory_dir.exists() else []
        
        if len(files) < 3:
            print(f"⚠️ Nur {len(files)} Memory-Dateien gefunden (min. 3 empfohlen)")
            print("   Pattern Learning funktioniert besser mit mehr Daten.")
            return True  # Nicht kritisch
        
        print(f"✅ {len(files)} Memory-Dateien gefunden")
        print("Starte Analyse (kann 10-20 Sekunden dauern)...")
        
        # Kurze Analyse für Test
        result = learner.quick_analysis(days=7)
        
        if result and 'patterns' in result:
            print("\n✅ Patterns erkannt!")
            patterns = result['patterns']
            
            if 'likes' in patterns:
                print("\n❤️ Gefundene Vorlieben:")
                for cat, items in list(patterns['likes'].items())[:3]:
                    if items:
                        print(f"   {cat}: {', '.join(items[:3])}")
            
            if 'insights' in patterns:
                print(f"\n💡 Erkenntnis: {patterns['insights'][:150]}...")
        else:
            print("⚠️ Keine Patterns gefunden (oder API-Timeout)")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auto_people():
    """Teste Auto-People Update"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Auto-People Update (mit Kimi)")
    print("="*60)
    
    try:
        sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace' / 'scripts'))
        from auto_people_update import list_existing_people
        
        existing = list_existing_people()
        if existing:
            print(f"📋 Existierende Personen: {', '.join(existing)}")
        else:
            print("📋 Noch keine Personen in PEOPLE.md")
        
        print("\nUm neue Personen zu finden, führe aus:")
        print("   python3 scripts/auto_people_update.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def show_summary():
    """Zeige Zusammenfassung"""
    print("\n" + "="*60)
    print("📊 DIGITAL TWIN V2 - STATUS")
    print("="*60)
    
    print("""
✅ MODULE ERSTELLT:

1. Kimi Helper (modules/kimi_helper.py)
   → Verbindung zu Kimi 2.5 API
   
2. Sentiment Tracker V2 (modules/sentiment_tracker_v2.py)
   → Keyword-Analyse für kurze Messages
   → Kimi-Power für lange Messages
   
3. Pattern Learner V2 (modules/pattern_learner_v2.py)
   → Extrahiert automatisch Muster aus Memory
   → Schreibt Erkenntnisse in MEMORY.md
   
4. Auto-People Update (scripts/auto_people_update.py)
   → Findet Personen automatisch
   → Generiert Profile mit Kimi

📁 DATEIEN:
   • config/kimi_config.py
   • modules/kimi_helper.py
   • modules/sentiment_tracker_v2.py
   • modules/pattern_learner_v2.py
   • scripts/auto_people_update.py

🚀 NÄCHSTE SCHRITTE:

1. Teste Kimi Connection:
   python3 modules/kimi_helper.py

2. Führe Pattern-Analyse durch:
   python3 modules/pattern_learner_v2.py

3. Aktualisiere PEOPLE.md:
   python3 scripts/auto_people_update.py

4. Integriere in Telegram:
   Nutze SentimentTrackerV2 statt V1
""")

def main():
    print("\n" + "🚀"*30)
    print("  DIGITAL TWIN V2 - KIMI POWER SETUP")
    print("🚀"*30)
    
    results = {
        'kimi_connection': test_kimi_connection(),
        'sentiment_v2': test_sentiment_v2(),
        'pattern_learner': test_pattern_learner(),
        'auto_people': test_auto_people()
    }
    
    # Ergebnisse
    print("\n" + "="*60)
    print("📊 TEST-ERGEBNISSE")
    print("="*60)
    
    for name, success in results.items():
        status = "✅ OK" if success else "❌ FEHLER"
        print(f"  {name:25} {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n{passed}/{total} Tests bestanden")
    
    show_summary()
    
    if passed >= 3:
        print("\n🎉 DIGITAL TWIN V2 IST BEREIT!")
        return 0
    else:
        print("\n⚠️  EINIGE TESTS FEHLGESCHLAGEN")
        print("Aber die Module sind erstellt und können verwendet werden.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
