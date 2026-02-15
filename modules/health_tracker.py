#!/usr/bin/env python3
"""
Health Tracker - Überwache Gesundheit & Balance
"""

from datetime import datetime, timedelta
import json
from pathlib import Path

class HealthTracker:
    def __init__(self):
        self.db_path = Path.home() / '.openclaw' / 'workspace' / 'data' / 'health.json'
        self.db_path.parent.mkdir(exist_ok=True)
        self.load_data()
    
    def load_data(self):
        if self.db_path.exists():
            with open(self.db_path) as f:
                self.data = json.load(f)
        else:
            self.data = {
                'gym_sessions': [],
                'sleep_quality': [],
                'meals': [],
                'work_hours': [],
                'created_at': datetime.now().isoformat()
            }
    
    def save_data(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_gym_session(self, duration_minutes=None, notes=""):
        """Logge Gym-Session"""
        entry = {
            'date': datetime.now().isoformat(),
            'duration': duration_minutes,
            'notes': notes
        }
        self.data['gym_sessions'].append(entry)
        self.save_data()
        return "💪 Gym-Session geloggt! Gut gemacht!"
    
    def log_sleep(self, hours, quality=5):
        """Logge Schlafdauer und Qualität"""
        entry = {
            'date': datetime.now().isoformat(),
            'hours': hours,
            'quality': quality  # 1-10
        }
        self.data['sleep_quality'].append(entry)
        self.save_data()
        
        feedback = ""
        if hours < 6:
            feedback = "⚠️ Wenig Schlaf! Heute früh ins Bett?"
        elif hours > 9:
            feedback = "😴 Viel geschlafen - fühlst du dich erholt?"
        else:
            feedback = "✅ Gute Schlafdauer!"
        
        return f"💤 {hours}h Schlaf geloggt. {feedback}"
    
    def days_since_last_gym(self):
        """Wie lange her war letztes Gym?"""
        if not self.data['gym_sessions']:
            return 999
        
        last = datetime.fromisoformat(self.data['gym_sessions'][-1]['date'])
        return (datetime.now() - last).days
    
    def get_last_sleep(self):
        """Holt den letzten Schlafeintrag"""
        if not self.data['sleep_quality']:
            return None
        return self.data['sleep_quality'][-1]
    
    def should_suggest_gym(self):
        """Sollte ich Gym vorschlagen?"""
        days = self.days_since_last_gym()
        
        # Nach 3 Tagen: Sanfter Hinweis
        if days == 3:
            return (True, "Du warst 3 Tage nicht im Gym. Heute Zeit für Bewegung? 🏃")
        
        # Nach 5 Tagen: Direkter
        elif days >= 5:
            return (True, f"⚠️ {days} Tage kein Training! Zeit für Sport!")
        
        return (False, None)
    
    def check_sleep_quality(self):
        """Prüfe ob genug geschlafen wurde"""
        last_sleep = self.get_last_sleep()
        if not last_sleep:
            return (False, None)
        
        hours = last_sleep['hours']
        
        if hours < 6:
            return (True, "💤 Wenig Schlaf gestern. Heute früh ins Bett denken?")
        
        return (False, None)
    
    def log_work_hours(self, hours, date=None):
        """Logge Arbeitsstunden für einen Tag"""
        if date is None:
            date = datetime.now()
        
        entry = {
            'date': date.isoformat(),
            'hours': hours
        }
        self.data['work_hours'].append(entry)
        self.save_data()
    
    def get_weekly_work_hours(self, week_offset=0):
        """Berechne Arbeitsstunden dieser Woche"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday() + (week_offset * 7))
        week_end = week_start + timedelta(days=7)
        
        total_hours = 0
        for entry in self.data['work_hours']:
            entry_date = datetime.fromisoformat(entry['date'])
            if week_start <= entry_date < week_end:
                total_hours += entry['hours']
        
        return total_hours
    
    def check_work_life_balance(self):
        """Ist die Balance okay?"""
        hours = self.get_weekly_work_hours()
        
        if hours > 50:
            return {
                'status': 'overworked',
                'hours': hours,
                'message': f"⚠️ {hours}h diese Woche - das ist zu viel! Zeit für Pausen?"
            }
        elif hours > 45:
            return {
                'status': 'busy',
                'hours': hours,
                'message': f"Busy week ({hours}h). Gönn dir am Wochenende Zeit für dich!"
            }
        else:
            return {
                'status': 'balanced',
                'hours': hours,
                'message': f"Work-Life-Balance sieht gut aus ({hours}h). 👍"
            }
    
    def get_health_summary(self):
        """Gibt eine Gesundheits-Zusammenfassung"""
        summary = "🏥 **Gesundheits-Status**\n\n"
        
        # Gym
        days_gym = self.days_since_last_gym()
        if days_gym == 0:
            summary += "💪 Heute warst du trainieren!\n"
        elif days_gym < 3:
            summary += f"💪 Letztes Training: {days_gym} Tage her\n"
        elif days_gym < 7:
            summary += f"⚠️ Letztes Training: {days_gym} Tage her\n"
        else:
            summary += f"🚨 Letztes Training: {days_gym} Tage her - Zeit für Sport!\n"
        
        # Schlaf
        last_sleep = self.get_last_sleep()
        if last_sleep:
            summary += f"💤 Letzter Schlaf: {last_sleep['hours']}h (Qualität: {last_sleep['quality']}/10)\n"
        
        # Work-Life
        balance = self.check_work_life_balance()
        summary += f"\n📊 {balance['message']}\n"
        
        return summary
    
    def get_health_suggestions(self):
        """Gibt gesundheits-basierte Vorschläge"""
        suggestions = []
        
        # Gym-Vorschlag
        should_gym, gym_msg = self.should_suggest_gym()
        if should_gym:
            suggestions.append({
                'type': 'gym',
                'message': gym_msg,
                'priority': 7 if self.days_since_last_gym() >= 5 else 5
            })
        
        # Schlaf-Vorschlag
        should_sleep, sleep_msg = self.check_sleep_quality()
        if should_sleep:
            suggestions.append({
                'type': 'sleep',
                'message': sleep_msg,
                'priority': 6
            })
        
        # Work-Life
        balance = self.check_work_life_balance()
        if balance['status'] == 'overworked':
            suggestions.append({
                'type': 'work_life',
                'message': balance['message'],
                'priority': 8
            })
        
        # Sortiere nach Priorität
        suggestions.sort(key=lambda x: x['priority'], reverse=True)
        return suggestions

# Singleton
health_tracker = HealthTracker()

if __name__ == "__main__":
    # Test
    print("🧪 Health Tracker Test\n")
    
    ht = HealthTracker()
    
    print("🏥 Gesundheits-Summary:")
    print(ht.get_health_summary())
    
    print("\n💡 Gesundheits-Vorschläge:")
    for sugg in ht.get_health_suggestions():
        print(f"• [{sugg['priority']}/10] {sugg['message']}")
