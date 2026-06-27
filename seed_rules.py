import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. Insert Oyun
baslik = "Futbolun Yeni Kuralları: Hangisi Daha İyi?"
aciklama = "Dünya Kupası ile birlikte futbola devrim niteliğinde yeni kurallar geldi. Sence oyunun kaderini değiştiren en iyi kural hangisi?"
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
    ("Yarı Otomatik Ofsayt Sistemi (SAOT)", "VAR Kararlarının Stadyuma Anons Edilmesi"),
    ("Sadece Kaptanların Hakemle Konuşabilmesi", "Mavi Kart ve 10 Dakika Oyundan Çıkma (Sin Bin)"),
    ("5 Oyuncu Değişikliği Hakkı", "Tam Zamanlı Oynatma (10+ Dk Uzatmalar)"),
    ("Ayakla Taç Atışı Kullanımı (Deneme)", "Kalecilerin Penaltıda Dikkat Dağıtamaması")
]

generic_img = "/static/img/images.jpeg"

for rule1, rule2 in matchups:
    secenekler = f"{rule1},{rule2}"
    r_url = f"{generic_img},{generic_img}"
    dogru_cevap = "Farketmez"
    cur.execute("""
        INSERT INTO soru (oyun_id, secenekler, resim_url, dogru_cevap) 
        VALUES (%s, %s, %s, %s);
    """, (oyun_id, secenekler, r_url, dogru_cevap))

conn.commit()
cur.close()
conn.close()

print(f"Rules game seeded successfully with ID: {oyun_id}")
