import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Replace clearbit with icon.horse in hangisi_soru table
cur.execute("SELECT id, resim_url FROM hangisi_soru WHERE resim_url LIKE '%logo.clearbit.com%'")
rows = cur.fetchall()
for r in rows:
    old_url = r[1]
    # old_url = https://logo.clearbit.com/apple.com
    domain = old_url.split('/')[-1]
    new_url = f"https://icon.horse/icon/{domain}"
    cur.execute("UPDATE hangisi_soru SET resim_url = %s WHERE id = %s", (new_url, r[0]))

conn.commit()
cur.close()
conn.close()
print("Fixed Clearbit downtime with Icon Horse!")
