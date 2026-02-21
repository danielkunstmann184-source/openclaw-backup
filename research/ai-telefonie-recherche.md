# KI-Telefonie / Voice-Chat mit AI-Agenten - Recherche

**Recherche-Datum:** 2026-02-21

---

## Übersicht: Open-Source Lösungen für KI-Telefonie

| Projekt | Stars | Sprache | Fokus | Telefonie |
|---------|-------|---------|-------|-----------|
| **Pipecat** | 10.4k | Python | Framework | Twilio, Daily, WebSocket |
| **Bolna** | 578 | Python | End-to-End | Twilio, Plivo |
| **Vocode** | ~2k | Python | Framework | Twilio, Zoom |
| **Chanakya** | 167 | JavaScript | Lokaler Assistant | - |
| **Fritz AI Assistant** | 9 | Python | FritzBox-Integration | SIP/Asterisk |

---

## 1. Frameworks & Orchestrierung

### 1.1 Pipecat (Daily.co) ⭐ Empfohlen
- **GitHub:** https://github.com/pipecat-ai/pipecat
- **Stars:** 10.4k
- **Sprache:** Python
- **Beschreibung:** Open-Source Framework für Voice & Multimodal AI Agents

**Features:**
- Modularer Pipeline-Ansatz (STT → LLM → TTS)
- Unterstützt 20+ STT Provider (Deepgram, Whisper, Azure, etc.)
- Unterstützt 20+ LLM Provider (OpenAI, Anthropic, Ollama, etc.)
- Unterstützt 20+ TTS Provider (ElevenLabs, Piper, Azure, etc.)
- Telefonie: Twilio, Daily (WebRTC), WebSocket Server
- Client SDKs: JavaScript, React, React Native, Swift, Kotlin

**Self-hosted Möglichkeiten:**
- ✅ Vollständig lokal mit Ollama + Piper + Whisper
- ✅ Docker-Support
- ⚠️ Für Telefonie braucht man Twilio/Daily API-Keys

**Kosten:**
- Framework: Kostenlos (Open Source)
- Telefonie: Twilio ($0.0085/min), Daily (kostenlos für Dev)
- API-Kosten: Je nach gewählten Providern

**Setup-Komplexität:** Mittel (Docker verfügbar)

---

### 1.2 Bolna
- **GitHub:** https://github.com/bolna-ai/bolna
- **Stars:** 578
- **Sprache:** Python
- **Beschreibung:** End-to-end Open-Source Voice Agents Plattform

**Features:**
- JSON-basierte Agent-Konfiguration
- Telefonie: Twilio, Plivo, Exotel (coming), Vonage (coming)
- STT: Deepgram, Azure
- LLM: OpenAI, DeepSeek, Llama, Cohere, Mistral (via LiteLLM)
- TTS: AWS Polly, ElevenLabs, Deepgram, OpenAI, Azure, Cartesia
- Redis für Persistenz

**Self-hosted Möglichkeiten:**
- ✅ Docker Compose Setup verfügbar
- ✅ Unterstützt lokale LLMs via LiteLLM/Ollama
- ⚠️ Telefonie-Provider benötigen API-Keys

**Kosten:**
- Framework: Kostenlos
- Telefonie: Twilio/Plivo Gebühren
- API-Kosten: Variable

**Setup-Komplexität:** Mittel (Docker Compose)

---

### 1.3 Vocode (vocode-core)
- **GitHub:** https://github.com/vocodedev/vocode-core
- **Sprache:** Python
- **Beschreibung:** Build voice-based LLM apps in minutes

**Features:**
- Real-time Streaming Conversations
- Telefonie: Twilio, Zoom Dial-in
- STT: AssemblyAI, Deepgram, Gladia, Google Cloud, Azure, RevAI, Whisper
- LLM: OpenAI, Anthropic
- TTS: ElevenLabs, Microsoft Azure, Google Cloud, Play.ht, Coqui (OSS), AWS Polly

**Self-hosted Möglichkeiten:**
- ✅ Selbst hostbar
- ⚠️ Braucht API-Keys für Telefonie

**Setup-Komplexität:** Mittel

---

## 2. "Bring Your Own Number" Lösungen

