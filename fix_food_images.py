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

def get_wiki_image_slow(title):
    try:
        time.sleep(2) # Prevent 429 Too Many Requests
        url = 'https://tr.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles=' + urllib.parse.quote(title)
        req = urllib.request.Request(url, headers={'User-Agent': 'HangiEasyBot/2.0 (Contact: onur@hangieasy.com)'})
        res = json.loads(urllib.request.urlopen(req).read().decode())
        pages = res['query']['pages']
        return list(pages.values())[0].get('original', {}).get('source', None)
    except Exception as e:
        print(f"Error fetching {title}: {e}")
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

print("Fixing Late Night Food tournament images...")

cur.execute("SELECT id FROM oyun WHERE baslik = %s LIMIT 1", ("Gece Acıkınca Yenilecek En İyi Yemek",))
res = cur.fetchone()
if not res:
    print("Game not found!")
    exit()
oyun_id = res[0]

# Some hardcoded fallbacks just in case wikipedia still fails
fallbacks = {
    "Hamburger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
    "Pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
    "Sosisli sandviç": "https://images.unsplash.com/photo-1590165482153-f5424df2a8fb?w=800",
    "Patates kızartması": "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=800",
    "Soğan halkası": "https://images.unsplash.com/photo-1639024470354-94c6e931ed8c?w=800"
}

dir_path = "static/img/late_night_food"
os.makedirs(dir_path, exist_ok=True)

main_cover_url = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=800&auto=format&fit=crop"

for i, pair in enumerate(pairs):
    poster1 = fallbacks.get(pair["f1"]) or get_wiki_image_slow(pair["f1"])
    poster2 = fallbacks.get(pair["f2"]) or get_wiki_image_slow(pair["f2"])
    
    if not poster1: poster1 = main_cover_url
    if not poster2: poster2 = main_cover_url
    
    path1 = f"{dir_path}/{i}_1.jpg"
    path2 = f"{dir_path}/{i}_2.jpg"
    
    try:
        req1 = urllib.request.Request(poster1, headers={'User-Agent': 'HangiEasyBot/2.0'})
        with open(path1, 'wb') as f: f.write(urllib.request.urlopen(req1).read())
        
        time.sleep(1)
        req2 = urllib.request.Request(poster2, headers={'User-Agent': 'HangiEasyBot/2.0'})
        with open(path2, 'wb') as f: f.write(urllib.request.urlopen(req2).read())
        print(f"Downloaded new images for {pair['f1']} vs {pair['f2']}")
    except Exception as e:
        print(f"Failed to download for {pair['f1']} or {pair['f2']}: {e}")
        
    final_path1 = f"/{path1}" if not path1.startswith("http") else path1
    final_path2 = f"/{path2}" if not path2.startswith("http") else path2
    
    resim_url = f"{final_path1},{final_path2}"
    secenekler = f"{pair['f1']},{pair['f2']}"
    
    cur.execute('''
        UPDATE soru 
        SET resim_url = %s
        WHERE oyun_id = %s AND secenekler = %s
    ''', (resim_url, oyun_id, secenekler))

conn.commit()
cur.close()
conn.close()
print("Food images updated successfully!")
