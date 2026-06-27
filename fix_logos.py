import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

updates = {
    "Puma": "https://logo.clearbit.com/puma.com",
    "Lacoste": "https://logo.clearbit.com/lacoste.com",
    "BP": "https://logo.clearbit.com/bp.com",
    "Unilever": "https://logo.clearbit.com/unilever.com",
    "Playboy": "https://logo.clearbit.com/playboy.com"
}

# We need to find the game ID for "Kaç Logo Biliyorsun? (Zor Seviye)"
cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Kaç Logo Biliyorsun? (Zor Seviye)' ORDER BY id DESC LIMIT 1")
oyun = cur.fetchone()
if oyun:
    oyun_id = oyun[0]
    for brand, new_url in updates.items():
        # Because we randomized A, B, C, D we don't know which column has the brand.
        # BUT we know it's one of the options AND dogru_cevap points to it.
        # Actually we can just update the row where secenek_a = brand OR secenek_b = brand etc AND dogru_cevap points to that.
        # Simpler: The script inserted the correct answer into one of the options.
        # Let's just find the row where brand is in ANY option and update its resim_url.
        cur.execute("""
            UPDATE hangisi_soru 
            SET resim_url = %s 
            WHERE oyun_id = %s AND (
                (secenek_a = %s AND dogru_cevap = 'A') OR
                (secenek_b = %s AND dogru_cevap = 'B') OR
                (secenek_c = %s AND dogru_cevap = 'C') OR
                (secenek_d = %s AND dogru_cevap = 'D')
            )
        """, (new_url, oyun_id, brand, brand, brand, brand))

conn.commit()
cur.close()
conn.close()
print("Logos Fixed!")
