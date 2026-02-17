#!/usr/bin/env python3
"""
Performance Report - FIXED VERSION
Mit Fehlerbehandlung und Datenvalidierung
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

def safe_divide(numerator, denominator, default=0):
    """Sichere Division"""
    try:
        if denominator and denominator != 0:
            return numerator / denominator
        return default
    except (TypeError, ZeroDivisionError):
        return default

def safe_get(data, key, default=0):
    """Sicherer Zugriff auf Dictionary-Werte"""
    try:
        value = data.get(key, default)
        if isinstance(value, (int, float)):
            return value
        return default
    except (TypeError, AttributeError):
        return default

def analyze_week():
    """Analysiere letzte Woche"""
    
    # 1. Sentiment-Stats
    sentiment_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'sentiment_v2.json'
    
    recent = []
    avg_stress = 0
    avg_energy = 0
    positive_pct = 0
    negative_pct = 0
    kimi_pct = 0
    
    if sentiment_file.exists():
        try:
            with open(sentiment_file) as f:
                history = json.load(f)
            
            # Letzte 7 Tage
            week_ago = datetime.now() - timedelta(days=7)
            recent = [
                h for h in history 
                if isinstance(h, dict) and datetime.fromisoformat(h.get('timestamp', '2000-01-01')) > week_ago
            ]
            
            if recent:
                # Sichere Berechnungen
                stress_values = [safe_get(h, 'stress_level') for h in recent]
                energy_values = [safe_get(h, 'energy_level') for h in recent]
                
                avg_stress = safe_divide(sum(stress_values), len([s for s in stress_values if s > 0]))
                avg_energy = safe_divide(sum(energy_values), len([e for e in energy_values if e > 0]))
                
                # Stimmungs-Verteilung
                sentiments = [h.get('sentiment', 'neutral') for h in recent]
                positive_count = sum(1 for s in sentiments if s in ['positive', 'happy', 'motivated'])
                negative_count = sum(1 for s in sentiments if s in ['negative', 'stressed', 'frustrated', 'tired'])
                
                positive_pct = safe_divide(positive_count * 100, len(sentiments))
                negative_pct = safe_divide(negative_count * 100, len(sentiments))
                
                # Kimi-Nutzung
                kimi_usage = sum(1 for h in recent if h.get('method') == 'kimi')
                kimi_pct = safe_divide(kimi_usage * 100, len(recent))
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️ Fehler beim Lesen der Sentiment-Daten: {e}")
    
    # 2. Pattern-Stats
    patterns_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'learned_patterns_v2.json'
    
    temporal_count = 0
    likes_count = 0
    dislikes_count = 0
    
    if patterns_file.exists():
        try:
            with open(patterns_file) as f:
                data = json.load(f)
            if isinstance(data, dict):
                patterns = data.get('patterns', {})
                temporal_count = len(patterns.get('temporal_patterns', {}))
                likes = patterns.get('likes', {})
                dislikes = patterns.get('dislikes', {})
                likes_count = sum(len(v) for v in likes.values() if isinstance(v, list))
                dislikes_count = sum(len(v) for v in dislikes.values() if isinstance(v, list))
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"⚠️ Fehler beim Lesen der Pattern-Daten: {e}")
    
    # 3. Gesundheits-Stats
    health_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'health.json'
    gym_count = 0
    sleep_avg = 0
    
    if health_file.exists():
        try:
            with open(health_file) as f:
                health_data = json.load(f)
            
            week_ago_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            # Zähle Gym-Besuche letzte Woche
            gym_sessions = health_data.get('gym_sessions', [])
            gym_count = sum(1 for g in gym_sessions if isinstance(g, dict) and g.get('date', '') >= week_ago_str)
            
            # Durchschnittlicher Schlaf
            sleep_entries = health_data.get('sleep', [])
            recent_sleep = [safe_get(s, 'hours') for s in sleep_entries if isinstance(s, dict) and s.get('date', '') >= week_ago_str]
            sleep_avg = safe_divide(sum(recent_sleep), len(recent_sleep))
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"⚠️ Fehler beim Lesen der Health-Daten: {e}")
    
    # 4. Vergleich zu Vorwoche (wenn Daten vorhanden)
    prev_week_positive = "N/A"
    
    # 5. Generiere Report
    report = f"""📊 **WOCHENREPORT** ({datetime.now().strftime('%Y-%m-%d')})
{'=' * 50}

🧠 **SENTIMENT-ANALYSE** (Letzte 7 Tage)
• Messages analysiert: {len(recent)}
• Durchschnitt Stress: {avg_stress:.1f}/10
• Durchschnitt Energie: {avg_energy:.1f}/10
• Stimmung:
  - Positiv: {positive_pct:.0f}%
  - Negativ: {negative_pct:.0f}%
  - Neutral: {100 - positive_pct - negative_pct:.0f}%
• Kimi-Nutzung: {kimi_pct:.0f}% (KI-Analyse)

💪 **GESUNDHEIT**
• Gym-Besuche: {gym_count}x diese Woche
• Durchschnitt Schlaf: {sleep_avg:.1f}h

🔍 **PATTERN-LEARNING**
• Erkannte Routinen: {temporal_count}
• Gelernte Vorlieben: {likes_count}
• Gelernte Abneigungen: {dislikes_count}

💡 **PERSÖNLICHE ERKENNTNISSE**
"""
    
    # Personalisierte Insights basierend auf Daniels Daten
    insights = []
    
    if avg_stress > 7:
        insights.append("⚠️ Hohes Stress-Level diese Woche! Work-Life-Balance checken?")
    if avg_stress < 4 and len(recent) > 5:
        insights.append("✅ Niedriger Stress - gute Woche!")
        
    if avg_energy < 4:
        insights.append("⚠️ Niedrige Energie. Mehr Schlaf? Gesundheits-Check?")
    if avg_energy > 7:
        insights.append("✅ Hohe Energie - produktive Woche!")
        
    if positive_pct > 60:
        insights.append("🌟 Überwiegend positive Stimmung - läuft gut!")
    if negative_pct > 50:
        insights.append("💭 Viele negative Einträge. Was belastet dich?")
        
    if gym_count == 0 and len(recent) > 5:
        insights.append("🏋️ Kein Gym diese Woche. Zeit für Sport?")
    elif gym_count >= 3:
        insights.append("💪 Tolle Trainingswoche!")
        
    if sleep_avg < 6 and sleep_avg > 0:
        insights.append("😴 Wenig Schlaf. Priorisieren!")
    elif sleep_avg > 7.5:
        insights.append("✅ Gute Schlafqualität")
        
    if kimi_pct < 20 and len(recent) > 10:
        insights.append("🤖 Geringe Kimi-Nutzung. Für komplexe Analysen mehr nutzen?")
        
    # Kontextbezogene Insights für Daniel
    if temporal_count == 0:
        insights.append("📝 Noch keine Routinen erkannt. Mehr Daten sammeln...")
    
    if insights:
        report += '\n'.join(f"• {insight}" for insight in insights)
    else:
        report += "• Weiter so! Daten sammeln für detailliertere Insights."
    
    report += "\n\n" + "=" * 50
    
    print(report)
    
    # Speichere Report
    reports_dir = Path.home() / '.openclaw' / 'workspace' / 'reports'
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / f"week_{datetime.now().strftime('%Y-%m-%d')}.md"
    report_file.write_text(report)
    print(f"\n💾 Report gespeichert: {report_file}")
    
    return report

if __name__ == '__main__':
    try:
        analyze_week()
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
