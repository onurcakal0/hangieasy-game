import os
import psycopg2
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

movie_queries = {
    "Baba (The Godfather)": "The Godfather 1972 famous scene high quality",
    "Titanik": "Titanic 1997 movie jack and rose bow scene high quality",
    "Avatar": "Avatar 2009 movie pandora scene",
    "Kara Şövalye": "The Dark Knight 2008 joker interrogation scene",
    "Forrest Gump": "Forrest Gump bench scene high quality",
    "The Matrix": "The Matrix neo dodging bullets scene",
    "Başlangıç (Inception)": "Inception 2010 hallway fight scene",
    "Yüzüklerin Efendisi": "Lord of the rings return of the king charge scene",
    "Yıldızlararası": "Interstellar gargantua black hole scene",
    "Harry Potter": "Harry potter sorcerers stone floating candles scene",
    "Yenilmezler (Avengers)": "The Avengers 2012 circle camera spin scene",
    "Jurassic Park": "Jurassic Park 1993 t-rex roar scene",
    "Yıldız Savaşları (Star Wars)": "Star Wars Episode IV binary sunset scene",
    "Örümcek Adam": "Spider-Man 2002 upside down kiss scene",
    "Joker": "Joker 2019 stairs dance scene",
    "Aslan Kral": "The Lion King 1994 pride rock scene",
    "Gladyatör": "Gladiator are you not entertained scene",
    "Geleceğe Dönüş": "Back to the future clock tower lightning scene",
    "Ucuz Roman (Pulp Fiction)": "Pulp fiction dance scene",
    "Dövüş Kulübü": "Fight club rules scene brad pitt"
}

ddgs = DDGS()

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Resimdeki Filmi Tahmin Edebilir Misin?' LIMIT 1")
oyun = cur.fetchone()
if oyun:
    for brand, query in movie_queries.items():
        results = ddgs.images(query, max_results=1)
        if results:
            img_url = results[0]['image']
            print(f"Updating {brand} -> {img_url}")
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

conn.commit()
cur.close()
conn.close()
print("Scenes updated successfully!")
