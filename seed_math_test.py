import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Create the Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s) RETURNING id
''', (
    "Kafa Karıştıran 4 İşlem Testi", 
    "Sadece 10 saniyen var! Gittikçe zorlaşan matematik işlemlerini kafadan çözebilecek misin?",
    "https://images.unsplash.com/photo-1509228468518-180dd4864904?q=80&w=800&auto=format&fit=crop", # Math blackboard
    "HangiEasy",
    0
))
oyun_id = cur.fetchone()[0]

sorular = [
    # Seviye 1: Çok Kolay (Q1-Q4)
    {"q": "15 + 18 = ?", "opts": ["33", "32", "23", "43"], "ans": "A"},
    {"q": "45 - 23 = ?", "opts": ["12", "22", "32", "28"], "ans": "B"},
    {"q": "8 x 7 = ?", "opts": ["48", "54", "56", "64"], "ans": "C"},
    {"q": "72 ÷ 8 = ?", "opts": ["8", "7", "12", "9"], "ans": "D"},
    
    # Seviye 2: Kolay-Orta (Q5-Q8)
    {"q": "35 + 48 - 12 = ?", "opts": ["71", "61", "81", "73"], "ans": "A"},
    {"q": "12 x 5 + 15 = ?", "opts": ["65", "75", "60", "85"], "ans": "B"},
    {"q": "(18 + 14) x 2 = ?", "opts": ["44", "54", "64", "62"], "ans": "C"},
    {"q": "150 ÷ 5 + 45 = ?", "opts": ["65", "70", "80", "75"], "ans": "D"},
    
    # Seviye 3: Orta (Q9-Q12)
    {"q": "120 - (45 + 25) = ?", "opts": ["50", "40", "60", "45"], "ans": "A"},
    {"q": "14 x 6 - 24 = ?", "opts": ["50", "60", "70", "84"], "ans": "B"},
    {"q": "(65 + 35) ÷ 4 = ?", "opts": ["20", "30", "25", "40"], "ans": "C"},
    {"q": "180 ÷ (12 - 3) = ?", "opts": ["18", "15", "12", "20"], "ans": "D"},
    
    # Seviye 4: Orta-Zor (Q13-Q16)
    {"q": "25 x 4 + 15 x 3 = ?", "opts": ["145", "135", "125", "155"], "ans": "A"},
    {"q": "320 ÷ 8 + 45 x 2 = ?", "opts": ["120", "130", "110", "140"], "ans": "B"},
    {"q": "85 - (15 x 4) + 20 = ?", "opts": ["35", "55", "45", "65"], "ans": "C"},
    {"q": "16 x 5 - 120 ÷ 3 = ?", "opts": ["50", "30", "60", "40"], "ans": "D"},
    
    # Seviye 5: Zor (Q17-Q20)
    {"q": "23 x 14 = ?", "opts": ["322", "312", "332", "342"], "ans": "A"},
    {"q": "125 + 85 - 45 x 2 = ?", "opts": ["110", "120", "130", "140"], "ans": "B"},
    {"q": "(340 ÷ 17) + 85 = ?", "opts": ["95", "115", "105", "125"], "ans": "C"},
    {"q": "15 x (12 - 4) + 110 = ?", "opts": ["240", "220", "210", "230"], "ans": "D"}
]

for s in sorular:
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, s["q"], s["opts"][0], s["opts"][1], s["opts"][2], s["opts"][3], s["ans"]))

conn.commit()
cur.close()
conn.close()
print("Kafa Karıştıran 4 İşlem Testi başarıyla eklendi!")
