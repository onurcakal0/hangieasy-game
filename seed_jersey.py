import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. Insert Oyun
baslik = "En Şık 2026 Dünya Kupası Forması"
aciklama = "Turnuvanın en iyi tasarıma sahip forması hangisi? Göz alıcı detaylar ve ikonik renkler çarpışıyor!"
resim_url = "/static/img/images.jpeg"
kategori = "World Cup 2026"
oyun_modu = "omu_bumu"

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
    ("Brezilya Forması", "br", "Arjantin Forması", "ar"),
    ("Fransa Forması", "fr", "İngiltere Forması", "gb-eng"),
    ("İtalya Forması", "it", "Almanya Forması", "de"),
    ("Portekiz Forması", "pt", "İspanya Forması", "es"),
    ("Hollanda Forması", "nl", "Belçika Forması", "be"),
    ("Türkiye Forması", "tr", "Hırvatistan Forması", "hr"),
    ("Meksika Forması", "mx", "ABD Forması", "us"),
    ("Japonya Forması", "jp", "Güney Kore Forması", "kr")
]

for t1, c1, t2, c2 in matchups:
    secenekler = f"{t1},{t2}"
    r_url = f"https://flagcdn.com/w640/{c1}.png,https://flagcdn.com/w640/{c2}.png"
    dogru_cevap = "Farketmez"
    cur.execute("""
        INSERT INTO soru (oyun_id, secenekler, resim_url, dogru_cevap) 
        VALUES (%s, %s, %s, %s);
    """, (oyun_id, secenekler, r_url, dogru_cevap))

conn.commit()
cur.close()
conn.close()

print(f"Jersey game seeded successfully with ID: {oyun_id}")
