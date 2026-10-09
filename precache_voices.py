"""
Pre-caches en-IN-NeerjaNeural audio for all standard responses of Maharani Gayatri Devi.
Ensures zero-latency response for chat and speech playback with authentic royal voice.
"""

import os
import sys
import hashlib
import asyncio
import edge_tts

VOICE = "en-IN-NeerjaNeural"
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_cache")
os.makedirs(AUDIO_DIR, exist_ok=True)

REPLIES = [
    # 0. Intro Welcome Greeting (Matches D-ID Video exactly)
    "Arey Khamma Ghani Sa, my dear guest! Come on in, let me share a royal secret with you. When you visit Rajasthan, you do not just see history - you live it! Have you ever climbed the winding ramparts of Mehrangarh as the desert wind sings ancient warrior songs? Or tasted piping hot Dal Baati Churma with sweet ghevar in a buzzing night bazaar? From regal courtyards to starlit sand dunes, every moment is pure magic. Tell me, when are you visiting? Padharo Mhare Des!",

    # 1. Greetings
    "Arey Khamma Ghani Sa, my dear friend! A royal, heartfelt welcome to the land of kings and queens, eternal romance, and supreme grace. I am Maharani Gayatri Devi, and in our Rajasthan we hold sacred the timeless creed of 'Atithi Devo Bhava' - the guest is God. Tell me, what stirs your curiosity today, Hukum? Majestic hill forts, starlit sand dunes, royal feasts, or colorful bazaars?",

    # 2. Who are you
    "Arey Khamma Ghani! I am Maharani Gayatri Devi, your royal cultural ambassador! It is my deepest honor to welcome travelers from across the world into our palace courtyards and share the living soul of Rajasthan - our royal heritage, shimmering lake palaces, desert ballads, and heartfelt hospitality. Consider me your royal guide and sister, Hukum!",

    # 3. Jaipur
    "Arey Jaipur, our beloved Pink City! Founded in 1727 by Maharaja Sawai Jai Singh II, its rose-colored gates open with immense warmth. Imagine gazing up at the 953 honeycombed breeze windows of Hawa Mahal, walking through the mirrored celestial halls of Amber Fort's Sheesh Mahal, and watching the pink skyline blush with gold at sunset from Nahargarh! And by night, feast on a royal thali while folk dancers swirl to the beats of the dhol. Pure magic, my dear friend!",

    # 4. Udaipur
    "Ah, Udaipur, the Venice of the East and pride of Mewar! Cradled by the ancient Aravalli mountains, it is pure romance. Picture the majestic white marble City Palace reflecting in the calm waters of Lake Pichola, and the ethereal Lake Palace floating like a royal swan. Take a gentle sunset boat ride as the evening breeze ripples across the water and palace lamps flicker like stars. You will fall in love with Udaipur, Hukum!",

    # 5. Jodhpur
    "Arey Jodhpur, the glorious Sun City under the protective gaze of Mehrangarh Fort! Towering 400 feet above a sea of indigo-blue houses, Mehrangarh is one of the grandest fortresses on Earth. As you climb its winding ramparts, the desert wind whispers ancient ballads of Rajput courage and valor. And right below, the white marble cenotaph of Jaswant Thada gleams like a desert jewel. Truly magnificent, my friend!",

    # 6. Jaisalmer
    "Arey, the golden sands of Jaisalmer will enchant your very soul! Here stands Sonar Qila, our living Golden Fort sculpted from yellow sandstone. Ride into the rolling Sam sand dunes on a decorated camel as the sun sets in blazing crimson. At night, sit beside a crackling campfire under an infinite canopy of stars, listening to the soulful Sarangi singing 'Kesariya Balam'. Tell me, are you ready for the desert magic? Padharo Mhare Des!",

    # 7. Food
    "Arey, feasting in Rajasthan is an art made for emperors and queens! You must taste our piping hot Dal Baati Churma, drenched in fragrant golden desi ghee. Savor spicy Ker Sangri, crisp Pyaaz Kachoris fresh from morning bazaar karahis, and fiery royal Laal Maas simmered with Mathania red chilies. And never leave without golden honeycomb Ghevar soaked in saffron syrup! One bite and your soul will sing with joy, Hukum!",

    # 8. Forts
    "Our forts are not made of silent stone, Hukum - every rampart breathes with stories of supreme honor! Chittorgarh Fort stands as the eternal altar of Rajput courage and Rani Padmini's immortal grace. In Kumbhalgarh, walk along the world's second-longest continuous wall - 36 kilometers winding across the mountains! Stand upon these battlements, close your eyes, and you will hear the galloping hooves of warrior kings.",

    # 9. Culture, music, dance
    "Our culture is a vibrant, joyous celebration of life! Watch royal women dance the graceful Ghoomar with swirling, mirror-embroidered ghagras, and marvel at the fiery, hypnotic twirls of the Kalbelia desert dancers. When the Khartal clicks and the soulful Sarangi plays, the entire desert comes alive. If you can, visit during our Desert Festival or Pushkar Mela - it is an unforgettable spectacle of color, my friend!",

    # 10. Pushkar & Ajmer
    "Pushkar is a divine, peaceful oasis, blessed with the sacred Lord Brahma Temple and 52 holy bathing ghats encircling its serene lake. During Kartik Purnima, it erupts with joy during the world-famous Pushkar Camel Fair! And just across the mountain lies Ajmer Sharif, where pilgrims of all faiths seek peace, hope, and blessings at the revered shrine of Sufi Saint Khwaja Moinuddin Chishti.",

    # 11. Wildlife & Tigers
    "Rajasthan's wild spirit reigns at Ranthambore National Park! Here, the Royal Bengal Tiger roams like an emperor among tenth-century fort ruins and ancient banyan trees. Imagine an early morning jungle safari through the misty ravines when suddenly a magnificent striped tiger steps out before you - it is a thrill that will make your heart race with wonder, Hukum!",

    # 12. Shopping
    "Rajasthan's bazaars are an artisan's wonderland! In Jaipur, discover authentic cobalt Blue Pottery, dazzling Kundan and Meenakari jewelry, and swirling Leheriya tie-dye fabrics. In Jodhpur, slip into handcrafted camel-leather mojris and take home fragrant Mathania spices. Every craft has been passed down from master artisans across royal generations!",

    # 13. Best time to visit
    "The golden season to visit our land is between October and March! The desert winter brings pleasant, warm sunshine by day and cool, refreshing starlit nights. It is the peak season of vibrant folk festivals, camel safaris, and rooftop palace dining. Even our monsoon from July to September turns Udaipur and Mount Abu into emerald green wonderlands, my friend!",

    # 14. Itinerary
    "For an unforgettable royal journey, I suggest seven to ten days: Spend two days exploring Jaipur's Amber Fort and bazaars, two days discovering Jodhpur's blue alleys and Mehrangarh, two days riding camels across Jaisalmer's golden sand dunes, and two days resting beside Udaipur's romantic lakes. A royal circuit that will fill your heart with memories for a lifetime, Hukum!",

    # 15. Hotels & Heritage
    "In Rajasthan, every traveler is treated like royal royalty! For supreme grandeur, stay in living palaces like Taj Lake Palace in Udaipur or Rambagh Palace in Jaipur. For authentic charm on any budget, stay in family-run heritage havelis with carved jharokhas, courtyards, and warm home-cooked delicacies. You will not feel like a tourist - you will feel like family!",

    # 16. Safety & Tips
    "Travel with an easy mind, my friend! Rajasthan is globally celebrated for its warmth, kindness, and deep respect for guests under 'Atithi Devo Bhava'. Keep water handy in the sunny desert, dress respectfully when visiting sacred temples, take certified government guides at monuments, and always bring a friendly smile. We will take care of you like our own! Padharo Mhare Des!",

    # 17. Hindi / Hinglish
    "Arey Khamma Ghani Sa! Rajasthan ki paawan veer-bhoomi par aapka hardik swagat hai! Hamare yahan Amer Qila, Hawa Mahal, Mehrangarh ki shaan, Thar Desert ke sunhare dhoron par camel safari, aur desi ghee se bhare Dal Baati Churma aapka intezaar kar rahe hain. Hukum, aap kis sheher ya vishay ke baare mein jaanna chahte hain? Main Maharani Gayatri Devi aapki poori madad karoonga!",

    # 18. Default Envoy
    "Arey Hukum, you speak of an intriguing question! In Rajasthan, every palace wall whispers history and every desert wind sings a ballad of valor. Whether you wish to explore our grand hill forts, taste royal delicacies, ride camels across starlit dunes, or witness colorful folk dances, I am right here by your side. Tell me, which wonder shall we unveil first, my friend?",

    # 19. Voice Test
    "Arey Khamma Ghani, my friend! I am Maharani Gayatri Devi, speaking in my authentic royal voice, exactly the same as my introduction video! Padharo Mhare Des!"
]

def get_hash(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]

async def render_text(idx, text):
    h = get_hash(text)
    filepath = os.path.join(AUDIO_DIR, f"{h}.mp3")
    print(f"[{idx+1}/{len(REPLIES)}] Rendering audio with {VOICE}...")
    comm = edge_tts.Communicate(text.strip(), VOICE)
    await comm.save(filepath)
    print(f"[{idx+1}/{len(REPLIES)}] Successfully saved: {h}.mp3 ({os.path.getsize(filepath)} bytes)")

async def main():
    print(f"Pre-caching {len(REPLIES)} cultural responses for Maharani Gayatri Devi ({VOICE})...")
    for idx, text in enumerate(REPLIES):
        await render_text(idx, text)
    print("\n[SUCCESS] All standard Maharani royal voice audio clips pre-cached successfully!")

if __name__ == "__main__":
    asyncio.run(main())
