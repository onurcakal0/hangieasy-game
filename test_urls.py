import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT resim_url FROM hangisi_soru LIMIT 10")
rows = cur.fetchall()
for r in rows:
    print(r[0])

conn.close()
