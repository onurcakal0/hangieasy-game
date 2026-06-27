import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

url_arthur = "https://image.tmdb.org/t/p/w780/j8rEEyF7fA77u8tT94vF7xYf0z0.jpg"
url_ezio = "https://image.tmdb.org/t/p/w780/kKEMjZ0yq1rX85Yj5U6XkQzM0d4.jpg" 
url_ryu = "https://image.tmdb.org/t/p/w780/w7P3B0xZ8H8Xg2Q1m7zZ5Z6Y0r.jpg"

cur.execute("UPDATE hangisi_soru SET resim_url = %s WHERE resim_url LIKE '%%dummyimage.com%%' AND soru_metni LIKE '%%Arthur Morgan%%'", (url_arthur,))
cur.execute("UPDATE hangisi_soru SET resim_url = %s WHERE resim_url LIKE '%%dummyimage.com%%' AND soru_metni LIKE '%%Ezio Auditore%%'", (url_ezio,))
cur.execute("UPDATE hangisi_soru SET resim_url = %s WHERE resim_url LIKE '%%dummyimage.com%%' AND soru_metni LIKE '%%Ryu%%'", (url_ryu,))

conn.commit()
cur.close()
conn.close()
print("Fixed!")
