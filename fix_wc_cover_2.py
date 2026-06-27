import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Safe, reliable image for the game cover
image_url = "https://images.unsplash.com/photo-1574629810360-7efbb19255cb?q=80&w=800&auto=format&fit=crop"

cur.execute("UPDATE oyun SET resim_url = %s WHERE id = 23;", (image_url,))
conn.commit()

cur.close()
conn.close()
print("Cover fixed!")
