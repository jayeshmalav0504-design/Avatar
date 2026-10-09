# Rajasthan Tourism AI Avatar Production Kit — Maharani Edition

## 1. Scripts (60–80 Words Each)

### Option A: Welcoming & Cultural Focus
> **Word Count:** 74 words  
> **Key Themes:** Warmth, 'Padharo Mhare Des', folk instruments, dance, cuisine.
>
> *"Padharo Mhare Des! Welcome to Rajasthan, where vibrant traditions breathe life into golden sands. Listen to the soulful resonance of the sarangi, marvel at swirling Kalbelia dancers, and lose yourself in lively desert fairs. Indulge in authentic royal flavours, from rich Dal Baati Churma to fragrant ghevar. Here, every smile is an invitation and every sunset a festival of warmth. Come, experience royal hospitality and let the timeless heart of India welcome you home."*

---

### Option B: Historical & Architectural Grandeur
> **Word Count:** 76 words  
> **Key Themes:** Forts, palaces, valour, Mewar & Marwar royalty, timeless heritage.
>
> *"Step into an era of valour, romance, and enduring royal grandeur. Welcome to Rajasthan, a living canvas of human ambition. From the impregnable amber ramparts of Mehrangarh to the floating marble wonders of Udaipur's Lake Palace, every stone whispers legends of kings and warriors. Wander through ornate jharokhas, mirrored royal courtyards, and grand desert fortresses carved from living rock. Witness a majestic heritage that has stood the test of centuries. Unveil the royal legacy of Rajasthan."*

---

## 2. Image Generation Prompt (Maharani Avatar)

```text
Ultra-realistic frontal studio portrait of an elegant and graceful Rajasthani Maharani (royal queen), chest-up view looking directly into the camera with a warm, welcoming, regal smile, mouth gently closed. She wears an exquisite royal ruby-red and emerald-green silk poshak with intricate handcrafted golden gota patti and zardozi embroidery, a delicate sheer golden odhna (veil) draped gracefully over her head and hair, traditional Rajasthani royal jewelry including an ornate kundan and pearl maang tikka (borla) on her forehead, an elegant gold nath (nose ring), layered pearl and emerald choker necklaces (aad and rani haar), and glittering jhumkas. Softly defocused background of a grand Udaipur marble palace courtyard with ornate scalloped arches and carved sandstone pillars, warm golden-hour royal lighting, 85mm portrait lens, photorealistic 8k, natural radiant skin texture, perfect for AI video animation.
```

- **File Generated:** `avatar.jpg` (active D-ID image)

---

## 3. Voice Recommendations (Maharani Persona)

| Parameter | Recommended Setting | Rationale |
| :--- | :--- | :--- |
| **Provider** | Microsoft Azure / Edge TTS (via D-ID) | High naturalness with Indian English pronunciation |
| **Language Code** | `en-IN` (Indian English) / `hi-IN` (Hindi) | Flawless phonetic handling of Hindi/Rajasthani names (*Padharo Mhare Des*, *sarangi*, *Mehrangarh*, *jharokhas*) |
| **Voice Persona** | `en-IN-NeerjaNeural` | Regal, melodic, warm, and sophisticated queen cadence |
| **Tone** | Regal, gracious, hospitable, articulate | Balances royal prestige with accessible warmth |
| **Pacing / Speed** | `0.95x` | Measured, deliberate pacing suited for cultural heritage storytelling |

---

## 4. Automation Script
Run `python create_did_video.py` in this folder to render the animated video.
