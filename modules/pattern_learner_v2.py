#!/usr/bin/env python3
"""
Pattern Learner V2 - ROBUST MIT FALLBACK
Nutzt Kimi wenn verfügbar, sonst einfache Regex-Patterns
"""

from pathlib import Path
from datetime import datetime, timedelta
import json
import re
import sys

sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))

# Versuche Kimi zu importieren
try:
    from config.kimi_config import KIMI_API_KEY, USE_KIMI_FALLBACK
    from modules.kimi_helper import kimi
    KIMI_AVAILABLE = bool(KIMI_API_KEY and len(KIMI_API_KEY) > 20)
except:
    KIMI_AVAILABLE = False

class PatternLearnerV2:
    def __init__(self):
        self.memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
        self.patterns_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'learned_patterns_v2.json'
        self.patterns_file.parent.mkdir(exist_ok=True)
        self.memory_file = Path.home() / '.openclaw' / 'workspace' / 'MEMORY.md'
    
    def weekly_analysis(self, days=14):
        """
        Pattern-Analyse - mit Kimi oder Fallback
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
                header = f"=== {date.strftime('%A, %Y-%m-%d')} ===\n"
                memory_texts.append(header + content)
                dates_collected.append(date.strftime('%Y-%m-%d'))
        
        if not memory_texts:
            print("⚠️ Keine Memory-Files gefunden")
            return {}
        
        print(f"✅ {len(memory_texts)} Tage gefunden")
        
        # Versuche Kimi (wenn verfügbar)
        if KIMI_AVAILABLE and USE_KIMI_FALLBACK:
            try:
                print("🧠 Nutze Kimi für Pattern-Analyse...")
                patterns = self._analyze_with_kimi(memory_texts)
                method = 'kimi'
            except Exception as e:
                print(f"⚠️ Kimi failed ({e}), nutze Fallback...")
                patterns = self._analyze_with_fallback(memory_texts)
                method = 'fallback'
        else:
            print("📝 Nutze einfache Pattern-Analyse...")
            patterns = self._analyze_with_fallback(memory_texts)
            method = 'fallback'
        
        # Speichere
        result = {
            'analyzed_at': datetime.now().isoformat(),
            'days_analyzed': len(memory_texts),
            'dates': dates_collected,
            'method': method,
            'patterns': patterns
        }
        
        with open(self.patterns_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    
    def _analyze_with_kimi(self, memory_texts):
        """Nutze Kimi für komplexe Pattern-Analyse"""
        combined_text = "\n\n".join(memory_texts[:7])  # Max 7 Tage für Kimi
        
        prompt = f"""Analysiere diese Tagebücher und extrahiere Muster:

{combined_text[:8000]}  # Limit für Kimi

Extrahiere:
1. Zeitliche Muster (welche Aktivitäten an welchen Tagen?)
2. Vorlieben (was mag die Person?)
3. Abneigungen (was nervt?)
4. Routinen (regelmäßige Aktivitäten)

Antworte als JSON:
{{
  "temporal_patterns": {{"Montag": ["Aktivität1"], ...}},
  "likes": {{"food": ["Pizza"], "activities": ["Sport"]}},
  "dislikes": {{"food": [], "situations": []}},
  "routines": ["routine1", "routine2"]
}}"""
        
        try:
            response = kimi.ask(prompt, max_tokens=1500)
            # Versuche JSON zu parsen
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback wenn Kimi-Antwort ungültig
        return self._analyze_with_fallback(memory_texts)
    
    def _analyze_with_fallback(self, memory_texts):
        """Einfache Regex-basierte Pattern-Analyse"""
        combined_text = "\n".join(memory_texts).lower()
        
        patterns = {
            'temporal_patterns': {},
            'likes': {
                'food': [],
                'activities': [],
                'people': []
            },
            'dislikes': {
                'situations': [],
                'activities': []
            },
            'routines': []
        }
        
        # Wochentage erkennen
        days = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag']
        for day in days:
            day_activities = []
            # Suche nach "Day: Aktivität" oder "Day → Aktivität"
            day_pattern = rf'(?:{day}|{day.capitalize()}).{{0,50}}?(?:→|:)\s*(\w+)'
            matches = re.findall(day_pattern, combined_text)
            if matches:
                patterns['temporal_patterns'][day.capitalize()] = list(set(matches))[:3]
        
        # Vorlieben erkennen
        like_patterns = {
            'food': ['pizza', 'pasta', 'burger', 'sushi', 'kaffee', 'tee'],
            'activities': ['sport', 'gym', 'laufen', 'lesen', 'musik', 'kochen'],
            'people': ['juliane', 'juli', 'fin', 'jonas', 'michael']
        }
        
        for category, items in like_patterns.items():
            for item in items:
                if item in combined_text:
                    patterns['likes'][category].append(item)
        
        # Routinen erkennen
        routine_keywords = ['jeden tag', 'täglich', 'immer', 'regelmäßig', 'routine']
        for keyword in routine_keywords:
            if keyword in combined_text:
                # Extrahiere Satz mit Routine
                sentences = combined_text.split('.')
                for sent in sentences:
                    if keyword in sent and len(sent) > 10:
                        patterns['routines'].append(sent.strip()[:100])
                        break
        
        # Duplikate entfernen
        patterns['routines'] = list(set(patterns['routines']))[:5]
        
        return patterns
    
    def get_patterns(self):
        """Holt gespeicherte Patterns"""
        if self.patterns_file.exists():
            with open(self.patterns_file) as f:
                return json.load(f)
        return {}
    
    def suggest_based_on_patterns(self, day_of_week=None):
        """Gibt Vorschläge basierend auf gelernten Patterns"""
        patterns = self.get_patterns()
        
        if not patterns or 'patterns' not in patterns:
            return None
        
        p = patterns['patterns']
        suggestions = []
        
        # Zeitbasierte Vorschläge
        if day_of_week and 'temporal_patterns' in p:
            day_patterns = p['temporal_patterns'].get(day_of_week, [])
            if day_patterns:
                suggestions.append(f"📅 Normalerweise am {day_of_week}: {', '.join(day_patterns[:3])}")
        
        # Vorlieben
        if 'likes' in p and p['likes'].get('activities'):
            acts = p['likes']['activities'][:3]
            suggestions.append(f"❤️ Du magst: {', '.join(acts)}")
        
        return suggestions

# Singleton
learner = PatternLearnerV2()

if __name__ == "__main__":
    print("🧪 Pattern Learner V2 Test\n")
    print(f"Kimi verfügbar: {KIMI_AVAILABLE}\n")
    
    result = learner.weekly_analysis(days=7)
    
    if result:
        print(f"\n✅ Analyse complete!")
        print(f"Methode: {result.get('method', 'unknown')}")
        print(f"Tage analysiert: {result.get('days_analyzed', 0)}")
        
        patterns = result.get('patterns', {})
        if 'temporal_patterns' in patterns:
            print(f"Zeitliche Patterns: {len(patterns['temporal_patterns'])}")
        if 'likes' in patterns:
            print(f"Vorlieben erkannt: {sum(len(v) for v in patterns['likes'].values())}")
