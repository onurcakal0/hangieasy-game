import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id, secenekler, dogru_cevap, resim_url, resim_url_2 FROM soru WHERE oyun_id = 19 LIMIT 2")
for row in cur.fetchall():
    print(row)

conn.close()
