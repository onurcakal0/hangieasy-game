import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id, baslik, oyun_modu FROM oyun WHERE baslik LIKE '%15%' OR baslik ILIKE '%bütçe%' LIMIT 5")
for row in cur.fetchall():
    print(row)

conn.close()
