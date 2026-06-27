import os
import time
import psycopg2
import urllib.request
import re
from dotenv import load_dotenv
import random

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Create static directory if not exists
os.makedirs("static/img/football_logos", exist_ok=True)

teams = [
    {"name": "Aston Villa", "wiki": "Aston_Villa_F.C.", "wrongs": ["West Ham United", "Everton", "Burnley"]},
    {"name": "Newcastle United", "wiki": "Newcastle_United_F.C.", "wrongs": ["Juventus", "Notts County", "Udinese"]},
    {"name": "Bayer Leverkusen", "wiki": "Bayer_04_Leverkusen", "wrongs": ["RB Leipzig", "VfL Wolfsburg", "Borussia Mönchengladbach"]},
    {"name": "Napoli", "wiki": "SSC_Napoli", "wrongs": ["Lazio", "Sampdoria", "Empoli"]},
    {"name": "Real Sociedad", "wiki": "Real_Sociedad", "wrongs": ["Deportivo Alavés", "Celta Vigo", "Rayo Vallecano"]},
    {"name": "Marseille", "wiki": "Olympique_de_Marseille", "wrongs": ["Monaco", "Lyon", "Bordeaux"]},
    {"name": "West Ham", "wiki": "West_Ham_United_F.C.", "wrongs": ["Aston Villa", "Crystal Palace", "Burnley"]},
    {"name": "Athletic Bilbao", "wiki": "Athletic_Bilbao", "wrongs": ["Real Sociedad", "Osasuna", "Sporting Gijón"]},
    {"name": "Eintracht Frankfurt", "wiki": "Eintracht_Frankfurt", "wrongs": ["Stuttgart", "Werder Bremen", "FC Köln"]},
    {"name": "Lazio", "wiki": "SS_Lazio", "wrongs": ["Napoli", "Atalanta", "Torino"]},
    {"name": "Crystal Palace", "wiki": "Crystal_Palace_F.C.", "wrongs": ["Aston Villa", "West Ham United", "Brentford"]},
    {"name": "Brentford", "wiki": "Brentford_F.C.", "wrongs": ["Fulham", "Sheffield United", "Bournemouth"]},
    {"name": "Celta Vigo", "wiki": "RC_Celta_de_Vigo", "wrongs": ["Deportivo La Coruña", "Real Sociedad", "Mallorca"]},
    {"name": "Osasuna", "wiki": "CA_Osasuna", "wrongs": ["Athletic Bilbao", "Zaragoza", "Almería"]},
    {"name": "Union Berlin", "wiki": "1._FC_Union_Berlin", "wrongs": ["Hertha Berlin", "Bochum", "Mainz 05"]},
    {"name": "SC Freiburg", "wiki": "SC_Freiburg", "wrongs": ["Stuttgart", "Augsburg", "Heidenheim"]},
    {"name": "Atalanta", "wiki": "Atalanta_BC", "wrongs": ["Sassuolo", "Udinese", "Hellas Verona"]},
    {"name": "Fiorentina", "wiki": "ACF_Fiorentina", "wrongs": ["Bologna", "Parma", "Palermo"]},
    {"name": "Torino", "wiki": "Torino_F.C.", "wrongs": ["Bologna", "Lazio", "Genoa"]},
    {"name": "RC Lens", "wiki": "RC_Lens", "wrongs": ["Rennes", "Nantes", "Metz"]},
    {"name": "OGC Nice", "wiki": "OGC_Nice", "wrongs": ["Monaco", "Montpellier", "Lille"]},
    {"name": "Fulham", "wiki": "Fulham_F.C.", "wrongs": ["Brentford", "Nottingham Forest", "Luton Town"]},
    {"name": "VfL Bochum", "wiki": "VfL_Bochum", "wrongs": ["Schalke 04", "Arminia Bielefeld", "Darmstadt"]},
    {"name": "Empoli", "wiki": "Empoli_F.C.", "wrongs": ["Spezia", "Frosinone", "Salernitana"]},
    {"name": "RCD Mallorca", "wiki": "RCD_Mallorca", "wrongs": ["Cadiz", "Las Palmas", "Getafe"]}
]

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "5 Büyük Lig Logo Tahmin", 
    "Avrupa'nın en büyük 5 liginden 25 dişli takım! Futbol bilgin ne kadar sağlam? Orta ve zor seviye logolar seni bekliyor.",
    "https://images.unsplash.com/photo-1518605368461-1e1e11415121?auto=format&fit=crop&q=80&w=800", # Generic football stadium
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

print("Downloading football logos sequentially to avoid rate limits...")
for idx, c in enumerate(teams):
    team_name = c['name']
    wiki_url = f"https://en.wikipedia.org/wiki/{c['wiki']}"
    filename = f"logo_{oyun_id}_{idx}.jpg"
    filepath = f"static/img/football_logos/{filename}"
    
    local_url = "https://dummyimage.com/600x400/151520/ffffff&text=" + urllib.parse.quote(team_name)
    try:
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'HangiEasyBot/1.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'meta property="og:image" content="(.*?)"', html)
        if match:
            img_url = match.group(1)
            # Download image
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'HangiEasyBot/1.0'})
            with urllib.request.urlopen(req_img) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            local_url = f"/{filepath}"
            print(f"Downloaded: {team_name}")
        else:
            print(f"No og:image for {team_name}")
    except Exception as e:
        print(f"Error {team_name}: {e}")

    time.sleep(1) # Prevent 429
    
    # Insert question
    options = c['wrongs'] + [team_name]
    random.shuffle(options)
    
    dogru_harf = "A" if options[0] == team_name else "B" if options[1] == team_name else "C" if options[2] == team_name else "D"
    
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, "Bu logo hangi futbol takımına aittir?", local_url, options[0], options[1], options[2], options[3], dogru_harf))

conn.commit()
cur.close()
conn.close()
print("Football Logos test seeded successfully with locally hosted images!")
