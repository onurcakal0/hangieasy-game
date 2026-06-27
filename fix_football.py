import urllib.request
import json
import urllib.parse
import time

teams = [
    {"name": "Aston Villa", "idx": 0},
    {"name": "Newcastle United", "idx": 1},
    {"name": "Bayer Leverkusen", "idx": 2},
    {"name": "Napoli", "idx": 3},
    {"name": "Real Sociedad", "idx": 4},
    {"name": "Marseille", "idx": 5},
    {"name": "West Ham", "idx": 6},
    {"name": "Athletic Bilbao", "idx": 7},
    {"name": "Eintracht Frankfurt", "idx": 8},
    {"name": "Lazio", "idx": 9},
    {"name": "Crystal Palace", "idx": 10},
    {"name": "Brentford", "idx": 11},
    {"name": "Celta Vigo", "idx": 12},
    {"name": "Osasuna", "idx": 13},
    {"name": "Union Berlin", "idx": 14},
    {"name": "SC Freiburg", "idx": 15},
    {"name": "Atalanta", "idx": 16},
    {"name": "Fiorentina", "idx": 17},
    {"name": "Torino", "idx": 18},
    {"name": "Lens", "idx": 19}, # Changed from RC Lens for better search
    {"name": "Nice", "idx": 20}, # Changed from OGC Nice
    {"name": "Fulham", "idx": 21},
    {"name": "VfL Bochum", "idx": 22},
    {"name": "Empoli", "idx": 23},
    {"name": "Mallorca", "idx": 24}
]

failed = [2, 3, 8, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

# Find game ID dynamically
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik LIKE '%5 Büyük Lig Logo%' LIMIT 1")
row = cur.fetchone()
if row:
    oyun_id = row[0]
else:
    print("Oyun bulunamadı")
    exit()

for idx in failed:
    team_name = next(t['name'] for t in teams if t['idx'] == idx)
    search_url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={urllib.parse.quote(team_name)}"
    print(f"Fetching {team_name}...")
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        
        if data.get('teams'):
            img_url = data['teams'][0]['strBadge']
            filepath = f"static/img/football_logos/logo_{oyun_id}_{idx}.jpg"
            
            # Download
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img) as img_response, open(filepath, 'wb') as out_file:
                out_file.write(img_response.read())
            
            print(f"Successfully fixed {team_name}")
            
            # Update DB to point to the local file (if it was pointing to dummyimage)
            local_url = f"/{filepath}"
            # We need to find the specific question. We can match by dogru_cevap being in the options.
            # But wait, the question text has the team_name in one of the options.
            # Let's just update all questions for this game_id where secenek_a = team_name or secenek_b = team_name etc.
            cur.execute(f'''
                UPDATE hangisi_soru SET resim_url = %s 
                WHERE oyun_id = %s AND (secenek_a = %s OR secenek_b = %s OR secenek_c = %s OR secenek_d = %s)
            ''', (local_url, oyun_id, team_name, team_name, team_name, team_name))
        else:
            print(f"Could not find badge for {team_name} via sportsdb")
    except Exception as e:
        print(f"Error for {team_name}: {e}")

conn.commit()
cur.close()
conn.close()
print("All missing images fetched!")
