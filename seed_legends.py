import os
import psycopg2
import requests
import time
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

def get_player_image(name):
    url = f'https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={name}'
    try:
        res = requests.get(url).json()
        if res and res.get('player'):
            thumb = res['player'][0].get('strThumb')
            if thumb:
                return thumb
            cutout = res['player'][0].get('strCutout')
            if cutout:
                return cutout
            render = res['player'][0].get('strRender')
            if render:
                return render
    except Exception as e:
        print(f"Error fetching {name}: {e}")
    # Fallback to generic silhouette
    return "https://cdn.pixabay.com/photo/2014/04/03/10/53/football-311746_1280.png"

# Zidane cover
zidane_cover = get_player_image("Zinedine Zidane")

# 1. Insert Oyun
baslik = "Dünya Kupası Efsaneleri"
aciklama = "Dünya Kupası tarihine damga vurmuş 24 efsane futbolcu karşı karşıya! Senin için en büyük efsane kim?"
kategori = "World Cup 2026"
oyun_modu = "omu_bumu"

cur.execute("SELECT id FROM kullanici ORDER BY id ASC LIMIT 1;")
admin_id_row = cur.fetchone()
admin_id = admin_id_row[0] if admin_id_row else 1

cur.execute("""
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, olusturan_id) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
""", (baslik, aciklama, zidane_cover, kategori, oyun_modu, admin_id))
oyun_id = cur.fetchone()[0]

legends = [
    "Pele", "Diego Maradona", "Zinedine Zidane", "Ronaldo",
    "Lionel Messi", "Cristiano Ronaldo", "Franz Beckenbauer", "Johan Cruyff",
    "Gerd Muller", "Miroslav Klose", "Michel Platini", "Garrincha",
    "Ronaldinho", "Andres Iniesta", "Xavi", "Romario",
    "Roberto Baggio", "Paolo Rossi", "Cafu", "Roberto Carlos",
    "Lothar Matthaus", "Paolo Maldini", "Fabio Cannavaro", "Bobby Charlton"
]

# Fetch images
player_images = {}
for p in legends:
    player_images[p] = get_player_image(p)
    time.sleep(0.1) # Be nice to API

# Matchups (12 pairs)
matchups = [
    (legends[0], legends[1]),
    (legends[2], legends[3]),
    (legends[4], legends[5]),
    (legends[6], legends[7]),
    (legends[8], legends[9]),
    (legends[10], legends[11]),
    (legends[12], legends[13]),
    (legends[14], legends[15]),
    (legends[16], legends[17]),
    (legends[18], legends[19]),
    (legends[20], legends[21]),
    (legends[22], legends[23])
]

for p1, p2 in matchups:
    secenekler = f"{p1},{p2}"
    r_url = f"{player_images[p1]},{player_images[p2]}"
    dogru_cevap = "Farketmez"
    cur.execute("""
        INSERT INTO soru (oyun_id, secenekler, resim_url, dogru_cevap) 
        VALUES (%s, %s, %s, %s);
    """, (oyun_id, secenekler, r_url, dogru_cevap))

conn.commit()
cur.close()
conn.close()

print(f"Legends game seeded successfully with ID: {oyun_id}")
