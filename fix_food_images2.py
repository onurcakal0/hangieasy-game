import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

image_map = {
    "Kokoreç": "https://images.unsplash.com/photo-1544025162-811c75c88b0a?w=800",
    "Islak hamburger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
    "Çiğ köfte": "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?w=800",
    "Midye dolma": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800",
    "Döner": "https://images.unsplash.com/photo-1529148482759-b35b25c5f217?w=800",
    "Tantuni": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=800",
    "Lahmacun": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800",
    "Pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
    "İşkembe çorbası": "https://images.unsplash.com/photo-1547592180-85f173990554?w=800",
    "Kelle paça": "https://images.unsplash.com/photo-1603105037880-880cd4136bd9?w=800",
    "Tost": "https://images.unsplash.com/photo-1528736235302-52922df5c122?w=800",
    "Gözleme": "https://images.unsplash.com/photo-1616641618783-a4e9bd7f7485?w=800",
    "Patates kızartması": "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=800",
    "Soğan halkası": "https://images.unsplash.com/photo-1639024470354-94c6e931ed8c?w=800",
    "Hamburger": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800",
    "Sosisli sandviç": "https://images.unsplash.com/photo-1590165482153-f5424df2a8fb?w=800",
    "Sucuk": "https://images.unsplash.com/photo-1608681423871-3316ccb6b379?w=800",
    "Pastırma": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800",
    "Kumpir": "https://images.unsplash.com/photo-1508213824874-95484cdcf31f?w=800",
    "Boyoz": "https://images.unsplash.com/photo-1577045138356-8c460d009e51?w=800"
}

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

cur.execute("SELECT id FROM oyun WHERE baslik = %s LIMIT 1", ("Gece Acıkınca Yenilecek En İyi Yemek",))
res = cur.fetchone()
oyun_id = res[0]

for pair in pairs:
    url1 = image_map[pair["f1"]]
    url2 = image_map[pair["f2"]]
    resim_url = f"{url1},{url2}"
    secenekler = f"{pair['f1']},{pair['f2']}"
    cur.execute('''
        UPDATE soru 
        SET resim_url = %s
        WHERE oyun_id = %s AND secenekler = %s
    ''', (resim_url, oyun_id, secenekler))

conn.commit()
cur.close()
conn.close()
print("Images fixed with static Unsplash URLs!")
