#!/usr/bin/env python3
"""
Kimi Helper - Wrapper für Moonshot Kimi 2.5 API
NUTZT REQUESTS (keine Installation nötig!)
"""

import requests
import json
import sys
from pathlib import Path

# Config laden
sys.path.insert(0, str(Path.home() / '.openclaw' / 'workspace'))
from config.kimi_config import KIMI_API_KEY, KIMI_BASE_URL, KIMI_MODEL

class KimiHelper:
    def __init__(self):
        self.api_key = KIMI_API_KEY
        self.base_url = KIMI_BASE_URL
        self.model = KIMI_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def ask(self, prompt, system_prompt=None, max_tokens=2000, temperature=0.7):
        """
        Stelle Kimi eine Frage via Requests
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request Error: {e}")
            return None
    
    def analyze_sentiment_advanced(self, message):
        """
        Nutze Kimi für ERWEITERTE Sentiment-Analyse
        """
        prompt = f'''Analysiere diese Nachricht auf Stimmung: "{message}"

Bewerte (0-10):
- Stress-Level
- Energie-Level
- Emotionaler Zustand

Antworte NUR in diesem JSON-Format:
{{
    "stress_level": 0-10,
    "energy_level": 0-10,
    "emotional_state": "happy/stressed/tired/motivated/frustrated/neutral",
    "reasoning": "kurze Begründung auf Deutsch",
    "confidence": 0-1
}}'''
        
        response = self.ask(
            prompt, 
            system_prompt="Du bist ein Experte für Stimmungsanalyse.",
            max_tokens=500
        )
        
        if not response:
            return self._fallback_sentiment()
        
        # Parse JSON
        try:
            import re
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response)
        except:
            return self._fallback_sentiment()
    
    def _fallback_sentiment(self):
        return {
            "stress_level": 5,
            "energy_level": 5,
            "emotional_state": "neutral",
            "reasoning": "API-Fallback",
            "confidence": 0.0
        }
    
    def extract_patterns(self, memory_texts):
        """
        Extrahiere Patterns aus Memory-Files
        """
        combined_text = "\n\n---\n\n".join(memory_texts)[:25000]
        
        prompt = f'''Analysiere diese Chat-Logs:

{combined_text}

Finde Muster in:
1. Zeitlichen Abläufen (Wochentage)
2. Vorlieben (was mag der User?)
3. Abneigungen (was nervt?)
4. Produktivität (wann ist er aktiv?)

JSON-Format:
{{
    "temporal_patterns": {{"Monday": ["..."], ...}},
    "likes": {{"food": [], "activities": []}},
    "dislikes": {{"times": [], "situations": []}},
    "productivity": {{"peak_hours": "...", "low_energy": "..."}},
    "insights": "..."
}}'''
        
        response = self.ask(
            prompt,
            system_prompt="Du bist ein Experte für Verhaltensanalyse.",
            max_tokens=3000
        )
        
        if not response:
            return {"error": "No response"}
        
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response)
        except Exception as e:
            return {
                "error": f"Parsing failed: {e}",
                "raw_response": response[:500]
            }
    
    def find_mentioned_people(self, memory_texts):
        """
        Finde alle erwähnten Personen
        """
        combined = " ".join(memory_texts)[:15000]
        
        prompt = f'''Aus diesem Text, liste alle erwähnten Personen auf:

{combined}

Nur echte Namen (Vor- oder Nachnamen). Keine Firmen/Orte.

JSON-Liste: ["Name1", "Name2"]'''
        
        response = self.ask(
            prompt,
            system_prompt="Du identifizierst Personen in Texten.",
            max_tokens=500
        )
        
        if not response:
            return []
        
        try:
            import re
            json_match = re.search(r'\[[^\]]*\]', response)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response)
        except:
            return []
    
    def analyze_person_from_memory(self, person_name, memory_texts):
        """
        Extrahiere Person-Profil aus Memory
        """
        combined = "\n".join(memory_texts)[:20000]
        
        prompt = f'''Finde alle Informationen über "{person_name}" in diesen Logs:

{combined}

JSON:
{{
    "name": "{person_name}",
    "relationship": "Freund/Kollege/Familie/Partner/...",
    "importance": 1-10,
    "communication_style": "...",
    "interests": {{"loves": [], "avoids": []}},
    "notes": "..."
}}'''
        
        response = self.ask(
            prompt,
            system_prompt="Du bist ein Experte für Beziehungsanalyse.",
            max_tokens=1500
        )
        
        if not response:
            return {"name": person_name, "error": "No response"}
        
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response)
        except:
            return {
                "name": person_name,
                "error": "Parsing failed",
                "raw": response[:500]
            }

# Singleton
kimi = KimiHelper()

if __name__ == "__main__":
    print("🧪 Kimi Helper Test\n")
    print("Testing API Connection...\n")
    
    response = kimi.ask("Hallo! Bist du bereit für den Digital Twin? Antworte kurz.")
    
    if response:
        print(f"✅ Kimi antwortet:\n{response}\n")
        
        # Test Sentiment
        print("🧠 Testing Sentiment Analysis...")
        test_msg = "Mein Chef hat mich wieder vollgemüllt mit Arbeit, ich kotze!"
        print(f"Nachricht: {test_msg}")
        sentiment = kimi.analyze_sentiment_advanced(test_msg)
        print(f"Ergebnis: {json.dumps(sentiment, indent=2, ensure_ascii=False)}\n")
        
        print("🎉 Kimi ist bereit für den Digital Twin!")
    else:
        print("❌ Keine Antwort von Kimi")
