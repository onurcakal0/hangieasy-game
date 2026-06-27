import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS hangisi_oyun (
        id SERIAL PRIMARY KEY,
        baslik VARCHAR(200) NOT NULL,
        aciklama TEXT,
        resim_url VARCHAR(500),
        olusturan_id INTEGER,
        olusturan_adi VARCHAR(100) DEFAULT 'HangiEasy',
        oynanma_sayisi INTEGER DEFAULT 0,
        tarih TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS hangisi_soru (
        id SERIAL PRIMARY KEY,
        oyun_id INTEGER REFERENCES hangisi_oyun(id) ON DELETE CASCADE,
        soru_metni TEXT NOT NULL,
        resim_url VARCHAR(500),
        secenek_a VARCHAR(200) NOT NULL,
        secenek_b VARCHAR(200) NOT NULL,
        secenek_c VARCHAR(200) NOT NULL,
        secenek_d VARCHAR(200) NOT NULL,
        dogru_cevap VARCHAR(1) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS hangisi_skor (
        id SERIAL PRIMARY KEY,
        oyun_id INTEGER REFERENCES hangisi_oyun(id) ON DELETE CASCADE,
        kullanici_adi VARCHAR(100) NOT NULL,
        puan INTEGER NOT NULL,
        tarih TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS hangisi_tepki (
        id SERIAL PRIMARY KEY,
        oyun_id INTEGER REFERENCES hangisi_oyun(id) ON DELETE CASCADE,
        kullanici_adi VARCHAR(100) NOT NULL,
        tepki VARCHAR(50) NOT NULL,
        tarih TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()
cur.close()
conn.close()
print("Hangisi tables created successfully!")
