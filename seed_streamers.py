import os
import urllib.request
import json
import psycopg2
from dotenv import load_dotenv

streamers = [
    {"name": "Elraenn", "twitch": "elraenn", "price": 5},
    {"name": "Eray", "twitch": "eray", "price": 5},
    {"name": "Kendine Müzisyen", "twitch": "kendinemuzisyen", "price": 5},
    {"name": "Pqueen", "twitch": "pqueen", "price": 5},
    {"name": "wtcN", "twitch": "wtcn", "price": 3},
    {"name": "Jahrein", "twitch": "jahrein", "price": 3},
    {"name": "Hype", "twitch": "hype", "price": 3},
    {"name": "Anna Deniz", "twitch": "annadeniz", "price": 3},
    {"name": "Toqtir", "twitch": "toqtir", "price": 1},
    {"name": "Jrokez", "twitch": "jrokez", "price": 1},
    {"name": "RRaenee", "twitch": "rraenee", "price": 1},
    {"name": "Mithrain", "twitch": "mithrain", "price": 1} # Replaced Baboli with Mithrain for guaranteed image
]

def get_twitch_pfp(username):
    url = "https://gql.twitch.tv/gql"
    headers = {
        'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'Content-Type': 'application/json'
    }
    body = [{
        "operationName": "ChannelShell",
        "variables": {"login": username},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "580ab410bcd0c1ad194224957ae2241e5d252b2c5173d8e0cce9d32d5bb14efe"
            }
        }
    }]
    
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    res = urllib.request.urlopen(req).read().decode()
    data = json.loads(res)
    
    try:
        user = data[0]['data']['userOrError']
        if 'profileImageURL' in user:
            # Replace -70x70.png with -300x300.png for HD image
            return user['profileImageURL'].replace("-70x70.png", "-300x300.png").replace("-70x70.jpeg", "-300x300.jpeg").replace("-70x70.jpg", "-300x300.jpg")
    except Exception as e:
        pass
    return None

os.makedirs("static/img/streamers", exist_ok=True)

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Insert Game
cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "$15 Bütçe Savaşı: Kick TR Yayıncıları", 
    "Issız bir adaya düştün ve yanında hayatta kalmak için Kick Türkiye yayıncılarından oluşan bir ekip kurmalısın! Bütçen $15. Kadronu seç, adadan kurtul!",
    "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&q=80&w=800", # Island / Gaming setup
    "E-Spor & Yayıncı",
    "butce_savasi",
    0
))
oyun_id = cur.fetchone()[0]

for s in streamers:
    print(f"Fetching {s['name']}...")
    img_url = get_twitch_pfp(s['twitch'])
    local_url = f"https://dummyimage.com/300x300/151520/ffffff&text={s['name']}"
    
    if img_url:
        filepath = f"static/img/streamers/{s['twitch']}.jpg"
        try:
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img) as img_res, open(filepath, 'wb') as out_file:
                out_file.write(img_res.read())
            local_url = f"/{filepath}"
            print(f"Successfully downloaded {s['name']}")
        except Exception as e:
            print(f"Failed to download image for {s['name']}: {e}")
    else:
        print(f"Profile picture not found for {s['name']}")

    secenekler_verisi = f"{s['name']},Yayıncılar"
    
    cur.execute('''
        INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
        VALUES (%s, %s, %s, %s)
    ''', (oyun_id, secenekler_verisi, str(s['price']), local_url))

conn.commit()
cur.close()
conn.close()
print("Kick TR Budget War game seeded successfully!")
