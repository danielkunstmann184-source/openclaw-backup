#!/usr/bin/env python3
"""
Predictor - Antizipiere Bedürfnisse basierend auf Patterns und MEMORY.md
"""

from datetime import datetime, timedelta
import re
from pathlib import Path

class Predictor:
    def __init__(self):
        self.memory_path = Path.home() / '.openclaw' / 'workspace' / 'MEMORY.md'
        self.memory_dir = Path.home() / '.openclaw' / 'workspace' / 'memory'
        self.user_path = Path.home() / '.openclaw' / 'workspace' / 'USER.md'
    
    def predict_tomorrow_needs(self):
        """
        Was wird der User morgen brauchen?
        
        Returns: list von Predictions mit Aktionen
        """
        predictions = []
        tomorrow = datetime.now() + timedelta(days=1)
        
        # 1. Analysiere morgigen Kalender (aus MEMORY.md)
        tomorrow_events = self.get_tomorrow_calendar()
        for event in tomorrow_events:
            # Wichtiges Meeting?
            if self.is_important_meeting(event):
                predictions.append({
                    'type': 'meeting_prep',
                    'priority': 8,
                    'event': event,
                    'actions': [
                        'Sammle Infos über Teilnehmer',
                        'Checke relevante Dokumente',
                        'Erstelle Agenda-Vorschlag'
                    ],
                    'message': f"📅 Morgen wichtig: {event['title']} um {event['time']}. Soll ich vorbereiten?"
                })
            
            # Früher Termin?
            if self.is_early_event(event):
                predictions.append({
                    'type': 'early_alarm',
                    'priority': 7,
                    'event': event,
                    'message': f"⏰ Dein erster Termin ist um {event['time']} - früher als sonst. Wecker ok?"
                })
        
        # 2. Wiederkehrende Aufgaben
        recurring = self.check_recurring_tasks(tomorrow)
        predictions.extend(recurring)
        
        # 3. Wetter-basierte Predictions
        weather_pred = self.predict_weather_needs()
        if weather_pred:
            predictions.append(weather_pred)
        
        # 4. Social Predictions
        social_pred = self.predict_social_needs(tomorrow)
        predictions.extend(social_pred)
        
        # Sortiere nach Priorität
        predictions.sort(key=lambda x: x['priority'], reverse=True)
        return predictions
    
    def get_tomorrow_calendar(self):
        """
        Parse MEMORY.md für morgige Termine
        Returns: list von Events für morgen
        """
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        
        events = []
        
        # Prüfe ob es eine Datei für morgen gibt
        tomorrow_file = self.memory_dir / f"{tomorrow_str}.md"
        if tomorrow_file.exists():
            content = tomorrow_file.read_text()
            # Suche nach Terminen (einfache Pattern)
            # Format: "## Termine" oder "- 09:00: Meeting"
            for line in content.split('\n'):
                # Pattern: "- HH:MM: Titel" oder "- 9:00 Termin"
                match = re.match(r'.*?(\d{1,2}):(\d{2})\s*[:\-]?\s*(.+)', line)
                if match:
                    hour, minute, title = match.groups()
                    events.append({
                        'title': title.strip(),
                        'time': f"{hour.zfill(2)}:{minute}",
                        'importance': 5  # Default
                    })
        
        return events
    
    def is_important_meeting(self, event):
        """Ist dieses Meeting wichtig?"""
        keywords = ['mitglied', 'kunde', 'termin', 'wichtig', 'chef', 'ceo', 'präsentation', 'interview']
        title_lower = event['title'].lower()
        return (
            any(kw in title_lower for kw in keywords) or
            event.get('importance', 0) > 7
        )
    
    def is_early_event(self, event):
        """Ist das früher als üblich?"""
        try:
            event_hour = int(event['time'].split(':')[0])
            usual_start = 9  # TODO: Lerne aus MEMORY.md
            return event_hour < usual_start
        except:
            return False
    
    def check_recurring_tasks(self, date=None):
        """
        Checke ob an einem Tag wiederkehrende Aufgaben anfallen
        """
        if date is None:
            date = datetime.now() + timedelta(days=1)
        
        day_of_week = date.strftime('%A')
        day_of_month = date.day
        weekday_de = {
            'Monday': 'Montag',
            'Tuesday': 'Dienstag',
            'Wednesday': 'Mittwoch',
            'Thursday': 'Donnerstag',
            'Friday': 'Freitag',
            'Saturday': 'Samstag',
            'Sunday': 'Sonntag'
        }
        day_de = weekday_de.get(day_of_week, day_of_week)
        
        predictions = []
        
        # Montag: Wochenstart
        if day_of_week == 'Monday':
            predictions.append({
                'type': 'recurring_task',
                'priority': 6,
                'message': "📊 Morgen ist Montag - Zeit für Wochenplanung!"
            })
        
        # Freitag: Wochenabschluss
        if day_of_week == 'Friday':
            predictions.append({
                'type': 'recurring_task',
                'priority': 5,
                'message': "🎉 Morgen ist Freitag - Wochenabschluss nicht vergessen!"
            })
        
        # Monatliche Tasks
        if day_of_month == 1:
            predictions.append({
                'type': 'recurring_task',
                'priority': 8,
                'message': "📅 Morgen ist der 1. - Neuer Monat, neue Ziele!"
            })
        
        # Wenn 14 Tage vor Monatsende (für Deadlines)
        if day_of_month >= 15:
            predictions.append({
                'type': 'deadline_warning',
                'priority': 4,
                'message': f"⏰ Nur noch {30 - day_of_month} Tage im Monat - offene Deadlines?"
            })
        
        return predictions
    
    def predict_weather_needs(self):
        """
        Basierend auf morgen's Wetter, was braucht User?
        """
        # TODO: Implementiere Weather-API Integration
        # Für jetzt: Platzhalter
        
        # Wir könnten hier die OpenWeather API nutzen
        # Aber das macht der Wetter-Cron schon
        
        return None
    
    def predict_social_needs(self, date=None):
        """
        Steht ein Geburtstag an? Wichtiger Social-Event?
        """
        if date is None:
            date = datetime.now() + timedelta(days=1)
        
        predictions = []
        
        # Prüfe PEOPLE.md (falls existiert)
        people_file = Path.home() / '.openclaw' / 'workspace' / 'PEOPLE.md'
        if people_file.exists():
            content = people_file.read_text()
            
            # Suche nach Geburtstagen
            # Pattern: "**Geburtstag**: 12. Juni" oder ähnlich
            birthday_pattern = r'\*\*Geburtstag\*\*:\s*(\d{1,2})\.\s*(\w+)'
            matches = re.findall(birthday_pattern, content)
            
            for day, month in matches:
                # Konvertiere Monatsnamen zu Nummer
                month_map = {
                    'januar': 1, 'februar': 2, 'märz': 3, 'april': 4,
                    'mai': 5, 'juni': 6, 'juli': 7, 'august': 8,
                    'september': 9, 'oktober': 10, 'november': 11, 'dezember': 12
                }
                month_num = month_map.get(month.lower(), 0)
                
                if month_num == date.month and int(day) == date.day:
                    # Extrahiere Name (Zeile vor Geburtstag)
                    predictions.append({
                        'type': 'birthday_reminder',
                        'priority': 9,
                        'message': f"🎂 Morgen hat jemand Geburtstag! Gratulieren nicht vergessen."
                    })
        
        return predictions
    
    def predict_cognitive_load(self, date=None):
        """
        Wie anstrengend wird der Tag?
        
        Returns: dict mit load (0-10) und recommendation
        """
        if date is None:
            date = datetime.now() + timedelta(days=1)
        
        events = self.get_tomorrow_calendar()
        load = 0
        
        for event in events:
            # Meetings sind anstrengend
            if any(word in event['title'].lower() for word in ['meeting', 'termin', 'gespräch', 'call']):
                load += 2
            
            # Präsentationen besonders
            if any(word in event['title'].lower() for word in ['präsentation', 'präsi', 'vortrag']):
                load += 5
            
            # Viele Teilnehmer = anstrengend
            if len(event.get('participants', [])) > 5:
                load += 2
        
        # Empfehlung
        if load > 10:
            recommendation = "⚠️ Morgen wird heavy! Plane Pausen ein und geh früh schlafen."
        elif load > 7:
            recommendation = "Morgen wird anstrengend. Genug Schlaf!"
        elif load > 4:
            recommendation = "Normaler Tag morgen. Alles gut!"
        else:
            recommendation = "Entspannter Tag morgen. Zeit für eigene Projekte?"
        
        return {
            'load': min(load, 10),
            'recommendation': recommendation
        }
    
    def generate_evening_briefing(self):
        """
        Erstelle Abend-Briefing mit Predictions für morgen
        """
        # 1. Hole Predictions
        predictions = self.predict_tomorrow_needs()
        
        # 2. Cognitive Load
        cognitive = self.predict_cognitive_load()
        
        # 3. Baue Briefing zusammen
        briefing = "🌙 **Guten Abend!**\n\n"
        
        if predictions:
            briefing += "📋 **Morgen auf dem Plan:**\n"
            for pred in predictions[:3]:  # Top 3
                briefing += f"• {pred['message']}\n"
            briefing += "\n"
        
        briefing += f"🧠 **Cognitive Load:** {cognitive['load']}/10\n"
        briefing += f"{cognitive['recommendation']}\n\n"
        
        # Optional: Vorbereitung anbieten
        if predictions and predictions[0]['priority'] > 7:
            briefing += "💡 Soll ich heute Abend schon vorbereiten?"
        
        return briefing
    
    def get_contextual_suggestions(self):
        """
        Kontext-basierte Vorschläge basierend auf aktueller Situation
        """
        suggestions = []
        now = datetime.now()
        
        # Zeit-basierte Suggestions
        hour = now.hour
        
        if 6 <= hour < 9:
            suggestions.append({
                'type': 'morning_routine',
                'message': 'Guten Morgen! Zeit für den Tagesplan?',
                'priority': 5
            })
        elif 11 <= hour < 13:
            suggestions.append({
                'type': 'lunch_reminder',
                'message': 'Mahlzeit! Zeit für eine Pause?',
                'priority': 3
            })
        elif 17 <= hour < 19:
            suggestions.append({
                'type': 'evening_winddown',
                'message': 'Feierabend naht! Noch offene Tasks?',
                'priority': 4
            })
        elif 21 <= hour < 23:
            suggestions.append({
                'type': 'bedtime_prep',
                'message': 'Bald Schlafenszeit. Morgen vorbereiten?',
                'priority': 5
            })
        
        return suggestions

# Singleton
predictor = Predictor()

if __name__ == "__main__":
    # Test
    print("🧪 Predictor Test\n")
    
    p = Predictor()
    
    print("📊 Evening Briefing:")
    print(p.generate_evening_briefing())
    
    print("\n📈 Cognitive Load morgen:")
    cognitive = p.predict_cognitive_load()
    print(f"Load: {cognitive['load']}/10")
    print(f"Empfehlung: {cognitive['recommendation']}")
    
    print("\n💡 Contextual Suggestions:")
    for sugg in p.get_contextual_suggestions():
        print(f"• {sugg['message']}")
