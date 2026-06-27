import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE hangisi_soru ADD COLUMN zorluk_derecesi VARCHAR(20) DEFAULT 'Orta'")
    conn.commit()
    print("Column 'zorluk_derecesi' added successfully.")
except psycopg2.errors.DuplicateColumn:
    conn.rollback()
    print("Column already exists.")

cur.close()
conn.close()
