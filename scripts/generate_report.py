#!/usr/bin/env python3
"""
Performance Report - Wie gut bin ich?
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

def analyze_week():
    """Analysiere letzte Woche"""
    
    # 1. Sentiment-Stats
    sentiment_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'sentiment_v2.json'
    
    if sentiment_file.exists():
        with open(sentiment_file) as f:
            history = json.load(f)
        
        # Letzte 7 Tage
        week_ago = datetime.now() - timedelta(days=7)
        recent = [
            h for h in history 
            if datetime.fromisoformat(h['timestamp']) > week_ago
        ]
        
        if recent:
            avg_stress = sum(h['stress_level'] for h in recent) / len(recent)
            avg_energy = sum(h['energy_level'] for h in recent) / len(recent)
            
            # Stimmungs-Verteilung
            sentiments = [h['sentiment'] for h in recent]
            positive_pct = (sentiments.count('positive') / len(sentiments)) * 100
            negative_pct = (sentiments.count('negative') / len(sentiments)) * 100
            
            # Wie oft nutzte ich Kimi vs. Simple?
            kimi_usage = sum(1 for h in recent if h.get('method') == 'kimi')
            kimi_pct = (kimi_usage / len(recent)) * 100
        else:
            avg_stress = 0
            avg_energy = 0
            positive_pct = 0
            negative_pct = 0
            kimi_pct = 0
    else:
        print("⚠️ Keine Sentiment-Daten")
        recent = []
        avg_stress = 0
        avg_energy = 0
        positive_pct = 0
        negative_pct = 0
        kimi_pct = 0
    
    # 2. Pattern-Stats
    patterns_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'learned_patterns_v2.json'
    
    if patterns_file.exists():
        with open(patterns_file) as f:
            data = json.load(f)
        patterns = data.get('patterns', {})
        temporal_count = len(patterns.get('temporal_patterns', {}))
        likes_count = sum(len(v) for v in patterns.get('likes', {}).values())
        dislikes_count = sum(len(v) for v in patterns.get('dislikes', {}).values())
    else:
        temporal_count = 0
        likes_count = 0
        dislikes_count = 0
    
    # 3. Generiere Report
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
• Kimi-Nutzung: {kimi_pct:.0f}% (Rest: Simple-Analyse)

🔍 **PATTERN-LEARNING**
• Zeitliche Patterns: {temporal_count}
• Erkannte Vorlieben: {likes_count}
• Erkannte Abneigungen: {dislikes_count}

💡 **ERKENNTNISSE**
"""
    
    # Insights basierend auf Daten
    if avg_stress > 7:
        report += "⚠️ Hohes Stress-Level diese Woche! Work-Life-Balance checken?\n"
    if avg_energy < 4:
        report += "⚠️ Niedrige Energie. Mehr Schlaf? Gesundheits-Check?\n"
    if positive_pct > 60:
        report += "✅ Überwiegend positive Stimmung - läuft gut!\n"
    if kimi_pct < 30 and len(recent) > 10:
        report += "💡 Wenig Kimi-Nutzung. Evtl. Threshold senken für bessere Analyse?\n"
    
    report += "\n" + "=" * 50
    
    print(report)
    
    # Speichere Report
    report_file = Path.home() / '.openclaw' / 'workspace' / 'reports' / f"week_{datetime.now().strftime('%Y-%m-%d')}.md"
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text(report)
    
    return report

if __name__ == '__main__':
    analyze_week()
