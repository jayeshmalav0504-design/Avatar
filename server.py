"""
Rajasthan Tourism Avatar Web Studio Server
-------------------------------------------
Zero-dependency Python HTTP server that runs the web interface locally.
Features:
- Maharani Gayatri Devi royal avatar & cultural persona
- Microsoft en-IN-NeerjaNeural neural voice synthesis
- In-memory cached audio clips for sub-millisecond instant playback
- Direct D-ID video studio integration

Usage:
    python server.py
Then open http://localhost:5000 in your browser.
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import asyncio
import io
import hashlib
import edge_tts

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 5000
API_KEY = "Z29vZ2xlLW9hdXRoMnwxMDU2NDU3ODA5ODM0MzY0MzAyNzdAYWtfVzh5Nl9MQzdwTEg3ZTA4dDlteVRz:AYPI15kyrZV76D_WmDhuB"
AUTH_HEADER = "Basic " + base64.b64encode(API_KEY.encode()).decode()

DEFAULT_IMAGE_URL = "s3://d-id-images-prod/google-oauth2|105645780983436430277/img_2DT4ccj-uSfTN5PhaGZ3a/avatar.jpg"
CACHED_IMAGE_URL = DEFAULT_IMAGE_URL
AUDIO_CACHE = {}
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_cache")
os.makedirs(AUDIO_DIR, exist_ok=True)

def preload_audio_cache():
    """Preloads disk-cached audio clips into memory for sub-millisecond responses."""
    loaded = 0
    if os.path.exists(AUDIO_DIR):
        for fname in os.listdir(AUDIO_DIR):
            if fname.endswith(".mp3"):
                fpath = os.path.join(AUDIO_DIR, fname)
                try:
                    with open(fpath, "rb") as f:
                        data = f.read()
                        if len(data) > 500:
                            h = os.path.splitext(fname)[0]
                            AUDIO_CACHE[h] = data
                            loaded += 1
                except Exception:
                    pass
    print(f"[CACHE] Loaded {loaded} pre-cached en-IN-NeerjaNeural audio files into memory.")

def get_text_hash(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]

def generate_maharani_audio(text):
    """Renders speech using the authentic en-IN-NeerjaNeural royal voice persona."""
    if not text:
        return None
    cleaned = text.strip()
    h = get_text_hash(cleaned)

    # 1. Check in-memory cache by hash or raw text
    if h in AUDIO_CACHE:
        return AUDIO_CACHE[h]
    if cleaned in AUDIO_CACHE:
        return AUDIO_CACHE[cleaned]

    # 2. Check disk cache
    disk_path = os.path.join(AUDIO_DIR, f"{h}.mp3")
    if os.path.exists(disk_path):
        try:
            with open(disk_path, "rb") as f:
                data = f.read()
                if len(data) > 500:
                    AUDIO_CACHE[h] = data
                    AUDIO_CACHE[cleaned] = data
                    return data
        except Exception:
            pass

    # 3. Dynamic synthesis with edge-tts
    async def _render():
        comm = edge_tts.Communicate(cleaned, "en-IN-NeerjaNeural")
        buf = io.BytesIO()
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        return buf.getvalue()

    try:
        audio_bytes = asyncio.run(_render())
        if audio_bytes and len(audio_bytes) > 500:
            AUDIO_CACHE[h] = audio_bytes
            AUDIO_CACHE[cleaned] = audio_bytes
            try:
                with open(disk_path, "wb") as f:
                    f.write(audio_bytes)
            except Exception:
                pass
            return audio_bytes
    except Exception as e:
        print(f"Notice: Neural TTS render exception: {e}")
    return None

def upload_local_avatar():
    global CACHED_IMAGE_URL
    if CACHED_IMAGE_URL:
        return CACHED_IMAGE_URL

    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "avatar.jpg")

    if not os.path.exists(image_path):
        CACHED_IMAGE_URL = DEFAULT_IMAGE_URL
        return CACHED_IMAGE_URL

    try:
        with open(image_path, "rb") as f:
            file_bytes = f.read()

        boundary = "----WebKitFormBoundary" + hex(int(time.time() * 1000))[2:]
        crlf = b"\r\n"
        body = bytearray()
        body.extend(f"--{boundary}".encode() + crlf)
        body.extend(b'Content-Disposition: form-data; name="image"; filename="avatar.jpg"' + crlf)
        body.extend(b"Content-Type: image/jpeg" + crlf + crlf)
        body.extend(file_bytes)
        body.extend(crlf)
        body.extend(f"--{boundary}--".encode() + crlf)

        req = urllib.request.Request(
            "https://api.d-id.com/images",
            data=bytes(body),
            headers={
                "Authorization": AUTH_HEADER,
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Accept": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            CACHED_IMAGE_URL = data.get("url") or DEFAULT_IMAGE_URL
            return CACHED_IMAGE_URL
    except Exception as e:
        print(f"Notice: Using verified avatar image URL due to upload status: {e}")
        CACHED_IMAGE_URL = DEFAULT_IMAGE_URL
        return CACHED_IMAGE_URL

def generate_royal_reply(q):
    """Generates an authentic, deeply cultural Rajasthani Maharani Ambassador reply."""
    if not q:
        return "Arey Khamma Ghani Sa, my dear guest! Come on in, let me share a royal secret with you. When you visit Rajasthan, you do not just see history - you live it! Have you ever climbed the winding ramparts of Mehrangarh as the desert wind sings ancient warrior songs? Or tasted piping hot Dal Baati Churma with sweet ghevar in a buzzing night bazaar? From regal courtyards to starlit sand dunes, every moment is pure magic. Tell me, when are you visiting? Padharo Mhare Des!"

    q_lower = q.lower()

    # 1. Greetings & Royal Welcome
    if any(k in q_lower for k in ["hello", "hi", "hey", "khamma", "namaste", "ghani", "greetings", "ram ram", "pranam", "adaab", "padharo"]):
        return "Arey Khamma Ghani Sa, my dear friend! A royal, heartfelt welcome to the land of kings and queens, eternal romance, and supreme grace. I am Maharani Gayatri Devi, and in our Rajasthan we hold sacred the timeless creed of 'Atithi Devo Bhava' - the guest is God. Tell me, what stirs your curiosity today, Hukum? Majestic hill forts, starlit sand dunes, royal feasts, or colorful bazaars?"

    # 2. Identity / Persona / Background
    if any(k in q_lower for k in ["who are you", "what is your name", "tell me about yourself", "who r u", "kaun ho", "aap kaun", "introduce", "maharani"]):
        return "Arey Khamma Ghani! I am Maharani Gayatri Devi, your royal cultural ambassador! It is my deepest honor to welcome travelers from across the world into our palace courtyards and share the living soul of Rajasthan - our royal heritage, shimmering lake palaces, desert ballads, and heartfelt hospitality. Consider me your royal guide and sister, Hukum!"

    # 3. Jaipur / Pink City
    if any(k in q_lower for k in ["jaipur", "pink city", "amer", "amber fort", "hawa mahal", "jal mahal", "nahargarh", "jaigarh", "bapu bazaar", "chokhi dhani"]):
        return "Arey Jaipur, our beloved Pink City! Founded in 1727 by Maharaja Sawai Jai Singh II, its rose-colored gates open with immense warmth. Imagine gazing up at the 953 honeycombed breeze windows of Hawa Mahal, walking through the mirrored celestial halls of Amber Fort's Sheesh Mahal, and watching the pink skyline blush with gold at sunset from Nahargarh! And by night, feast on a royal thali while folk dancers swirl to the beats of the dhol. Pure magic, my dear friend!"

    # 4. Udaipur / City of Lakes
    if any(k in q_lower for k in ["udaipur", "lake pichola", "city palace", "jag mandir", "fateh sagar", "monsoon palace", "sajjangarh", "lake palace", "venice of the east"]):
        return "Ah, Udaipur, the Venice of the East and pride of Mewar! Cradled by the ancient Aravalli mountains, it is pure romance. Picture the majestic white marble City Palace reflecting in the calm waters of Lake Pichola, and the ethereal Lake Palace floating like a royal swan. Take a gentle sunset boat ride as the evening breeze ripples across the water and palace lamps flicker like stars. You will fall in love with Udaipur, Hukum!"

    # 5. Jodhpur / The Blue City
    if any(k in q_lower for k in ["jodhpur", "blue city", "mehrangarh", "jaswant thada", "umaid bhawan", "clock tower", "ghanta ghar", "suncity"]):
        return "Arey Jodhpur, the glorious Sun City under the protective gaze of Mehrangarh Fort! Towering 400 feet above a sea of indigo-blue houses, Mehrangarh is one of the grandest fortresses on Earth. As you climb its winding ramparts, the desert wind whispers ancient ballads of Rajput courage and valor. And right below, the white marble cenotaph of Jaswant Thada gleams like a desert jewel. Truly magnificent, my friend!"

    # 6. Jaisalmer / Desert Safari / Thar
    if any(k in q_lower for k in ["jaisalmer", "desert", "safari", "camel", "thar", "sand", "dunes", "sam dunes", "sonar qila", "golden fort", "khuri", "dune bashing"]):
        return "Arey, the golden sands of Jaisalmer will enchant your very soul! Here stands Sonar Qila, our living Golden Fort sculpted from yellow sandstone. Ride into the rolling Sam sand dunes on a decorated camel as the sun sets in blazing crimson. At night, sit beside a crackling campfire under an infinite canopy of stars, listening to the soulful Sarangi singing 'Kesariya Balam'. Tell me, are you ready for the desert magic? Padharo Mhare Des!"

    # 7. Royal Food & Delicacies
    if any(k in q_lower for k in ["food", "eat", "dish", "cuisine", "taste", "dal baati", "kachori", "sweet", "ghevar", "laal maas", "ker sangri", "gatte", "churma", "hungry"]):
        return "Arey, feasting in Rajasthan is an art made for emperors and queens! You must taste our piping hot Dal Baati Churma, drenched in fragrant golden desi ghee. Savor spicy Ker Sangri, crisp Pyaaz Kachoris fresh from morning bazaar karahis, and fiery royal Laal Maas simmered with Mathania red chilies. And never leave without golden honeycomb Ghevar soaked in saffron syrup! One bite and your soul will sing with joy, Hukum!"

    # 8. Forts & Palaces (General / Kumbhalgarh / Chittorgarh)
    if any(k in q_lower for k in ["fort", "palace", "kumbhalgarh", "chittorgarh", "chittor", "padmini", "vijay stambh", "wall", "castle"]):
        return "Our forts are not made of silent stone, Hukum - every rampart breathes with stories of supreme honor! Chittorgarh Fort stands as the eternal altar of Rajput courage and Rani Padmini's immortal grace. In Kumbhalgarh, walk along the world's second-longest continuous wall - 36 kilometers winding across the mountains! Stand upon these battlements, close your eyes, and you will hear the galloping hooves of warrior kings."

    # 9. Culture, Music & Dance
    if any(k in q_lower for k in ["culture", "dance", "music", "festival", "kalbelia", "ghoomar", "song", "folk", "sarangi", "tradition", "turban", "pagri", "poshak"]):
        return "Our culture is a vibrant, joyous celebration of life! Watch royal women dance the graceful Ghoomar with swirling, mirror-embroidered ghagras, and marvel at the fiery, hypnotic twirls of the Kalbelia desert dancers. When the Khartal clicks and the soulful Sarangi plays, the entire desert comes alive. If you can, visit during our Desert Festival or Pushkar Mela - it is an unforgettable spectacle of color, my friend!"

    # 10. Pushkar & Ajmer
    if any(k in q_lower for k in ["pushkar", "ajmer", "brahma", "dargah", "holy lake", "ghat", "camel fair"]):
        return "Pushkar is a divine, peaceful oasis, blessed with the sacred Lord Brahma Temple and 52 holy bathing ghats encircling its serene lake. During Kartik Purnima, it erupts with joy during the world-famous Pushkar Camel Fair! And just across the mountain lies Ajmer Sharif, where pilgrims of all faiths seek peace, hope, and blessings at the revered shrine of Sufi Saint Khwaja Moinuddin Chishti."

    # 11. Ranthambore & Wildlife
    if any(k in q_lower for k in ["ranthambore", "tiger", "safari", "wildlife", "national park", "sariska", "bharatpur", "bird"]):
        return "Rajasthan's wild spirit reigns at Ranthambore National Park! Here, the Royal Bengal Tiger roams like an emperor among tenth-century fort ruins and ancient banyan trees. Imagine an early morning jungle safari through the misty ravines when suddenly a magnificent striped tiger steps out before you - it is a thrill that will make your heart race with wonder, Hukum!"

    # 12. Shopping & Handicrafts
    if any(k in q_lower for k in ["shopping", "shop", "buy", "textile", "jewelry", "pottery", "souvenir", "market", "bazaar", "mojri", "bandhani"]):
        return "Rajasthan's bazaars are an artisan's wonderland! In Jaipur, discover authentic cobalt Blue Pottery, dazzling Kundan and Meenakari jewelry, and swirling Leheriya tie-dye fabrics. In Jodhpur, slip into handcrafted camel-leather mojris and take home fragrant Mathania spices. Every craft has been passed down from master artisans across royal generations!"

    # 13. Best Time to Visit & Weather
    if any(k in q_lower for k in ["when", "weather", "time to visit", "month", "season", "october", "winter", "summer", "monsoon", "temperature"]):
        return "The golden season to visit our land is between October and March! The desert winter brings pleasant, warm sunshine by day and cool, refreshing starlit nights. It is the peak season of vibrant folk festivals, camel safaris, and rooftop palace dining. Even our monsoon from July to September turns Udaipur and Mount Abu into emerald green wonderlands, my friend!"

    # 14. Itinerary & Trip Planning
    if any(k in q_lower for k in ["itinerary", "plan", "trip", "tour", "how many days", "days", "route", "places to visit", "visit"]):
        return "For an unforgettable royal journey, I suggest seven to ten days: Spend two days exploring Jaipur's Amber Fort and bazaars, two days discovering Jodhpur's blue alleys and Mehrangarh, two days riding camels across Jaisalmer's golden sand dunes, and two days resting beside Udaipur's romantic lakes. A royal circuit that will fill your heart with memories for a lifetime, Hukum!"

    # 15. Hotels & Heritage Havelis
    if any(k in q_lower for k in ["hotel", "stay", "resort", "haveli", "heritage", "luxury", "budget", "room", "accommodation"]):
        return "In Rajasthan, every traveler is treated like royal royalty! For supreme grandeur, stay in living palaces like Taj Lake Palace in Udaipur or Rambagh Palace in Jaipur. For authentic charm on any budget, stay in family-run heritage havelis with carved jharokhas, courtyards, and warm home-cooked delicacies. You will not feel like a tourist - you will feel like family!"

    # 16. Safety & Travel Tips
    if any(k in q_lower for k in ["safe", "safety", "solo", "tip", "dress", "water", "transport", "cab", "train", "flight"]):
        return "Travel with an easy mind, my friend! Rajasthan is globally celebrated for its warmth, kindness, and deep respect for guests under 'Atithi Devo Bhava'. Keep water handy in the sunny desert, dress respectfully when visiting sacred temples, take certified government guides at monuments, and always bring a friendly smile. We will take care of you like our own! Padharo Mhare Des!"

    # 17. Hindi / Hinglish Inquiries
    if any(k in q_lower for k in ["kaisa", "kahan", "kya", "batao", "kaise", "dhanyawad", "shukriya", "acha", "shubh"]):
        return "Arey Khamma Ghani Sa! Rajasthan ki paawan veer-bhoomi par aapka hardik swagat hai! Hamare yahan Amer Qila, Hawa Mahal, Mehrangarh ki shaan, Thar Desert ke sunhare dhoron par camel safari, aur desi ghee se bhare Dal Baati Churma aapka intezaar kar rahe hain. Hukum, aap kis sheher ya vishay ke baare mein jaanna chahte hain? Main Maharani Gayatri Devi aapki poori madad karoongi!"

    # 18. Default Royal Envoy Response
    return "Arey Hukum, you speak of an intriguing question! In Rajasthan, every palace wall whispers history and every desert wind sings a ballad of valor. Whether you wish to explore our grand hill forts, taste royal delicacies, ride camels across starlit dunes, or witness colorful folk dances, I am right here by your side. Tell me, which wonder shall we unveil first, my friend?"

class StudioHandler(SimpleHTTPRequestHandler):
    def address_string(self):
        return str(self.client_address[0])

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/check-status":
            query = urllib.parse.parse_qs(parsed.query)
            talk_id = query.get("id", [None])[0]
            if not talk_id:
                self.send_error(400, "Missing talk ID")
                return

            req = urllib.request.Request(
                f"https://api.d-id.com/talks/{talk_id}",
                headers={"Authorization": AUTH_HEADER, "Accept": "application/json"}
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    resp_data = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(resp_data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(e.read())
            return

        elif parsed.path == "/api/intro-audio":
            intro_audio = AUDIO_CACHE.get("0faa8315f9bdffce") or AUDIO_CACHE.get("intro_maharani") or AUDIO_CACHE.get("36bbde63831eebc8")
            if not intro_audio:
                disk_path = os.path.join(AUDIO_DIR, "0faa8315f9bdffce.mp3")
                if os.path.exists(disk_path):
                    with open(disk_path, "rb") as f:
                        intro_audio = f.read()
            if intro_audio:
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(intro_audio)))
                self.end_headers()
                self.wfile.write(intro_audio)
            else:
                self.send_error(404, "Intro audio not found")
            return

        elif parsed.path == "/api/tts":
            query = urllib.parse.parse_qs(parsed.query)
            text = query.get("text", [""])[0]
            if not text:
                self.send_error(400, "Missing text parameter")
                return
            audio_bytes = generate_maharani_audio(text)
            if audio_bytes:
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(audio_bytes)))
                self.end_headers()
                self.wfile.write(audio_bytes)
            else:
                self.send_error(500, "Audio generation failed")
            return

        super().do_GET()

    def do_POST(self):
        if self.path == "/api/create-video":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))

            script_text = payload.get("script", "")
            voice_id = payload.get("voice_id", "en-IN-NeerjaNeural")
            is_lively = payload.get("is_lively", True)

            try:
                img_url = upload_local_avatar()

                talk_payload = {
                    "source_url": img_url,
                    "script": {
                        "type": "text",
                        "subtitles": False,
                        "provider": {
                            "type": "microsoft",
                            "voice_id": voice_id
                        },
                        "input": script_text
                    },
                    "config": {
                        "fluent": True if is_lively else False,
                        "pad_audio": 0.0
                    }
                }

                if is_lively:
                    talk_payload["driver_url"] = "bank://lively/driver-06"

                req = urllib.request.Request(
                    "https://api.d-id.com/talks",
                    data=json.dumps(talk_payload).encode("utf-8"),
                    headers={
                        "Authorization": AUTH_HEADER,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    method="POST"
                )

                with urllib.request.urlopen(req) as resp:
                    result = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(result)

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        elif self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))
            query = payload.get("message", "").strip()

            reply = generate_royal_reply(query)
            audio_bytes = generate_maharani_audio(reply)

            response_data = {"reply": reply}
            if audio_bytes:
                response_data["audio"] = "data:audio/mp3;base64," + base64.b64encode(audio_bytes).decode("ascii")

            res_bytes = json.dumps(response_data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_bytes)))
            self.end_headers()
            self.wfile.write(res_bytes)
            return

        self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    preload_audio_cache()
    server = HTTPServer(("0.0.0.0", PORT), StudioHandler)
    print(f"\n=======================================================")
    print(f"  Rajasthan Tourism Studio Running at:")
    print(f"  --> http://localhost:{PORT}")
    print(f"  --> http://127.0.0.1:{PORT}")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
