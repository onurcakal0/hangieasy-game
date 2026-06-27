import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

games_to_delete = [
    'Yapay Zeka Mı? Gerçek Mi?',
    'Kaç Logo Biliyorsun? (Zor Seviye)'
]

for title in games_to_delete:
    cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = %s", (title,))
    row = cur.fetchone()
    if row:
        oyun_id = row[0]
        # Delete related records to be safe (if no CASCADE)
        cur.execute("DELETE FROM hangisi_soru WHERE oyun_id = %s", (oyun_id,))
        cur.execute("DELETE FROM hangisi_skor WHERE oyun_id = %s", (oyun_id,))
        cur.execute("DELETE FROM hangisi_tepki WHERE oyun_id = %s", (oyun_id,))
        
        # Delete game
        cur.execute("DELETE FROM hangisi_oyun WHERE id = %s", (oyun_id,))
        print(f"Deleted game: {title}")

conn.commit()
cur.close()
conn.close()
