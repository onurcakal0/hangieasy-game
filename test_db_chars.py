import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id, secenek_a, dogru_cevap FROM hangisi_soru WHERE secenek_a IS NOT NULL LIMIT 10")
for row in cur.fetchall():
    print(row)

conn.close()
