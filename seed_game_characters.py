import os
import time
import psycopg2
import urllib.request
import urllib.parse
from dotenv import load_dotenv
import random

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Create static directory if not exists
os.makedirs("static/img/games", exist_ok=True)

# 20 Characters and their correct games + 3 wrong games
characters = [
    {"char": "Kratos", "correct": "God of War", "wrongs": ["Assassin's Creed", "Dark Souls", "Devil May Cry"]},
    {"char": "Master Chief", "correct": "Halo", "wrongs": ["Doom", "Gears of War", "Mass Effect"]},
    {"char": "Mario", "correct": "Super Mario", "wrongs": ["Sonic the Hedgehog", "Crash Bandicoot", "Rayman"]},
    {"char": "Sonic", "correct": "Sonic the Hedgehog", "wrongs": ["Super Mario", "Mega Man", "Pac-Man"]},
    {"char": "Lara Croft", "correct": "Tomb Raider", "wrongs": ["Uncharted", "Resident Evil", "Horizon Zero Dawn"]},
    {"char": "Geralt of Rivia", "correct": "The Witcher", "wrongs": ["Skyrim", "Dark Souls", "Dragon Age"]},
    {"char": "Link", "correct": "The Legend of Zelda", "wrongs": ["Final Fantasy", "Genshin Impact", "Fire Emblem"]},
    {"char": "Arthur Morgan", "correct": "Red Dead Redemption 2", "wrongs": ["Grand Theft Auto V", "Call of Juarez", "Mafia"]},
    {"char": "Nathan Drake", "correct": "Uncharted", "wrongs": ["Tomb Raider", "The Last of Us", "Far Cry"]},
    {"char": "Solid Snake", "correct": "Metal Gear Solid", "wrongs": ["Splinter Cell", "Hitman", "Deus Ex"]},
    {"char": "Ellie", "correct": "The Last of Us", "wrongs": ["Resident Evil", "Silent Hill", "Days Gone"]},
    {"char": "Gordon Freeman", "correct": "Half-Life", "wrongs": ["Portal", "Bioshock", "Fallout"]},
    {"char": "Doom Slayer", "correct": "DOOM", "wrongs": ["Halo", "Quake", "Wolfenstein"]},
    {"char": "Ezio Auditore", "correct": "Assassin's Creed", "wrongs": ["Prince of Persia", "Dishonored", "Thief"]},
    {"char": "Cloud Strife", "correct": "Final Fantasy VII", "wrongs": ["Kingdom Hearts", "Devil May Cry", "Persona 5"]},
    {"char": "Ryu", "correct": "Street Fighter", "wrongs": ["Mortal Kombat", "Tekken", "King of Fighters"]},
    {"char": "Scorpion", "correct": "Mortal Kombat", "wrongs": ["Street Fighter", "Injustice", "Soulcalibur"]},
    {"char": "Pikachu", "correct": "Pokémon", "wrongs": ["Digimon", "Yu-Gi-Oh!", "Monster Hunter"]},
    {"char": "Pac-Man", "correct": "Pac-Man", "wrongs": ["Tetris", "Space Invaders", "Donkey Kong"]},
    {"char": "Steve", "correct": "Minecraft", "wrongs": ["Roblox", "Terraria", "Fortnite"]}
]

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "Karaktere Göre Oyunu Tahmin Et!", 
    "Oyun dünyasının en ikonik 20 karakteri burada! Acaba resimdeki karakterin hangi efsanevi oyuna ait olduğunu bulabilecek misin?",
    "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?q=80&w=800&auto=format&fit=crop", # Generic gaming image
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

print("Downloading images locally to avoid rate limits...")
for idx, c in enumerate(characters):
    char_name = c['char']
    
    # Download image from Pollinations sequentially
    filename = f"char_{oyun_id}_{idx}.jpg"
    filepath = f"static/img/games/{filename}"
    
    prompt = f"{char_name} from {c['correct']} video game character 3d render cinematic lighting high quality"
    query = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{query}?width=600&height=400&nologo=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded: {char_name}")
    except Exception as e:
        print(f"Error downloading {char_name}: {e}")
        # Use dummy image if fails
        filepath = "https://dummyimage.com/600x400/151520/ffffff&text=" + urllib.parse.quote(char_name)
        
    time.sleep(1.5) # Prevent 429 Too Many Requests
    
    # Insert question
    options = c['wrongs'] + [c['correct']]
    random.shuffle(options)
    
    dogru_harf = ""
    if options[0] == c['correct']: dogru_harf = "A"
    elif options[1] == c['correct']: dogru_harf = "B"
    elif options[2] == c['correct']: dogru_harf = "C"
    else: dogru_harf = "D"
    
    local_url = f"/{filepath}" if not filepath.startswith("http") else filepath
    
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, f"Bu ikonik karakter ({char_name}) hangi oyuna ait?", local_url, options[0], options[1], options[2], options[3], dogru_harf))

conn.commit()
cur.close()
conn.close()
print("Game Characters test seeded successfully with locally hosted images!")