### 2.1 Fritz AI Assistant (für FritzBox)
- **GitHub:** https://github.com/dohren/fritz-ai-assistant
- **Stars:** 9
- **Sprache:** Python

**Beschreibung:**
Docker-Container der IP-Telefone (z.B. FritzBox) mit KI verbindet. Antwortet Anrufe, spricht mit lokalem TTS (Piper), und triggert Automatisierungen (n8n) via Webhooks.

**Vorteile:**
- ✅ Echte deutsche Telefonnummer (FritzBox)
- ✅ Lokales TTS (Wyoming Piper)
- ✅ Integration mit n8n
- ✅ Volle Kontrolle über eigene Hardware

**Setup:**
- FritzBox mit IP-Telefon konfigurieren
- Asterisk + ARI App (FastAPI)
- Docker Compose

**Kosten:**
- Nur Telefonie-Kosten (wie gewohnt)
- Keine zusätzlichen API-Kosten (wenn lokal)

---

### 2.2 Asterisk/FreePBX + AI Integration

**Projekte:**
- **voice-agent-asterisk** (3 Stars): https://github.com/msolomos/voice-agent-asterisk
  - Python-basiert, OpenAI Integration
  
**Möglichkeiten:**
- ✅ SIP-Trunking mit eigener Telefonnummer
- ✅ Asterisk ARI (Asterisk REST Interface) für KI-Integration
- ✅ FreePBX als GUI für Asterisk
- ✅ Verbindung mit lokalen LLMs möglich

**Setup-Komplexität:** Hoch (Asterisk Kenntnisse erforderlich)

**Kosten:**
- SIP-Trunk: ~5-10€/Monat (z.B. Sipgate, Dus.net)
- Server: Selbst gehostet oder VPS
- Keine API-Kosten bei lokaler KI

---

### 2.3 Allgemeine Telefonie-Provider für BYON

| Provider | Preis/Min | Eigene Nummer | SIP-Trunk |
|----------|-----------|---------------|-----------|
| **Twilio** | ~$0.0085 | ✅ | ✅ |
| **Plivo** | ~$0.005 | ✅ | ✅ |
| **Vonage** | ~$0.004 | ✅ | ✅ |
| **Telnyx** | ~$0.002 | ✅ | ✅ |
| **Sipgate** | 0.89ct/min | ✅ | ✅ |

---

## 3. Lokale/Vollständig Self-Hosted Lösungen

### 3.1 Chanakya - Local Voice Assistant
- **GitHub:** https://github.com/Rishabh-Bajpai/Chanakya-Local-Friend
- **Stars:** 167
- **Sprache:** JavaScript

**Features:**
- 🔒 100% Privacy (lokale Modelle)
- 🗣️ Voice-Powered via Ollama
- 🛠️ MCP (Model Context Protocol) für 1000+ Integrationen
- 🏠 Home Assistant Integration
- 🧠 Long-Term Memory
- 🐳 Docker Support

**Stack:**
- STT: Lokales Modell
- LLM: Ollama (lokale Modelle)
- TTS: Lokales Modell

**Vorteile:**
- ✅ Keine API-Keys nötig
- ✅ Keine Cloud-Abhängigkeit
- ✅ Hohe Privatsphäre

**Nachteile:**
- ❌ Keine Telefonie-Integration (nur Web-Interface)
- ❌ Höhere Hardware-Anforderungen

---

### 3.2 Kompletter Self-Hosted Stack (DIY)

**Komponenten:**
1. **Telefonie:** Asterisk + SIP-Trunk
2. **STT:** Whisper (lokal) oder Whisper.cpp
3. **LLM:** Ollama, vLLM, oder llama.cpp
4. **TTS:** Piper (lokal) oder Coqui TTS
5. **Orchestrierung:** Eigenes Python-Script oder Pipecat

**Beispiel-Setup:**
```
Telefon → SIP-Trunk → Asterisk → ARI → Python App
                                      ↓
                              Whisper (STT)
                                      ↓
                              Ollama (LLM)
                                      ↓
                              Piper (TTS)
                                      ↓
                              Asterisk → Telefon
```

**Hardware-Anforderungen:**
- Whisper: 4-8 GB RAM (je nach Modellgröße)
- LLM: 8-32 GB RAM (je nach Modell)
- TTS: 2-4 GB RAM

