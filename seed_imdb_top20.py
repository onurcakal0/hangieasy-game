import os
import psycopg2
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. Insert Oyun
baslik = "IMDb Top 20: En İyi Film Hangisi?"
aciklama = "IMDb tarihinin en yüksek puanlı 20 başyapıtı karşı karşıya. Sana göre gelmiş geçmiş en iyi film hangisi?"
resim_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2000&auto=format&fit=crop"
kategori = "Kültür & Eğlence"
oyun_modu = "omu_bumu"

cur.execute(
    "INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi, bitirilme_sayisi) VALUES (%s, %s, %s, %s, %s, 0, 0) RETURNING id",
    (baslik, aciklama, resim_url, kategori, oyun_modu)
)
oyun_id = cur.fetchone()[0]

# 2. Matchups
matchups = [
    ("Esaretin Bedeli (1994)", "Baba (1972)"),
    ("Kara Şövalye (2008)", "Baba 2 (1974)"),
    ("12 Öfkeli Adam (1957)", "Schindler'in Listesi (1993)"),
    ("Yüzüklerin Efendisi: Kralın Dönüşü", "Ucuz Roman (1994)"),
    ("Yüzüklerin Efendisi: Yüzük Kardeşliği", "İyi, Kötü ve Çirkin (1966)"),
    ("Forrest Gump (1994)", "Dövüş Kulübü (1999)"),
    ("Yüzüklerin Efendisi: İki Kule", "Başlangıç (Inception)"),
    ("Yıldız Savaşları: İmparator", "The Matrix (1999)"),
    ("Sıkı Dostlar (Goodfellas)", "Guguk Kuşu (1975)"),
    ("Yedi (Se7en)", "Şahane Hayat (1946)")
]

for m in matchups:
    film1 = m[0]
    film2 = m[1]
    
    url1 = f"https://placehold.co/600x800/1a1a24/f1c40f?text={urllib.parse.quote(film1)}"
    url2 = f"https://placehold.co/600x800/1a1a24/f1c40f?text={urllib.parse.quote(film2)}"
    
    secenekler = f"{film1},{film2}"
    
    cur.execute(
        "INSERT INTO soru (oyun_id, resim_url, resim_url_2, secenekler) VALUES (%s, %s, %s, %s)",
        (oyun_id, url1, url2, secenekler)
    )

conn.commit()
cur.close()
conn.close()
print("IMDb Top 20 game seeded successfully!")
