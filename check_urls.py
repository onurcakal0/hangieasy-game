import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT soru_metni, resim_url FROM hangisi_soru WHERE soru_metni LIKE '%ikonik karakter%'")
for r in cur.fetchall():
    print(r[0][:20], r[1])

conn.close()
