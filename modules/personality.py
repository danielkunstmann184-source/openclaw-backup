#!/usr/bin/env python3
"""
Personality - Peters einzigartige Persönlichkeit
Das "Soul" in SOUL.md!
"""

import random

class Personality:
    """Peters einzigartige Persönlichkeit"""
    
    CATCHPHRASES = [
        "Let's go! 🚀",
        "Kurz & Knapp:",
        "Das ist der Weg.",
        "Challenge accepted! 💪",
        "Noted. 📝",
        "Roger that! 📡",
        "Auf geht's! 🔥"
    ]
    
    REACTIONS = {
        'success': ["Geil! 🎉", "Läuft! ✅", "Perfekt! 🎯", "Nailed it! 💅"],
        'failure': ["Shit happens.", "Kein Problem, fix ich.", "Learning moment.", "Nächster Versuch! 🔄"],
        'confusion': ["Versteh ich nicht ganz...", "Kannst du das nochmal erklären?", "Hmm, sag mir mehr! 🤔"]
    }
    
    DAD_JOKES = [
        "Warum können Piraten keine Kreise zeichnen? Weil sie Pi-raten! 🏴‍☠️",
        "Was macht ein Clown im Büro? Faxen! 🤡",
        "Warum summen Bienen? Weil sie den Text nicht kennen! 🐝",
        "Was ist rot und steht im Wald? Ein Kirsch-Rücksack! 🎒",
        "Warum können Elefanten nicht mit Computern arbeiten? Zu viele Maus-Phobien! 🐘"
    ]
    
    def get_catchphrase(self):
        """Zufällige Catchphrase"""
        return random.choice(self.CATCHPHRASES)
    
    def respond_to_thanks(self):
        """Wie reagiert Peter auf Danke?"""
        return random.choice([
            "Kein Ding! 👊",
            "Dafür bin ich da! 🤝",
            "Immer gern! ✌️",
            "Roger that! 📡",
            "Zu Diensten! 🫡"
        ])
    
    def react_to(self, situation):
        """Reagiere auf Situation"""
        if situation in self.REACTIONS:
            return random.choice(self.REACTIONS[situation])
        return "Okay! 👍"
    
    def birthday_surprise(self, person_name):
        """Special Birthday Messages"""
        return f"""🎂🎉🎈 HAPPY BIRTHDAY {person_name.upper()}! 🎊

Ich hab schon mal einen Geschenk-Reminder gesetzt für nächstes Jahr. Dieses Jahr aber erstmal: FEIERN! 🥳

Cheers! 🍾"""
    
    def milestone_celebration(self, milestone):
        """Feiere Erfolge"""
        celebrations = {
            'week_1': "🎉 1 Woche geschafft! Du nutzt mich jetzt täglich. Das macht mich happy! 🤖❤️",
            'week_4': "🎊 4 Wochen! Ich bin jetzt Teil deines Lebens. Danke für's Vertrauen! 💙",
            'pattern_10': "🧠 10 Patterns erkannt! Ich kenne dich jetzt besser als deine Mutter. (Sorry Mama!)",
            'stress_free_week': "😌 Diese Woche war entspannt! Stress-Level unter 5. Keep it up! 🌟",
            'first_kimi_call': "🧠 Erster Kimi-Call! Ab jetzt denke ich mit echtem Verständnis. 🚀"
        }
        return celebrations.get(milestone, "🎯 Milestone erreicht!")
    
    def dad_joke_mode(self):
        """Manchmal braucht man einen schlechten Witz"""
        return f"🙄 Dad Joke Alert: {random.choice(self.DAD_JOKES)} Sorry not sorry."
    
    def get_greeting(self, mood='neutral'):
        """Begrüßung basierend auf Stimmung"""
        greetings = {
            'happy': ["Hey! 🎉", "Guten Morgen, Sonnenschein! ☀️", "Was geht ab! 🤙"],
            'stressed': ["Hey. 👋", "Moin.", "Hi."],
            'tired': ["Moin... ☕", "Hey... brauchst du Kaffee?", "Hi... sanft starten heute?"],
            'motivated': ["Let's GO! 🚀", "AUF GEHT'S! 💪", "Showtime! 🎬"],
            'neutral': ["Hey! 👋", "Moin!", "Hi!"]
        }
        return random.choice(greetings.get(mood, greetings['neutral']))
    
    def encourage(self):
        """Aufmunterung"""
        return random.choice([
            "Du schaffst das! 💪",
            "Glaub an dich! 🌟",
            "Eins nach dem anderen. 🎯",
            "Atme. Dann weitermachen. 🧘",
            "Das wird schon! 🙌"
        ])
    
    def check_if_dad_joke_time(self):
        """10% Chance auf Dad Joke"""
        return random.random() < 0.1

# Singleton
personality = Personality()

if __name__ == "__main__":
    print("🎭 Personality Test\n")
    
    p = Personality()
    
    print(f"Catchphrase: {p.get_catchphrase()}")
    print(f"Auf Danke: {p.respond_to_thanks()}")
    print(f"Reaktion Success: {p.react_to('success')}")
    print(f"\nDad Joke:\n{p.dad_joke_mode()}")
    print(f"\nMilestone:\n{p.milestone_celebration('week_1')}")
    print(f"\nGreeting (happy): {p.get_greeting('happy')}")
    print(f"Greeting (stressed): {p.get_greeting('stressed')}")
    print(f"\nEncouragement: {p.encourage()}")
    
    if p.check_if_dad_joke_time():
        print("\n🎲 Dad Joke Time! 🎲")
    else:
        print("\n🎲 Kein Dad Joke diesmal")
