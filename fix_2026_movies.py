import urllib.request
import urllib.parse
import os
import psycopg2
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

def get_tmdb_poster(title):
    try:
        url = "https://www.themoviedb.org/search?query=" + urllib.parse.quote(title)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.select_one('img.poster')
        if img and img.has_attr('src'):
            src = img['src']
            if 'w94_and_h141_face' in src:
                return src.replace('w94_and_h141_face', 'w600_and_h900_bestv2')
        return None
    except Exception as e:
        print(f"Error fetching TMDB poster for {title}: {e}")
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

print("Fixing 2026 Movies tournament images from TMDB...")
main_cover_url = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=800&auto=format&fit=crop"
dir_path = "static/img/movies_2026"
os.makedirs(dir_path, exist_ok=True)

# Find the game id
cur.execute("SELECT id FROM oyun WHERE baslik = %s LIMIT 1", ("2026'nın En Beklenen Filmi",))
res = cur.fetchone()
if not res:
    print("Game not found!")
    exit()
oyun_id = res[0]

for i, pair in enumerate(pairs):
    poster1 = get_tmdb_poster(pair["m1"])
    poster2 = get_tmdb_poster(pair["m2"])
    
    if not poster1: poster1 = main_cover_url
    if not poster2: poster2 = main_cover_url
    
    path1 = f"{dir_path}/{i}_1.jpg"
    path2 = f"{dir_path}/{i}_2.jpg"
    
    try:
        urllib.request.urlretrieve(poster1, path1)
        urllib.request.urlretrieve(poster2, path2)
        print(f"Downloaded new TMDB images for {pair['m1']} vs {pair['m2']}")
    except Exception as e:
        print(f"Failed to download for {pair['m1']} or {pair['m2']}: {e}")
        
    final_path1 = f"/{path1}" if not path1.startswith("http") else path1
    final_path2 = f"/{path2}" if not path2.startswith("http") else path2
    
    resim_url = f"{final_path1},{final_path2}"
    secenekler = f"{pair['m1']},{pair['m2']}"
    
    cur.execute('''
        UPDATE soru 
        SET resim_url = %s
        WHERE oyun_id = %s AND secenekler = %s
    ''', (resim_url, oyun_id, secenekler))

conn.commit()
cur.close()
conn.close()
print("2026 Movies images updated successfully!")
