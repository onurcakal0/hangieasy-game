import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

image_url = "/static/img/images.jpeg"

cur.execute("UPDATE oyun SET resim_url = %s WHERE kategori = 'World Cup 2026';", (image_url,))
conn.commit()

cur.close()
conn.close()
print("Cover fixed using local image!")
