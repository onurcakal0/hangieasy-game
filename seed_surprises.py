import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. Insert Oyun
baslik = "Dünya Kupaları Tarihinin En Büyük Sürprizi"
aciklama = "Futbol tarihinin gördüğü en büyük şoklardan hangisi daha inanılmazdı? En büyük mucizeyi seç!"
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

# 2. Matchups (Surprise 1, Country Code 1, Surprise 2, Country Code 2)
matchups = [
    ("S. Arabistan 2-1 Arjantin (2022)", "sa", "Senegal 1-0 Fransa (2002)", "sn"),
    ("G. Kore'nin İtalya'yı Elemesi (2002)", "kr", "Kuzey Kore 1-0 İtalya (1966)", "kp"),
    ("ABD 1-0 İngiltere (1950)", "us", "Kamerun 1-0 Arjantin (1990)", "cm"),
    ("Almanya 7-1 Brezilya (2014)", "de", "Hollanda 5-1 İspanya (2014)", "nl"),
    ("Fas'ın Yarı Finale Çıkması (2022)", "ma", "Kosta Rika'nın Peri Masalı (2014)", "cr"),
    ("Cezayir 2-1 Batı Almanya (1982)", "dz", "Güney Kore 2-0 Almanya (2018)", "kr"),
    ("Bulgaristan'ın Almanya'yı Elemesi (1994)", "bg", "Hırvatistan 3-0 Almanya (1998)", "hr"),
    ("Meksika 1-0 Almanya (2018)", "mx", "Japonya 2-1 İspanya (2022)", "jp"),
    ("Slovakya 3-2 İtalya (2010)", "sk", "İrlanda 1-0 İtalya (1994)", "ie"),
    ("G. Kore'nin İspanya'yı Elemesi (2002)", "kr", "İsviçre 1-0 İspanya (2010)", "ch"),
    ("Doğu Almanya 1-0 B. Almanya (1974)", "de", "K. İrlanda 1-0 İspanya (1982)", "gb-nir"),
    ("Küba'nın Romanya'yı Elemesi (1938)", "cu", "Gana 2-0 Çek Cumhuriyeti (2006)", "gh")
]

for s1, c1, s2, c2 in matchups:
    secenekler = f"{s1},{s2}"
    r_url = f"https://flagcdn.com/w640/{c1}.png,https://flagcdn.com/w640/{c2}.png"
    dogru_cevap = "Farketmez"
    cur.execute("""
        INSERT INTO soru (oyun_id, secenekler, resim_url, dogru_cevap) 
        VALUES (%s, %s, %s, %s);
    """, (oyun_id, secenekler, r_url, dogru_cevap))

conn.commit()
cur.close()
conn.close()

print(f"Surprises game seeded successfully with ID: {oyun_id}")
