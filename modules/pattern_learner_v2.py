#!/usr/bin/env python3
"""
Pattern Learner V2 - Mit Kimi ist ALLES möglich!
Extrahiert automatisch Muster aus Memory-Dateien
"""

from pathlib import Path
from datetime import datetime, timedelta
import json
import sys

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))
from modules.kimi_helper import kimi

class PatternLearnerV2:
    def __init__(self):
        self.memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
        self.patterns_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'learned_patterns_v2.json'
        self.patterns_file.parent.mkdir(exist_ok=True)
        self.memory_file = Path.home() / '.openclaw' / 'workspace' / 'MEMORY.md'
    
    def weekly_analysis(self, days=14):
        """
        VOLLE Power-Analyse mit Kimi!
        DAS WAR VORHER "BLOCKIERT" - JETZT NICHT MEHR!
        
        Returns: dict mit allen erkannten Patterns
        """
        print("🔍 Sammle Memory-Files...")
        
        # Sammle letzte N Tage
        memory_texts = []
        dates_collected = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            file_path = self.memory_dir / f"{date.strftime('%Y-%m-%d')}.md"
            
            if file_path.exists():
                content = file_path.read_text()
                # Füge Datum als Kontext hinzu
                header = f"=== {date.strftime('%A, %Y-%m-%d')} ===\n"
                memory_texts.append(header + content)
                dates_collected.append(date.strftime('%Y-%m-%d'))
        
        if not memory_texts:
            print("⚠️ Keine Memory-Files gefunden")
            return {}
        
        print(f"✅ {len(memory_texts)} Tage gefunden: {', '.join(dates_collected[:5])}...")
        print("🧠 Frage Kimi nach Patterns... (das kann 10-20 Sekunden dauern)")
        
        # NUTZE KIMI!
        patterns = kimi.extract_patterns(memory_texts)
        
        if 'error' in patterns:
            print(f"❌ Fehler: {patterns['error']}")
            return patterns
        
        print("✅ Patterns erkannt!")
        
        # Speichere
        result = {
            'analyzed_at': datetime.now().isoformat(),
            'days_analyzed': len(memory_texts),
            'dates': dates_collected,
            'patterns': patterns
        }
        
        with open(self.patterns_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Update MEMORY.md
        self._update_memory_file(patterns)
        
        return result
    
    def _update_memory_file(self, patterns):
        """Schreibe Patterns in MEMORY.md"""
        section = f"""## 🤖 Auto-Erkenntnisse (KI-Analyse vom {datetime.now().strftime('%Y-%m-%d')})

*Diese Patterns wurden automatisch von Kimi aus deinen letzten Tagen extrahiert.*

"""
        
        # Zeitliche Patterns
        if 'temporal_patterns' in patterns and patterns['temporal_patterns']:
            section += "### 📅 Zeitliche Muster:\n"
            for day, activities in patterns['temporal_patterns'].items():
                if activities:
                    section += f"- **{day}**: {', '.join(activities[:3])}\n"
            section += "\n"
        
        # Vorlieben
        if 'likes' in patterns and patterns['likes']:
            section += "### ❤️ Vorlieben:\n"
            for category, items in patterns['likes'].items():
                if items:
                    section += f"- **{category}**: {', '.join(items[:5])}\n"
            section += "\n"
        
        # Abneigungen
        if 'dislikes' in patterns and patterns['dislikes']:
            section += "### ⚠️ Abneigungen:\n"
            for category, items in patterns['dislikes'].items():
                if items:
                    section += f"- **{category}**: {', '.join(items[:5])}\n"
            section += "\n"
        
        # Produktivität
        if 'productivity' in patterns and patterns['productivity']:
            section += "### ⚡ Produktivitätsmuster:\n"
            prod = patterns['productivity']
            if 'peak_hours' in prod:
                section += f"- **Beste Zeit**: {prod['peak_hours']}\n"
            if 'low_energy' in prod:
                section += f"- **Niedrige Energie**: {prod['low_energy']}\n"
            if 'productive_days' in prod:
                section += f"- **Produktive Tage**: {', '.join(prod['productive_days'])}\n"
            section += "\n"
        
        # Insights
        if 'insights' in patterns and patterns['insights']:
            section += f"### 💡 Erkenntnis:\n{patterns['insights']}\n\n"
        
        # Lese aktuelle MEMORY.md
        if self.memory_file.exists():
            content = self.memory_file.read_text()
        else:
            content = "# MEMORY.md\n\n"
        
        # Ersetze alte Auto-Erkenntnisse oder append
        import re
        if '## 🤖 Auto-Erkenntnisse' in content:
            content = re.sub(
                r'## 🤖 Auto-Erkenntnisse.*?(?=## |\Z)',
                section,
                content,
                flags=re.DOTALL
            )
        else:
            content += "\n" + section
        
        self.memory_file.write_text(content)
        print("✅ MEMORY.md aktualisiert mit neuen Erkenntnissen")
    
    def get_patterns_summary(self):
        """Gibt Zusammenfassung der gelernten Patterns"""
        if not self.patterns_file.exists():
            return "Noch keine Patterns gelernt. Führe weekly_analysis() aus."
        
        with open(self.patterns_file) as f:
            data = json.load(f)
        
        summary = f"📊 Patterns (Stand: {data['analyzed_at'][:10]})\n"
        summary += f"Analysierte Tage: {data['days_analyzed']}\n\n"
        
        patterns = data.get('patterns', {})
        
        if 'likes' in patterns:
            summary += "❤️ Vorlieben erkannt\n"
        if 'temporal_patterns' in patterns:
            summary += "📅 Zeitliche Muster erkannt\n"
        if 'productivity' in patterns:
            summary += "⚡ Produktivitätsmuster erkannt\n"
        
        return summary
    
    def quick_analysis(self, days=7):
        """Schnelle Analyse für weniger Tage (für Tests)"""
        return self.weekly_analysis(days=days)

# Singleton
pattern_learner_v2 = PatternLearnerV2()

if __name__ == "__main__":
    print("🧠 Pattern Learner V2 - MIT KIMI POWER!\n")
    
    learner = PatternLearnerV2()
    
    # Schneller Test mit 7 Tagen
    print("Starte Analyse der letzten 7 Tage...\n")
    result = learner.quick_analysis(days=7)
    
    if result and 'patterns' in result:
        print("\n🎉 Erfolg! Gefundene Patterns:")
        patterns = result['patterns']
        
        if 'likes' in patterns:
            print("\n❤️ Likes:")
            for cat, items in patterns['likes'].items():
                print(f"  {cat}: {', '.join(items[:3])}")
        
        if 'insights' in patterns:
            print(f"\n💡 Insight: {patterns['insights'][:200]}")
    else:
        print("❌ Keine Patterns gefunden oder Fehler aufgetreten")
