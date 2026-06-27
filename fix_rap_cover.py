import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("UPDATE oyun SET resim_url = '/static/img/games/rap_cover.jpg' WHERE baslik = 'Türkçe Rap: 5 Saniye Challenge'")
conn.commit()

conn.close()
print("Cover updated!")
