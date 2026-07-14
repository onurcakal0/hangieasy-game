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
    {"m1": "The Batman Part II", "m2": "Supergirl: Woman of Tomorrow"},
    {"m1": "The Mandalorian & Grogu", "m2": "Avengers: Doomsday"},
    {"m1": "Toy Story 5", "m2": "Shrek 5"},
    {"m1": "Frozen 3", "m2": "The Super Mario Bros. Movie 2"},
    {"m1": "Five Nights at Freddy's 2", "m2": "The Conjuring: Last Rites"},
    {"m1": "Spider-Man: Beyond the Spider-Verse", "m2": "Teenage Mutant Ninja Turtles: Mutant Mayhem 2"},
    {"m1": "The Hunger Games: Sunrise on the Reaping", "m2": "Project Hail Mary"},
    {"m1": "Fast X: Part 2", "m2": "Jumanji 4"},
    {"m1": "Dune: Messiah", "m2": "Star Wars: New Jedi Order"},
    {"m1": "M3GAN 2.0", "m2": "The Black Phone 2"}
]

print("Creating 2026 Movies tournament...")

main_cover_url = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=800&auto=format&fit=crop" # Cinema concept

cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "2026'nın En Beklenen Filmi", 
    "2026 yılı sinema sektörü için gişe rekorlarının kırılacağı bir yıl olacak! Peki sana göre 2026'da vizyona girecek bu dev yapımlardan hangisi daha heyecan verici? Tarafını seç!",
    main_cover_url,
    "Dizi & Film",
    "omu_bumu",
    0
))
oyun_id = cur.fetchone()[0]

dir_path = "static/img/movies_2026"
os.makedirs(dir_path, exist_ok=True)

for i, pair in enumerate(pairs):
    poster1 = get_poster(pair["m1"])
    poster2 = get_poster(pair["m2"])
    
    if not poster1 or poster1 == "N/A": poster1 = main_cover_url
    if not poster2 or poster2 == "N/A": poster2 = main_cover_url
    
    path1 = f"{dir_path}/{i}_1.jpg"
    path2 = f"{dir_path}/{i}_2.jpg"
    
    try:
        urllib.request.urlretrieve(poster1, path1)
        urllib.request.urlretrieve(poster2, path2)
    except:
        print(f"Failed to download for {pair['m1']} or {pair['m2']}, using URLs")
        path1 = poster1
        path2 = poster2
        
    final_path1 = f"/{path1}" if not path1.startswith("http") else path1
    final_path2 = f"/{path2}" if not path2.startswith("http") else path2
    
    resim_url = f"{final_path1},{final_path2}"
    secenekler = f"{pair['m1']},{pair['m2']}"
    dogru_cevap = "Farketmez"
    
    cur.execute('''
        INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
        VALUES (%s, %s, %s, %s)
    ''', (oyun_id, secenekler, dogru_cevap, resim_url))
    print(f"Added pair: {pair['m1']} vs {pair['m2']}")
    time.sleep(0.5)

conn.commit()
cur.close()
conn.close()
print("2026 Movies seeded successfully!")
