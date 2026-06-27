import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "Yapay Zeka Mı? Gerçek Mi?", 
    "Sadece en keskin gözler bu farkı anlayabilir! Gördüğün fotoğraf gerçek bir kare mi, yoksa yapay zeka ürünü mü? Hızına göre puan kazanacaksın!",
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=800&auto=format&fit=crop",
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

sorular = [
    # GERÇEK (Unsplash)
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1506744626753-eda818298751?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1534081333815-ae5019106622?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1542224566-6e85f2e6772f?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1470071131384-001b85755536?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    ("Bu görsel sence hangisi?", "https://images.unsplash.com/photo-1433086966358-54859d0ed716?q=80&w=600&auto=format&fit=crop", "Gerçek"),
    
    # YAPAY ZEKA
    # We will use some known generic AI placeholder URLs or realistic AI generated image links
    ("Bu görsel sence hangisi?", "https://creadaily.com/wp-content/uploads/2023/10/midjourney-v5-photorealism-1-1024x1024.jpg", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://creadaily.com/wp-content/uploads/2023/10/midjourney-v5-photorealism-2-1024x1024.jpg", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://creadaily.com/wp-content/uploads/2023/10/midjourney-v5-photorealism-3-1024x1024.jpg", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/09a0db83-d588-4660-8f9f-07efc8a514d7", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/1a00a1cb-8a4b-4a5d-b258-00a4b95f2a1b", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/2c3a5b32-e0c1-4b17-a068-d07f3cf16003", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/42a8292c-623b-48bc-b286-9a2eb2016335", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/745e43c5-f8ef-41cf-b816-5bc77b9487c6", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/a1d95d10-e51c-4e8c-85de-bfd28a39a7b9", "Yapay Zeka"),
    ("Bu görsel sence hangisi?", "https://image.lexica.art/full_jpg/e2b9c7b9-688a-4db5-9e6b-cf83a3f1248d", "Yapay Zeka")
]

import random
random.shuffle(sorular)

for s in sorular:
    # A -> Yapay Zeka, B -> Gerçek
    dogru = 'A' if s[2] == "Yapay Zeka" else 'B'
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, s[0], s[1], "🤖 Yapay Zeka", "🌍 Gerçek", "", "", dogru))

conn.commit()
cur.close()
conn.close()
print("Game Seeded Successfully!")
