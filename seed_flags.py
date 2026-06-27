import os
import psycopg2
from dotenv import load_dotenv
import random

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

countries = [
    # Easy
    {"code": "tr", "correct": "Türkiye", "wrongs": ["Tunus", "Kuzey Kıbrıs", "Fas"]},
    {"code": "us", "correct": "Amerika Birleşik Devletleri", "wrongs": ["İngiltere", "Avustralya", "Yeni Zelanda"]},
    {"code": "gb", "correct": "Birleşik Krallık", "wrongs": ["Avustralya", "Amerika Birleşik Devletleri", "Fransa"]},
    {"code": "de", "correct": "Almanya", "wrongs": ["Belçika", "Avusturya", "Hollanda"]},
    {"code": "fr", "correct": "Fransa", "wrongs": ["İtalya", "Rusya", "Hollanda"]},
    {"code": "it", "correct": "İtalya", "wrongs": ["İrlanda", "Meksika", "Bulgaristan"]},
    {"code": "jp", "correct": "Japonya", "wrongs": ["Güney Kore", "Bangladeş", "Çin"]},
    {"code": "ca", "correct": "Kanada", "wrongs": ["Peru", "Lübnan", "Japonya"]},
    {"code": "br", "correct": "Brezilya", "wrongs": ["Arjantin", "Portekiz", "Kolombiya"]},
    {"code": "ru", "correct": "Rusya", "wrongs": ["Fransa", "Sırbistan", "Hırvatistan"]},
    {"code": "cn", "correct": "Çin", "wrongs": ["Vietnam", "Kuzey Kore", "Tayvan"]},
    {"code": "es", "correct": "İspanya", "wrongs": ["Portekiz", "Meksika", "Kolombiya"]},
    
    # Medium
    {"code": "kr", "correct": "Güney Kore", "wrongs": ["Japonya", "Kuzey Kore", "Çin"]},
    {"code": "ar", "correct": "Arjantin", "wrongs": ["Uruguay", "El Salvador", "Nikaragua"]},
    {"code": "mx", "correct": "Meksika", "wrongs": ["İtalya", "İspanya", "Peru"]},
    {"code": "au", "correct": "Avustralya", "wrongs": ["Yeni Zelanda", "Birleşik Krallık", "Amerika Birleşik Devletleri"]},
    {"code": "in", "correct": "Hindistan", "wrongs": ["Nijer", "İrlanda", "Fildişi Sahili"]},
    {"code": "gr", "correct": "Yunanistan", "wrongs": ["Kıbrıs", "Uruguay", "Arjantin"]},
    {"code": "se", "correct": "İsveç", "wrongs": ["Norveç", "Finlandiya", "Danimarka"]},
    {"code": "ch", "correct": "İsviçre", "wrongs": ["Avusturya", "İsveç", "Polonya"]},
    {"code": "eg", "correct": "Mısır", "wrongs": ["Suriye", "Irak", "Yemen"]},
    {"code": "za", "correct": "Güney Afrika", "wrongs": ["Zimbabve", "Nijerya", "Kenya"]},
    
    # Hard
    {"code": "bt", "correct": "Bhutan", "wrongs": ["Tibet", "Nepal", "Myanmar"]},
    {"code": "np", "correct": "Nepal", "wrongs": ["Bhutan", "Moğolistan", "Bangladeş"]},
    {"code": "sc", "correct": "Seyşeller", "wrongs": ["Mauritius", "Maldivler", "Bahamalar"]},
    {"code": "kz", "correct": "Kazakistan", "wrongs": ["Özbekistan", "Türkmenistan", "Kırgızistan"]},
    {"code": "lk", "correct": "Sri Lanka", "wrongs": ["Hindistan", "Maldivler", "Malezya"]},
    {"code": "mz", "correct": "Mozambik", "wrongs": ["Angola", "Zambiya", "Tanzanya"]},
    {"code": "gb-wls", "correct": "Galler", "wrongs": ["İskoçya", "İrlanda", "Bhutan"]},
    {"code": "jm", "correct": "Jamaika", "wrongs": ["Gana", "Senegal", "Etiyopya"]},
    {"code": "ke", "correct": "Kenya", "wrongs": ["Uganda", "Tanzanya", "Etiyopya"]},
    {"code": "al", "correct": "Arnavutluk", "wrongs": ["Karadağ", "Makedonya", "Sırbistan"]},
    {"code": "va", "correct": "Vatikan", "wrongs": ["San Marino", "İsviçre", "Malta"]},
    {"code": "lb", "correct": "Lübnan", "wrongs": ["Suriye", "Ürdün", "Kıbrıs"]},
    {"code": "mn", "correct": "Moğolistan", "wrongs": ["Kazakistan", "Çin", "Kırgızistan"]}
]

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "Dünya Bayrakları Sınavı", 
    "Kolaydan zora doğru 35 ülke! Bu bayrakların hangi ülkeye ait olduğunu 20 saniye içinde bulabilecek misin?",
    "https://flagcdn.com/w2560/un.png", # United Nations flag as cover
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

for c in countries:
    img_url = f"https://flagcdn.com/w640/{c['code']}.png"
    options = c['wrongs'] + [c['correct']]
    random.shuffle(options)
    
    dogru_harf = ""
    if options[0] == c['correct']: dogru_harf = "A"
    elif options[1] == c['correct']: dogru_harf = "B"
    elif options[2] == c['correct']: dogru_harf = "C"
    else: dogru_harf = "D"
    
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, "Bu bayrak hangi ülkeye ait?", img_url, options[0], options[1], options[2], options[3], dogru_harf))

conn.commit()
cur.close()
conn.close()
print("Flag Quiz Seeded Successfully!")
