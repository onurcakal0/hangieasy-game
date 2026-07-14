import urllib.request
import urllib.parse
import json
import os
import time
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

def get_poster(title):
    try:
        url = "http://www.omdbapi.com/?apikey=trilogy&t=" + urllib.parse.quote(title)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        return data.get('Poster')
    except:
        return None

pairs = [
    {"c1": "Micah Bell", "g1": "Red Dead Redemption II", "c2": "Abby", "g2": "The Last of Us Part II"},
    {"c1": "General Shepherd", "g1": "Call of Duty: Modern Warfare 2", "c2": "Big Smoke", "g2": "Grand Theft Auto: San Andreas"},
    {"c1": "Preston Garvey", "g1": "Fallout 4", "c2": "Officer Tenpenny", "g2": "Grand Theft Auto: San Andreas"},
    {"c1": "Ashley Graham", "g1": "Resident Evil 4", "c2": "Navirou", "g2": "Monster Hunter Stories"},
    {"c1": "Slippy Toad", "g1": "Star Fox 64", "c2": "Mr. Resetti", "g2": "Animal Crossing"},
    {"c1": "Nazeem", "g1": "The Elder Scrolls V: Skyrim", "c2": "Adoring Fan", "g2": "The Elder Scrolls IV: Oblivion"},
    {"c1": "Eric Sparrow", "g1": "Tony Hawk's Underground", "c2": "Gary Smith", "g2": "Bully"},
    {"c1": "Lance Vance", "g1": "Grand Theft Auto: Vice City", "c2": "David", "g2": "The Last of Us"},
    {"c1": "Moneybags", "g1": "Spyro the Dragon", "c2": "Patches", "g2": "Dark Souls"},
    {"c1": "Edgar Ross", "g1": "Red Dead Redemption", "c2": "Seymour Guado", "g2": "Final Fantasy X"}
]

print("Creating Hated Characters tournament...")

# Create cover using a generic angry gamer / villain concept from unsplash
main_cover_url = "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=800&auto=format&fit=crop"

cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "Oyunların En Sevilmeyen Karakterleri", 
    "Oyun dünyasının en nefret edilen, gıcık eden 20 karakteri karşı karşıya! Sana göre en sinir bozucu karakter hangisi? Seçimini yap ve tarafını belli et!",
    main_cover_url,
    "Eğlence",
    "omu_bumu",
    0
))
oyun_id = cur.fetchone()[0]

dir_path = "static/img/hated_chars"
os.makedirs(dir_path, exist_ok=True)

for i, pair in enumerate(pairs):
    poster1 = get_poster(pair["g1"])
    poster2 = get_poster(pair["g2"])
    
    if not poster1 or poster1 == "N/A": poster1 = main_cover_url
    if not poster2 or poster2 == "N/A": poster2 = main_cover_url
    
    path1 = f"{dir_path}/{i}_1.jpg"
    path2 = f"{dir_path}/{i}_2.jpg"
    
    try:
        urllib.request.urlretrieve(poster1, path1)
        urllib.request.urlretrieve(poster2, path2)
    except:
        print(f"Failed to download for {pair['g1']} or {pair['g2']}, using URLs")
        path1 = poster1
        path2 = poster2
        
    final_path1 = f"/{path1}" if not path1.startswith("http") else path1
    final_path2 = f"/{path2}" if not path2.startswith("http") else path2
    
    resim_url = f"{final_path1},{final_path2}"
    
    # We display the Character Name prominently, with the game in parenthesis.
    secenekler = f"{pair['c1']} ({pair['g1']}),{pair['c2']} ({pair['g2']})"
    dogru_cevap = "Farketmez"
    
    cur.execute('''
        INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
        VALUES (%s, %s, %s, %s)
    ''', (oyun_id, secenekler, dogru_cevap, resim_url))
    print(f"Added pair: {pair['c1']} vs {pair['c2']}")
    time.sleep(0.5)

conn.commit()
cur.close()
conn.close()
print("Hated characters seeded successfully!")
