import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Update it to a nice unsplash image
image_url = 'https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?q=80&w=800&auto=format&fit=crop'
cur.execute("UPDATE oyun SET resim_url = %s WHERE baslik ILIKE '%%genel kültür%%';", (image_url,))
conn.commit()

cur.close()
conn.close()
print("Updated successfully!")
