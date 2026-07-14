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

def get_wiki_image(title):
    try:
        url = 'https://tr.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles=' + urllib.parse.quote(title)
        req = urllib.request.Request(url, headers={'User-Agent': 'HangiEasyBot/1.0'})
        res = json.loads(urllib.request.urlopen(req).read().decode())
        pages = res['query']['pages']
        return list(pages.values())[0].get('original', {}).get('source', None)
    except:
        return None

pairs = [
    {"f1": "Kokoreç", "f2": "Islak hamburger"},
    {"f1": "Çiğ köfte", "f2": "Midye dolma"},
    {"f1": "Döner", "f2": "Tantuni"},
    {"f1": "Lahmacun", "f2": "Pizza"},
    {"f1": "İşkembe çorbası", "f2": "Kelle paça"},
    {"f1": "Tost", "f2": "Gözleme"},
    {"f1": "Patates kızartması", "f2": "Soğan halkası"},
    {"f1": "Hamburger", "f2": "Sosisli sandviç"},
    {"f1": "Sucuk", "f2": "Pastırma"},
    {"f1": "Kumpir", "f2": "Boyoz"}
]

print("Creating Late Night Food tournament...")

main_cover_url = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=800&auto=format&fit=crop"

cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "Gece Acıkınca Yenilecek En İyi Yemek", 
    "Gece yarısı miden kazındı, dışarıdan sipariş vereceksin veya sokağa çıkıp bir şeyler yiyeceksin. Peki sana göre en iyi gece yemeği hangisi? O mu bu mu?",
    main_cover_url,
    "Eğlence",
    "omu_bumu",
    0
))
oyun_id = cur.fetchone()[0]

dir_path = "static/img/late_night_food"
os.makedirs(dir_path, exist_ok=True)

for i, pair in enumerate(pairs):
    poster1 = get_wiki_image(pair["f1"])
    poster2 = get_wiki_image(pair["f2"])
    
    if not poster1: poster1 = main_cover_url
    if not poster2: poster2 = main_cover_url
    
    path1 = f"{dir_path}/{i}_1.jpg"
    path2 = f"{dir_path}/{i}_2.jpg"
    
    try:
        req1 = urllib.request.Request(poster1, headers={'User-Agent': 'HangiEasyBot/1.0'})
        with open(path1, 'wb') as f: f.write(urllib.request.urlopen(req1).read())
        
        req2 = urllib.request.Request(poster2, headers={'User-Agent': 'HangiEasyBot/1.0'})
        with open(path2, 'wb') as f: f.write(urllib.request.urlopen(req2).read())
    except Exception as e:
        print(f"Failed to download for {pair['f1']} or {pair['f2']}: {e}")
        path1 = poster1
        path2 = poster2
        
    final_path1 = f"/{path1}" if not path1.startswith("http") else path1
    final_path2 = f"/{path2}" if not path2.startswith("http") else path2
    
    resim_url = f"{final_path1},{final_path2}"
    secenekler = f"{pair['f1']},{pair['f2']}"
    dogru_cevap = "Farketmez"
    
    cur.execute('''
        INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
        VALUES (%s, %s, %s, %s)
    ''', (oyun_id, secenekler, dogru_cevap, resim_url))
    print(f"Added pair: {pair['f1']} vs {pair['f2']}")
    time.sleep(0.5)

conn.commit()
cur.close()
conn.close()
print("Food tournament seeded successfully!")
