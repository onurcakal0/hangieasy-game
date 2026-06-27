import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Update all games in "World Cup 2026" category to have the official logo
# Using a high-quality generic URL for the World Cup 26 brand
image_url = "https://digitalhub.fifa.com/transform/c0199e43-e6d8-4f81-aab4-d832e8b61e2f/World-Cup-2026-Brand-Announcement-Los-Angeles?io=transform:fill,height:1080,width:1920"

cur.execute("UPDATE oyun SET resim_url = %s WHERE kategori = 'World Cup 2026';", (image_url,))
conn.commit()

cur.close()
conn.close()

print("Cover images updated successfully!")
