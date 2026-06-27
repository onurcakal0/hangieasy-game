import urllib.request
import psycopg2
import os
from dotenv import load_dotenv

# Use a highly reliable wikipedia image for a football stadium
img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Wembley_Stadium_interior.jpg/800px-Wembley_Stadium_interior.jpg"
filepath = "static/img/football_cover.jpg"

print("Downloading cover image...")
req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
    out_file.write(response.read())

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("UPDATE hangisi_oyun SET resim_url = %s WHERE baslik LIKE '%5 Büyük Lig Logo%'", (f"/{filepath}",))

conn.commit()
cur.close()
conn.close()
print("Cover image fixed!")
