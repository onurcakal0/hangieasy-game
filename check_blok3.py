import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id, resim_url FROM oyun WHERE baslik = 'Blok3 Ne Kadar Tanıyorsun?'")
oyun = cur.fetchone()
if not oyun:
    print("Blok3 oyunu bulunamadi!")
    exit()

oyun_id, resim_url = oyun
print(f"Blok3 oyun_id: {oyun_id}")
print(f"Kapak URL: {resim_url}")

cur.execute("SELECT id, dogru_cevap, secenekler, resim_url FROM soru WHERE oyun_id = %s ORDER BY id", (oyun_id,))
sorular = cur.fetchall()

for i, s in enumerate(sorular):
    print(f"Soru {i+1} (ID: {s[0]}):")
    print(f"  Doğru Cevap: {s[1]}")
    print(f"  Ses URL: {s[3]}")

conn.close()