---

## 4. Cloud vs. Self-Hosted Vergleich

| Aspekt | Cloud-Lösung | Self-Hosted |
|--------|--------------|-------------|
| **Einfachheit** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Kosten** | Pay-per-use | Hardware + SIP-Trunk |
| **Privacy** | ❌ Daten in Cloud | ✅ Daten bleiben lokal |
| **API-Keys** | Erforderlich | Optional (lokale Modelle) |
| **Skalierbarkeit** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Anpassung** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 5. Empfehlungen nach Anwendungsfall

### Schnellstart (Cloud)
**Beste Option:** Pipecat + Twilio
- Schnellster Einstieg
- Viele Beispiele
- Gute Dokumentation

### Maximale Privacy
**Beste Option:** Fritz AI Assistant oder DIY Asterisk + lokale Modelle
- Keine Daten verlassen das Haus
- Keine API-Abhängigkeiten

### "Bring Your Own Number"
**Beste Option:** Fritz AI Assistant (für FritzBox) oder Asterisk + SIP-Trunk
- Eigene Telefonnummer nutzen
- Volle Kontrolle

### Entwickler-Framework
**Beste Option:** Pipecat oder Bolna
- Modular und erweiterbar
- Große Community
- Viele Integrationen

---

## 6. Weitere Interessante Projekte

### 6.1 OpenRingr
- **GitHub:** https://github.com/Scott-mcarthur/openringr
- **Beschreibung:** Open-source AI phone agent als Alternative zu Vapi, Bland AI, Retell
- **Stars:** Neu (0)
- **Sprache:** TypeScript

### 6.2 Twilio + OpenAI Integrationen
Es gibt viele Beispiel-Projekte auf GitHub:
- **ai-call-agent** (40 Stars): OpenAI Realtime API + Twilio
- **ai-voice-assistant-openai-deepgram** (29 Stars): GPT + Deepgram + Twilio
- **live-translation-openai-realtime-api** (119 Stars): Live-Übersetzung

---

## 7. Kostenübersicht (Schätzung)

### Cloud-Setup (Pipecat + Twilio + OpenAI)
| Komponente | Kosten/Monat |
|------------|--------------|
| Twilio Nummer | ~$1 |
| Twilio Calls | ~$0.0085/min |
| OpenAI GPT-4o-mini | ~$0.15/Mio tokens |
| ElevenLabs TTS | ~$5/Monat |
| **Gesamt** | ~$20-50/Monat (je nach Nutzung) |

### Self-Hosted (Asterisk + lokale Modelle)
| Komponente | Kosten/Monat |
|------------|--------------|
| SIP-Trunk (Sipgate) | ~0€ (nur Verbrauch) |
| Server (Strom) | ~5-10€ |
| Hardware (einmalig) | ~500-1000€ |
| **Gesamt** | ~5-10€/Monat + Hardware |

---

## 8. Zusammenfassung

| Projekt | Einfachheit | Self-Hosted | Telefonie | Privacy | Kosten |
|---------|-------------|-------------|-----------|---------|--------|
| **Pipecat** | ⭐⭐⭐⭐ | ✅ | ✅ | ⚠️* | $$ |
| **Bolna** | ⭐⭐⭐⭐ | ✅ | ✅ | ⚠️* | $$ |
| **Vocode** | ⭐⭐⭐ | ✅ | ✅ | ⚠️* | $$ |
| **Fritz AI** | ⭐⭐⭐ | ✅ | ✅ | ✅ | $ |
| **Chanakya** | ⭐⭐⭐ | ✅ | ❌ | ✅ | $ |
| **Asterisk DIY** | ⭐⭐ | ✅ | ✅ | ✅ | $ |

*Privacy hängt von gewählten Providern ab - mit lokalen Modellen ✅

---

## Nächste Schritte

1. **Für schnellen Test:** Pipecat Quickstart (15 Minuten)
2. **Für eigene Nummer:** Fritz AI Assistant ausprobieren (FritzBox vorhanden)
3. **Für maximale Kontrolle:** Asterisk + lokale Modelle aufsetzen
4. **Für Privacy-Fokus:** Chanakya oder kompletter lokaler Stack

---

*Diese Recherche wurde am 21. Februar 2026 durchgeführt.*
