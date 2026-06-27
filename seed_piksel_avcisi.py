import os
import psycopg2
import random
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# All 48 teams
teams = [
    ("ABD", "us"), ("Kanada", "ca"), ("Meksika", "mx"),
    ("Fransa", "fr"), ("İngiltere", "gb-eng"), ("İspanya", "es"), ("Almanya", "de"),
    ("Portekiz", "pt"), ("İtalya", "it"), ("Hollanda", "nl"), ("Hırvatistan", "hr"),
    ("Belçika", "be"), ("Türkiye", "tr"), ("İsviçre", "ch"), ("Danimarka", "dk"),
    ("Avusturya", "at"), ("Sırbistan", "rs"), ("Polonya", "pl"), ("İsveç", "se"),
    ("Arjantin", "ar"), ("Brezilya", "br"), ("Uruguay", "uy"), ("Kolombiya", "co"),
    ("Ekvador", "ec"), ("Venezuela", "ve"), ("Kosta Rika", "cr"), ("Jamaika", "jm"),
    ("Panama", "pa"), ("Fas", "ma"), ("Senegal", "sn"), ("Mısır", "eg"),
    ("Cezayir", "dz"), ("Fildişi Sahili", "ci"), ("Nijerya", "ng"), ("Kamerun", "cm"),
    ("Mali", "ml"), ("Gana", "gh"), ("Japonya", "jp"), ("Güney Kore", "kr"),
    ("İran", "ir"), ("Suudi Arabistan", "sa"), ("Avustralya", "au"), ("Katar", "qa"),
    ("Özbekistan", "uz"), ("BAE", "ae"), ("Yeni Zelanda", "nz"), ("Peru", "pe"),
    ("Galler", "gb-wls")
]

# 1. Insert Oyun
baslik = "Dünya Kupası 2026: Bulanık Bayrak Avı"
aciklama = "Turnuvaya katılan devlerin bayrakları gizlendi. Piksel avcısı yeteneklerini kullan ve gizli ülkeyi bul!"
resim_url = "https://digitalhub.fifa.com/transform/c0199e43-e6d8-4f81-aab4-d832e8b61e2f/World-Cup-2026-Brand-Announcement-Los-Angeles?io=transform:fill,height:1080,width:1920"
kategori = "World Cup 2026"
oyun_modu = "piksel_avcisi"

cur.execute("SELECT id FROM kullanici ORDER BY id ASC LIMIT 1;")
admin_id_row = cur.fetchone()
admin_id = admin_id_row[0] if admin_id_row else 1

cur.execute("""
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, olusturan_id) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
""", (baslik, aciklama, resim_url, kategori, oyun_modu, admin_id))
oyun_id = cur.fetchone()[0]

# Pick 10 random questions
selected_teams = random.sample(teams, 10)

for team_name, team_code in selected_teams:
    # 3 random wrong options
    wrong_teams = [t for t in teams if t[0] != team_name]
    wrong_choices = random.sample(wrong_teams, 3)
    
    options = [team_name] + [t[0] for t in wrong_choices]
    random.shuffle(options)
    
    secenekler = ", ".join(options)
    r_url = f"https://flagcdn.com/w640/{team_code}.png"
    dogru_cevap = team_name
    
    cur.execute("""
        INSERT INTO soru (oyun_id, secenekler, resim_url, dogru_cevap) 
        VALUES (%s, %s, %s, %s);
    """, (oyun_id, secenekler, r_url, dogru_cevap))

conn.commit()
cur.close()
conn.close()

print(f"Piksel avcisi game seeded successfully with ID: {oyun_id}")
