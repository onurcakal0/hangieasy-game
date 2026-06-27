import os
import psycopg2
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import json

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

API_KEY = "15d2ea6d0dc1d476efbca3eba2b9bbfb"

movie_queries = {
    "Baba (The Godfather)": "The Godfather",
    "Titanik": "Titanic",
    "Avatar": "Avatar",
    "Kara Şövalye": "The Dark Knight",
    "Forrest Gump": "Forrest Gump",
    "The Matrix": "The Matrix",
    "Başlangıç (Inception)": "Inception",
    "Yüzüklerin Efendisi": "The Return of the King",
    "Yıldızlararası": "Interstellar",
    "Harry Potter": "Harry Potter and the Sorcerer's Stone",
    "Yenilmezler (Avengers)": "The Avengers",
    "Jurassic Park": "Jurassic Park",
    "Yıldız Savaşları (Star Wars)": "Star Wars",
    "Örümcek Adam": "Spider-Man",
    "Joker": "Joker",
    "Aslan Kral": "The Lion King",
    "Gladyatör": "Gladiator",
    "Geleceğe Dönüş": "Back to the Future",
    "Ucuz Roman (Pulp Fiction)": "Pulp Fiction",
    "Dövüş Kulübü": "Fight Club"
}

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Resimdeki Filmi Tahmin Edebilir Misin?' LIMIT 1")
oyun = cur.fetchone()
if oyun:
    for brand, query in movie_queries.items():
        q = urllib.parse.quote(query)
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={q}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)
            data = json.loads(res.read().decode('utf-8'))
            if data['results']:
                # Get the first result's backdrop path
                backdrop = data['results'][0].get('backdrop_path')
                if backdrop:
                    img_url = f"https://image.tmdb.org/t/p/w780{backdrop}"
                    print(f"Found backdrop for {brand}: {img_url}")
                    cur.execute("""
                        UPDATE hangisi_soru 
                        SET resim_url = %s 
                        WHERE oyun_id = %s AND (
                            (secenek_a = %s AND dogru_cevap = 'A') OR
                            (secenek_b = %s AND dogru_cevap = 'B') OR
                            (secenek_c = %s AND dogru_cevap = 'C') OR
                            (secenek_d = %s AND dogru_cevap = 'D')
                        )
                    """, (img_url, oyun[0], brand, brand, brand, brand))
                else:
                    print(f"No backdrop for {brand}")
        except Exception as e:
            print(f"Error {brand}: {e}")

conn.commit()
cur.close()
conn.close()
print("All movie scenes updated with TMDB backdrops!")
