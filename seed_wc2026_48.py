import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

oyun_id = 22

# Clear old questions
cur.execute("DELETE FROM soru WHERE oyun_id = %s;", (oyun_id,))

matchups = [
    ("ABD", "us", "Meksika", "mx"),
    ("Kanada", "ca", "Kosta Rika", "cr"),
    ("Brezilya", "br", "Arjantin", "ar"),
    ("Fransa", "fr", "Almanya", "de"),
    ("İngiltere", "gb-eng", "İspanya", "es"),
    ("İtalya", "it", "Hollanda", "nl"),
    ("Portekiz", "pt", "Belçika", "be"),
    ("Türkiye", "tr", "Sırbistan", "rs"),
    ("Uruguay", "uy", "Kolombiya", "co"),
    ("Japonya", "jp", "Güney Kore", "kr"),
    ("Fas", "ma", "Senegal", "sn"),
    ("Mısır", "eg", "Cezayir", "dz"),
    ("Fildişi Sahili", "ci", "Nijerya", "ng"),
    ("İran", "ir", "Suudi Arabistan", "sa"),
    ("Avustralya", "au", "Yeni Zelanda", "nz"),
    ("Hırvatistan", "hr", "İsviçre", "ch"),
    ("Danimarka", "dk", "İsveç", "se"),
    ("Polonya", "pl", "Avusturya", "at"),
    ("Ekvador", "ec", "Venezuela", "ve"),
    ("Jamaika", "jm", "Panama", "pa"),
    ("Kamerun", "cm", "Gana", "gh"),
    ("Katar", "qa", "BAE", "ae"),
    ("Özbekistan", "uz", "Mali", "ml"),
    ("Peru", "pe", "Galler", "gb-wls")
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

print(f"48 Teams seeded successfully into game ID: {oyun_id}")
