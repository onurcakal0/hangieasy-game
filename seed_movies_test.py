import os
import psycopg2
from dotenv import load_dotenv
import random

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "Resimdeki Filmi Tahmin Edebilir Misin?", 
    "Sadece gerçek sinema gurmeleri 20'de 20 yapabilir! Afişe veya görsele bak, 4 şık arasından doğru filmi bul. Süren 20 saniye!",
    "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=800&auto=format&fit=crop", # Cinema popcorn or film roll image
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

sorular_data = [
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
        "correct": "Baba (The Godfather)",
        "wrongs": ["Sıkı Dostlar", "Yaralı Yüz (Scarface)", "Ucuz Roman"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/1/18/Titanic_%281997_film%29_poster.png",
        "correct": "Titanik",
        "wrongs": ["Aşk Gemisi", "Büyük İskender", "Pearl Harbor"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/d/d6/Avatar_%282009_film%29_poster.jpg",
        "correct": "Avatar",
        "wrongs": ["Marslı", "Uzay Yolu", "Yıldız Savaşları"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
        "correct": "Kara Şövalye",
        "wrongs": ["Örümcek Adam", "Demir Adam", "Yenilmezler"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
        "correct": "Forrest Gump",
        "wrongs": ["Yeşil Yol", "Er Ryan'ı Kurtarmak", "Esaretin Bedeli"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
        "correct": "The Matrix",
        "wrongs": ["Başlangıç (Inception)", "Bıçak Sırtı", "Terminatör"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
        "correct": "Başlangıç (Inception)",
        "wrongs": ["Zindan Adası", "Yıldızlararası", "Prestij"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/b/be/The_Lord_of_the_Rings_-_The_Return_of_the_King_%282003%29.jpg",
        "correct": "Yüzüklerin Efendisi",
        "wrongs": ["Harry Potter", "Hobbit", "Game of Thrones"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
        "correct": "Yıldızlararası",
        "wrongs": ["Yerçekimi", "Marslı", "Geliş (Arrival)"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/7/7a/Harry_Potter_and_the_Philosopher%27s_Stone_banner.gif",
        "correct": "Harry Potter",
        "wrongs": ["Yüzüklerin Efendisi", "Narnia Günlükleri", "Percy Jackson"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/f/f9/TheAvengers2012Poster.jpg",
        "correct": "Yenilmezler (Avengers)",
        "wrongs": ["Adalet Birliği (Justice League)", "X-Men", "Galaksinin Koruyucuları"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/e/e7/Jurassic_Park_poster.jpg",
        "correct": "Jurassic Park",
        "wrongs": ["King Kong", "Godzilla", "Indiana Jones"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/8/87/StarWarsMoviePoster1977.jpg",
        "correct": "Yıldız Savaşları (Star Wars)",
        "wrongs": ["Uzay Yolu (Star Trek)", "Dune", "Galaksinin Koruyucuları"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/f/f3/Spider-Man2002Poster.jpg",
        "correct": "Örümcek Adam",
        "wrongs": ["Batman", "Süpermen", "Flash"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/e/e1/Joker_%282019_film%29_poster.jpg",
        "correct": "Joker",
        "wrongs": ["Kara Şövalye", "Venom", "Deadpool"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3d/The_Lion_King_poster.jpg",
        "correct": "Aslan Kral",
        "wrongs": ["Madagaskar", "Buz Devri", "Oyuncak Hikayesi"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/f/fb/Gladiator_%282000_film_poster%29.png",
        "correct": "Gladyatör",
        "wrongs": ["Truva", "Cesur Yürek", "300 Spartalı"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/d/d2/Back_to_the_Future.jpg",
        "correct": "Geleceğe Dönüş",
        "wrongs": ["Terminatör", "E.T.", "Indiana Jones"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/3/3b/Pulp_Fiction_%281994%29_poster.jpg",
        "correct": "Ucuz Roman (Pulp Fiction)",
        "wrongs": ["Rezervuar Köpekleri", "Sıkı Dostlar", "Dövüş Kulübü"]
    },
    {
        "img": "https://upload.wikimedia.org/wikipedia/en/f/fc/Fight_Club_poster.jpg",
        "correct": "Dövüş Kulübü",
        "wrongs": ["Yedi (Se7en)", "Olağan Şüpheliler", "Zindan Adası"]
    }
]

for s in sorular_data:
    options = s['wrongs'] + [s['correct']]
    random.shuffle(options)
    
    dogru_harf = ""
    if options[0] == s['correct']: dogru_harf = "A"
    elif options[1] == s['correct']: dogru_harf = "B"
    elif options[2] == s['correct']: dogru_harf = "C"
    else: dogru_harf = "D"
    
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, "Bu resim hangi filme aittir?", s['img'], options[0], options[1], options[2], options[3], dogru_harf))

conn.commit()
cur.close()
conn.close()
print("Movies Game Seeded Successfully!")
