import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. Insert Oyun
baslik = "Dünya Kupası 2026: Hangi Ülke Şampiyon Olur?"
aciklama = "Kupayı sence hangi dev kazanacak? Tarafını seç, favorini finale kadar taşı ve şampiyonu belirle!"
resim_url = "https://images.unsplash.com/photo-1574629810360-7efbb19255cb?q=80&w=1000&auto=format&fit=crop"
kategori = "World Cup 2026"
oyun_modu = "omu_bumu"

# Try to find a user to assign or default to 1 (usually admin)
cur.execute("SELECT id FROM kullanici ORDER BY id ASC LIMIT 1;")
admin_id_row = cur.fetchone()
admin_id = admin_id_row[0] if admin_id_row else 1

cur.execute("""
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, olusturan_id) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
""", (baslik, aciklama, resim_url, kategori, oyun_modu, admin_id))
oyun_id = cur.fetchone()[0]

# 2. Matchups
matchups = [
    ("Brezilya", "br", "Almanya", "de"),
    ("Arjantin", "ar", "İspanya", "es"),
    ("Fransa", "fr", "İtalya", "it"),
    ("İngiltere", "gb-eng", "Portekiz", "pt"),
    ("Hollanda", "nl", "Belçika", "be"),
    ("Türkiye", "tr", "Hırvatistan", "hr"),
    ("Uruguay", "uy", "Kolombiya", "co"),
    ("Japonya", "jp", "Fas", "ma")
]

for t1, c1, t2, c2 in matchups:
    secenekler = f"{t1},{t2}"
    r_url = f"https://flagcdn.com/w320/{c1}.png,https://flagcdn.com/w320/{c2}.png"
    dogru_cevap = "Farketmez"
    cur.execute("""
        INSERT INTO soru (oyun_id, secenekler, resim_url, dogru_cevap) 
        VALUES (%s, %s, %s, %s);
    """, (oyun_id, secenekler, r_url, dogru_cevap))

conn.commit()
cur.close()
conn.close()

print(f"Game seeded successfully with ID: {oyun_id}")
