# 👑 Padharo Mhare Des Studio — Royal Rajasthan AI Cultural Avatar

[![Rajasthan Tourism](https://img.shields.io/badge/Rajasthan-Tourism%20Cultural%20Avatar-gold)](http://localhost:5000)
[![Voice Persona](https://img.shields.io/badge/Voice-en--IN--NeerjaNeural-orange)](https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/)
[![Video Engine](https://img.shields.io/badge/Video-D--ID%20Lively%20Driver-blue)](https://www.d-id.com/)

An interactive, culturally rich AI avatar web studio showcasing **Maharani Gayatri Devi**, the royal cultural ambassador of Rajasthan. Experience living heritage with real-time conversational intelligence, lifelike lip-synced video presentations, and warm Indian neural speech synthesis.

---

## ✨ Features

- **👑 Royal Maharani Presenter**: Photorealistic 8K portrait and animated talking video avatar of Maharani Gayatri Devi in traditional royal Rajasthani poshak and kundan jewelry.
- **🎙️ Unified Neural Voice (`en-IN-NeerjaNeural`)**: Warm, melodic, and culturally authentic royal voice synthesized via Edge TTS / Azure Neural, harmonized across video, text, and chat playback.
- **⚡ Zero-Latency Pre-Cached Audio Engine**: Sub-millisecond instant speech playback with in-memory caching for all 20 standard cultural responses (*Khamma Ghani Sa*, royal forts, desert safaris, Dal Baati Churma, and travel itineraries).
- **🎤 Speech-to-Speech Microphone Input**: Voice recognition in the browser allowing travelers to speak their questions directly to the avatar.
- **🎬 Dual Mode Studio**:
  1. **Live Chat Mode**: Ask questions in English or Hindi and receive royal spoken answers with synchronized animated talking avatar and live audio visualizers.
  2. **D-ID Production Studio**: Generate custom talking avatar videos on-demand with lively head gestures and facial expressions.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- Modern Web Browser (Google Chrome, Microsoft Edge, or Firefox)

### 2. Install Dependencies
```bash
pip install edge-tts
```

### 3. Run the Studio Server
```bash
python server.py
```

### 4. Open in Browser
Navigate to:
```
http://localhost:5000
```

---

## 📁 Project Structure

```
├── index.html                     # Frontend studio UI (Chat, Video, Audio Player, Web Speech)
├── server.py                       # Zero-dependency Python HTTP server & API endpoints
├── precache_voices.py              # Script to pre-cache neural speech for all cultural responses
├── create_did_video.py             # D-ID video generation automation script
├── TOURISM_AVATAR_KIT.md           # Production guide, script options, and prompt engineering
├── avatar.jpg                      # Active Maharani Gayatri Devi avatar portrait
├── rajasthan_tourism_maharani.mp4  # Active animated talking avatar video (Full HD)
├── audio_cache/                    # Pre-rendered neural MP3 audio clips for instant playback
└── .gitignore                      # Git ignore rules for clean repository tracking
```

---

## 🏛️ Cultural Knowledge Base

The avatar natively provides authentic guides on:
- 🌸 **Jaipur (Pink City)**: Hawa Mahal, Amer Fort Sheesh Mahal, Nahargarh sunset.
- 🌊 **Udaipur (City of Lakes)**: Lake Pichola, City Palace, Jag Mandir.
- 🏰 **Jodhpur (Sun City)**: Mehrangarh Fort, Jaswant Thada, blue alleys.
- 🐪 **Jaisalmer (Golden City)**: Sonar Qila, Sam Sand Dunes, camel safaris, campfire folk music.
- 🍲 **Royal Gastronomy**: Dal Baati Churma, Ker Sangri, Pyaaz Kachori, Laal Maas, and Ghevar.
- 🐅 **Wildlife & Heritage**: Ranthambore Royal Bengal Tigers, Chittorgarh, and Kumbhalgarh's great wall.

---

## 📜 License & Credits

Built for **Incredible India • Rajasthan Tourism Cultural Promotion**.
Powered by D-ID Video Generation & Microsoft Neural Text-to-Speech.
