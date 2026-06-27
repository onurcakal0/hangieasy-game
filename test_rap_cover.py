import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id, baslik, resim_url FROM oyun WHERE baslik = 'Türkçe Rap: 5 Saniye Challenge'")
print(cur.fetchone())

conn.close()
