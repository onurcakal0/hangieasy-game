import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS boss_abone (
        id SERIAL PRIMARY KEY,
        eposta VARCHAR(120) NOT NULL,
        tarih TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()
cur.close()
conn.close()
print("BossAbone table created!")
