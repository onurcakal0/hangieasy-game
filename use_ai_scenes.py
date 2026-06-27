import os
import psycopg2
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

movie_scenes = {
    "Baba (The Godfather)": "The Godfather 1972 movie scene Vito Corleone in his dark office cinematic realistic",
    "Titanik": "Titanic 1997 movie scene jack and rose standing on the bow of the ship sunset realistic",
    "Avatar": "Avatar 2009 movie scene glowing blue pandora forest at night realistic cinematic",
    "Kara Şövalye": "The Dark Knight 2008 movie scene joker in the interrogation room cinematic",
    "Forrest Gump": "Forrest Gump movie scene man sitting on a park bench with a box of chocolates realistic",
    "The Matrix": "The Matrix 1999 movie scene neo dodging bullets in slow motion green tint cinematic",
    "Başlangıç (Inception)": "Inception 2010 movie scene spinning top on a table dream sequence cinematic",
    "Yüzüklerin Efendisi": "Lord of the rings return of the king huge medieval army charging battle scene cinematic",
    "Yıldızlararası": "Interstellar movie scene astronaut walking on water planet with massive wave cinematic",
    "Harry Potter": "Harry potter sorcerers stone movie scene floating candles in great hall realistic",
    "Yenilmezler (Avengers)": "The Avengers 2012 movie scene superheroes standing in a circle in new york city cinematic",
    "Jurassic Park": "Jurassic Park 1993 movie scene giant t-rex roaring in the rain realistic",
    "Yıldız Savaşları (Star Wars)": "Star Wars Episode IV movie scene binary sunset two suns dessert planet cinematic",
    "Örümcek Adam": "Spider-Man 2002 movie scene upside down kiss in the rain realistic",
    "Joker": "Joker 2019 movie scene man with clown makeup dancing on stairs realistic cinematic",
    "Aslan Kral": "The Lion King 1994 movie scene holding lion cub up on pride rock sunrise realistic",
    "Gladyatör": "Gladiator movie scene roman soldier in the colosseum are you not entertained realistic",
    "Geleceğe Dönüş": "Back to the future movie scene delorean car lightning strikes clock tower realistic",
    "Ucuz Roman (Pulp Fiction)": "Pulp fiction movie scene john travolta and uma thurman dancing twist realistic",
    "Dövüş Kulübü": "Fight club movie scene brad pitt underground boxing ring realistic cinematic"
}

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Resimdeki Filmi Tahmin Edebilir Misin?' LIMIT 1")
oyun = cur.fetchone()
if oyun:
    for brand, prompt in movie_scenes.items():
        query = urllib.parse.quote(prompt)
        # Using a reliable generative endpoint
        img_url = f"https://image.pollinations.ai/prompt/{query}?width=800&height=450&nologo=1"
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
print("Scenes updated with Pollinations AI generated scenes!")
