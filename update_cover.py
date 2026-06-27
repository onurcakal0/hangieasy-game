import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("UPDATE hangisi_oyun SET resim_url = %s WHERE baslik LIKE '%%5 Büyük Lig Logo%%'", ("/static/img/football_cover.png",))

conn.commit()
cur.close()
conn.close()
print("Cover image updated in DB!")
