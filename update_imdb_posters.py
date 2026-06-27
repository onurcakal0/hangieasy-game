import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

posters = {
    "Esaretin Bedeli (1994)": "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
    "Baba (1972)": "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
    "Kara Şövalye (2008)": "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
    "Baba 2 (1974)": "https://upload.wikimedia.org/wikipedia/en/0/03/Godfather_part_ii.jpg",
    "12 Öfkeli Adam (1957)": "https://upload.wikimedia.org/wikipedia/en/9/91/12_angry_men.jpg",
    "Schindler'in Listesi (1993)": "https://upload.wikimedia.org/wikipedia/en/3/38/Schindler%27s_List_movie.jpg",
    "Yüzüklerin Efendisi: Kralın Dönüşü": "https://upload.wikimedia.org/wikipedia/en/b/be/The_Lord_of_the_Rings_-_The_Return_of_the_King_%282003%29.jpg",
    "Ucuz Roman (1994)": "https://upload.wikimedia.org/wikipedia/en/3/3b/Pulp_Fiction_%281994%29_poster.jpg",
    "Yüzüklerin Efendisi: Yüzük Kardeşliği": "https://upload.wikimedia.org/wikipedia/en/8/8a/The_Lord_of_the_Rings_The_Fellowship_of_the_Ring_%282001%29.jpg",
    "İyi, Kötü ve Çirkin (1966)": "https://upload.wikimedia.org/wikipedia/en/4/45/Good_the_bad_and_the_ugly_poster.jpg",
    "Forrest Gump (1994)": "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
    "Dövüş Kulübü (1999)": "https://upload.wikimedia.org/wikipedia/en/f/fc/Fight_Club_poster.jpg",
    "Yüzüklerin Efendisi: İki Kule": "https://upload.wikimedia.org/wikipedia/en/d/d0/Lord_of_the_Rings_-_The_Two_Towers_%282002%29.jpg",
    "Başlangıç (Inception)": "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
    "Yıldız Savaşları: İmparator": "https://upload.wikimedia.org/wikipedia/en/3/3f/The_Empire_Strikes_Back_%281980_movie_poster%29.jpg",
    "The Matrix (1999)": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
    "Sıkı Dostlar (Goodfellas)": "https://upload.wikimedia.org/wikipedia/en/7/7b/Goodfellas.jpg",
    "Guguk Kuşu (1975)": "https://upload.wikimedia.org/wikipedia/en/2/26/One_Flew_Over_the_Cuckoo%27s_Nest_poster.jpg",
    "Yedi (Se7en)": "https://upload.wikimedia.org/wikipedia/en/6/68/Seven_%28movie%29_poster.jpg",
    "Şahane Hayat (1946)": "https://upload.wikimedia.org/wikipedia/en/9/9f/It%27s_a_Wonderful_Life_%281946_poster%29.jpeg"
}

cur.execute("SELECT id FROM oyun WHERE baslik='IMDb Top 20: En İyi Film Hangisi?' ORDER BY id DESC LIMIT 1")
oyun_id = cur.fetchone()[0]

cur.execute("SELECT id, secenekler FROM soru WHERE oyun_id=%s ORDER BY id", (oyun_id,))
sorular = cur.fetchall()

# Delete and reinsert to fix the comma issue properly
cur.execute("DELETE FROM soru WHERE oyun_id=%s", (oyun_id,))

matchups = [
    ("Esaretin Bedeli (1994)", "Baba (1972)"),
    ("Kara Şövalye (2008)", "Baba 2 (1974)"),
    ("12 Öfkeli Adam (1957)", "Schindler'in Listesi (1993)"),
    ("Yüzüklerin Efendisi: Kralın Dönüşü", "Ucuz Roman (1994)"),
    ("Yüzüklerin Efendisi: Yüzük Kardeşliği", "İyi, Kötü ve Çirkin (1966)"),
    ("Forrest Gump (1994)", "Dövüş Kulübü (1999)"),
    ("Yüzüklerin Efendisi: İki Kule", "Başlangıç (Inception)"),
    ("Yıldız Savaşları: İmparator", "The Matrix (1999)"),
    ("Sıkı Dostlar (Goodfellas)", "Guguk Kuşu (1975)"),
    ("Yedi (Se7en)", "Şahane Hayat (1946)")
]

for m in matchups:
    f1 = m[0]
    f2 = m[1]
    secenekler = f"{f1}|{f2}" # Using | instead of , since Good, Bad and Ugly has a comma!
    
    cur.execute(
        "INSERT INTO soru (oyun_id, resim_url, resim_url_2, secenekler) VALUES (%s, %s, %s, %s)",
        (oyun_id, posters[f1], posters[f2], secenekler)
    )

conn.commit()
cur.close()
conn.close()
print("Posters updated successfully!")
