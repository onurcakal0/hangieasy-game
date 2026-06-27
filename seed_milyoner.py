import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

oyun_baslik = "Kim HE-Coin'er Olmak İster?"
cur.execute("DELETE FROM hangisi_oyun WHERE baslik = %s", (oyun_baslik,))

cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    oyun_baslik, 
    "Efsanevi yarışma formatı HangiEasy'de! Bilgini test et, 15 soruyu bil ve 1.000.000 HE-Coin ödülün sahibi ol. Joker haklarını akıllıca kullan!",
    "https://images.unsplash.com/photo-1578269174936-2709b6aeb913?auto=format&fit=crop&q=80&w=800", # Studio/lights image
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

sorular = [
    # 1-5 (Çok Kolay)
    ("Hangisi bir meyvedir?", "Elma", "Patates", "Havuç", "Kereviz", "A"),
    ("Türkiye'nin başkenti neresidir?", "Ankara", "İstanbul", "İzmir", "Bursa", "A"),
    ("Alfabemizin ilk harfi nedir?", "A", "B", "C", "D", "A"),
    ("Güneş sistemimizde Dünyaya en yakın yıldız hangisidir?", "Güneş", "Kutup Yıldızı", "Sirius", "Vega", "A"),
    ("Hangisi bir sosyal medya platformudur?", "Instagram", "Excel", "Word", "Photoshop", "A"),
    
    # 6-10 (Orta)
    ("Mona Lisa tablosu hangi ünlü ressama aittir?", "Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet", "A"),
    ("Hangi kıta hem Kuzey hem de Güney yarımkürede yer alır?", "Afrika", "Avrupa", "Kuzey Amerika", "Avustralya", "A"),
    ("Mustafa Kemal Atatürk'ün doğum yeri olan Selanik, günümüzde hangi ülkenin sınırları içerisindedir?", "Yunanistan", "Bulgaristan", "Makedonya", "Arnavutluk", "A"),
    ("Periyodik cetvelde O simgesiyle gösterilen element hangisidir?", "Oksijen", "Osmiyum", "Altın", "Karbon", "A"),
    ("Nobel ödülleri hangi ülkede dağıtılmaktadır?", "İsveç", "Norveç", "İsviçre", "Danimarka", "A"),
    
    # 11-13 (Zor)
    ("Kıbrıs Barış Harekatı hangi yıl gerçekleşmiştir?", "1974", "1960", "1983", "1954", "A"),
    ("Dünyanın en uzun akarsuyu hangisidir?", "Nil", "Amazon", "Yangtze", "Mississippi", "A"),
    ("Türkiye'nin uluslararası internet alan adı (domain) uzantısı nedir?", ".tr", ".tc", ".tu", ".tur", "A"),
    
    # 14 (Çok Zor)
    ("Romen rakamlarında 'L' harfi hangi sayıyı ifade eder?", "50", "100", "500", "1000", "A"),
    
    # 15 (Milyonluk Soru)
    ("Tarihte bilinen ilk yazılı antlaşma olan Kadeş Antlaşması hangi iki devlet arasında imzalanmıştır?", "Mısırlılar - Hititler", "Sümerler - Akadlar", "Romalılar - Kartacalılar", "Persler - Yunanlar", "A")
]

import random
for q in sorular:
    soru_metni = q[0]
    secenekler = [q[1], q[2], q[3], q[4]]
    dogru_cevap = q[1] # The first one is always the correct answer in the tuple above
    
    random.shuffle(secenekler)
    
    dogru_harf = ""
    if secenekler[0] == dogru_cevap: dogru_harf = "A"
    elif secenekler[1] == dogru_cevap: dogru_harf = "B"
    elif secenekler[2] == dogru_cevap: dogru_harf = "C"
    else: dogru_harf = "D"
    
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, soru_metni, secenekler[0], secenekler[1], secenekler[2], secenekler[3], dogru_harf))

conn.commit()
cur.close()
conn.close()
print("Kim HE-Coin'er Olmak İster? Seeded Successfully!")
