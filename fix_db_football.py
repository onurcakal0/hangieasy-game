import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik LIKE '%5 Büyük Lig Logo%' LIMIT 1")
row = cur.fetchone()
if not row:
    print("Oyun bulunamadı")
    exit()

oyun_id = row[0]

# Fix RC Lens (idx 19)
cur.execute(f"UPDATE hangisi_soru SET resim_url = %s WHERE oyun_id = %s AND (secenek_a = %s OR secenek_b = %s OR secenek_c = %s OR secenek_d = %s)", 
    (f"/static/img/football_logos/logo_{oyun_id}_19.jpg", oyun_id, "RC Lens", "RC Lens", "RC Lens", "RC Lens"))

# Fix OGC Nice (idx 20)
cur.execute(f"UPDATE hangisi_soru SET resim_url = %s WHERE oyun_id = %s AND (secenek_a = %s OR secenek_b = %s OR secenek_c = %s OR secenek_d = %s)", 
    (f"/static/img/football_logos/logo_{oyun_id}_20.jpg", oyun_id, "OGC Nice", "OGC Nice", "OGC Nice", "OGC Nice"))

# Fix RCD Mallorca (idx 24)
cur.execute(f"UPDATE hangisi_soru SET resim_url = %s WHERE oyun_id = %s AND (secenek_a = %s OR secenek_b = %s OR secenek_c = %s OR secenek_d = %s)", 
    (f"/static/img/football_logos/logo_{oyun_id}_24.jpg", oyun_id, "RCD Mallorca", "RCD Mallorca", "RCD Mallorca", "RCD Mallorca"))

conn.commit()
cur.close()
conn.close()
print("Database updated for RC Lens, OGC Nice, RCD Mallorca")
