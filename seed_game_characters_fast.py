import os
import time
import psycopg2
import urllib.request
import urllib.parse
import re
from dotenv import load_dotenv
import random
import concurrent.futures

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. Delete old broken game
cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Karaktere Göre Oyunu Tahmin Et!'")
for row in cur.fetchall():
    oyun_id = row[0]
    cur.execute("DELETE FROM hangisi_soru WHERE oyun_id = %s", (oyun_id,))
    cur.execute("DELETE FROM hangisi_skor WHERE oyun_id = %s", (oyun_id,))
    cur.execute("DELETE FROM hangisi_tepki WHERE oyun_id = %s", (oyun_id,))
    cur.execute("DELETE FROM hangisi_oyun WHERE id = %s", (oyun_id,))
conn.commit()

# Create static directory if not exists
os.makedirs("static/img/games", exist_ok=True)

# 20 Characters, their wiki pages, and games
characters = [
    {"char": "Kratos", "correct": "God of War", "wiki": "Kratos_(God_of_War)", "wrongs": ["Assassin's Creed", "Dark Souls", "Devil May Cry"]},
    {"char": "Master Chief", "correct": "Halo", "wiki": "Master_Chief_(Halo)", "wrongs": ["Doom", "Gears of War", "Mass Effect"]},
    {"char": "Mario", "correct": "Super Mario", "wiki": "Mario", "wrongs": ["Sonic the Hedgehog", "Crash Bandicoot", "Rayman"]},
    {"char": "Sonic", "correct": "Sonic the Hedgehog", "wiki": "Sonic_the_Hedgehog_(character)", "wrongs": ["Super Mario", "Mega Man", "Pac-Man"]},
    {"char": "Lara Croft", "correct": "Tomb Raider", "wiki": "Lara_Croft", "wrongs": ["Uncharted", "Resident Evil", "Horizon Zero Dawn"]},
    {"char": "Geralt of Rivia", "correct": "The Witcher", "wiki": "Geralt_of_Rivia", "wrongs": ["Skyrim", "Dark Souls", "Dragon Age"]},
    {"char": "Link", "correct": "The Legend of Zelda", "wiki": "Link_(The_Legend_of_Zelda)", "wrongs": ["Final Fantasy", "Genshin Impact", "Fire Emblem"]},
    {"char": "Arthur Morgan", "correct": "Red Dead Redemption 2", "wiki": "Arthur_Morgan_(Red_Dead)", "wrongs": ["Grand Theft Auto V", "Call of Juarez", "Mafia"]},
    {"char": "Nathan Drake", "correct": "Uncharted", "wiki": "Nathan_Drake_(character)", "wrongs": ["Tomb Raider", "The Last of Us", "Far Cry"]},
    {"char": "Solid Snake", "correct": "Metal Gear Solid", "wiki": "Solid_Snake", "wrongs": ["Splinter Cell", "Hitman", "Deus Ex"]},
    {"char": "Ellie", "correct": "The Last of Us", "wiki": "Ellie_(The_Last_of_Us)", "wrongs": ["Resident Evil", "Silent Hill", "Days Gone"]},
    {"char": "Gordon Freeman", "correct": "Half-Life", "wiki": "Gordon_Freeman", "wrongs": ["Portal", "Bioshock", "Fallout"]},
    {"char": "Doomguy", "correct": "DOOM", "wiki": "Doomguy", "wrongs": ["Halo", "Quake", "Wolfenstein"]},
    {"char": "Ezio Auditore", "correct": "Assassin's Creed", "wiki": "Ezio_Auditore_da_Firenze", "wrongs": ["Prince of Persia", "Dishonored", "Thief"]},
    {"char": "Cloud Strife", "correct": "Final Fantasy VII", "wiki": "Cloud_Strife", "wrongs": ["Kingdom Hearts", "Devil May Cry", "Persona 5"]},
    {"char": "Ryu", "correct": "Street Fighter", "wiki": "Ryu_(Street_Fighter)", "wrongs": ["Mortal Kombat", "Tekken", "King of Fighters"]},
    {"char": "Scorpion", "correct": "Mortal Kombat", "wiki": "Scorpion_(Mortal_Kombat)", "wrongs": ["Street Fighter", "Injustice", "Soulcalibur"]},
    {"char": "Pikachu", "correct": "Pokémon", "wiki": "Pikachu", "wrongs": ["Digimon", "Yu-Gi-Oh!", "Monster Hunter"]},
    {"char": "Pac-Man", "correct": "Pac-Man", "wiki": "Pac-Man_(character)", "wrongs": ["Tetris", "Space Invaders", "Donkey Kong"]},
    {"char": "Steve", "correct": "Minecraft", "wiki": "Steve_(Minecraft)", "wrongs": ["Roblox", "Terraria", "Fortnite"]}
]

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "Karaktere Göre Oyunu Tahmin Et!", 
    "Oyun dünyasının en ikonik 20 karakteri burada! Acaba resimdeki karakterin hangi efsanevi oyuna ait olduğunu bulabilecek misin?",
    "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?q=80&w=800&auto=format&fit=crop", 
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]
conn.commit()

def process_character(idx, c):
    char_name = c['char']
    wiki_url = f"https://en.wikipedia.org/wiki/{c['wiki']}"
    filename = f"char_{oyun_id}_{idx}.jpg"
    filepath = f"static/img/games/{filename}"
    
    local_url = "https://dummyimage.com/600x400/151520/ffffff&text=" + urllib.parse.quote(char_name)
    try:
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'meta property="og:image" content="(.*?)"', html)
        if match:
            img_url = match.group(1)
            # Download image
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            local_url = f"/{filepath}"
            print(f"Downloaded: {char_name}")
        else:
            print(f"No og:image for {char_name}")
    except Exception as e:
        print(f"Error {char_name}: {e}")

    # Insert question
    options = c['wrongs'] + [c['correct']]
    random.shuffle(options)
    
    dogru_harf = "A" if options[0] == c['correct'] else "B" if options[1] == c['correct'] else "C" if options[2] == c['correct'] else "D"
    
    return (oyun_id, f"Bu ikonik karakter ({char_name}) hangi oyuna ait?", local_url, options[0], options[1], options[2], options[3], dogru_harf)

# Use ThreadPoolExecutor for fast concurrent downloads
questions = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_character, idx, c) for idx, c in enumerate(characters)]
    for future in concurrent.futures.as_completed(futures):
        questions.append(future.result())

# Batch insert questions
for q in questions:
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', q)

conn.commit()
cur.close()
conn.close()
print("Game Characters test seeded instantly and successfully!")
