import urllib.request
import urllib.parse
import json
import os
import random
import time
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

artists = [
    {
        "name": "UZI",
        "search_term": "UZI",
        "valid_artists": ["UZI", "GNG & UZI", "UZI & Motive", "UZI & Aksan", "UZI & Mavi", "Tuhan & UZI"]
    },
    {
        "name": "Ezhel",
        "search_term": "Ezhel",
        "valid_artists": ["Ezhel", "Murda & Ezhel", "Artz, Bugy & Ezhel", "Ezhel & JUGGLERZ"]
    }
]

for a in artists:
    artist_name = a["name"]
    valid_artists = a["valid_artists"]
    
    cur.execute("SELECT id FROM oyun WHERE baslik = %s LIMIT 1", (f"{artist_name} Ne Kadar Tanıyorsun?",))
    res = cur.fetchone()
    if not res:
        print(f"Game not found for {artist_name}")
        continue
    oyun_id = res[0]
    
    cur.execute("DELETE FROM soru WHERE oyun_id = %s", (oyun_id,))
    
    dir_path = f"static/audio/{artist_name.lower().replace(' ', '_')}"
    os.makedirs(dir_path, exist_ok=True)
    
    url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(a["search_term"]) + "&entity=song&country=tr&limit=50"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    
    songs = []
    seen = set()
    for track in data.get('results', []):
        if track.get('artistName') in valid_artists and track.get('trackName') not in seen:
            songs.append(track)
            seen.add(track.get('trackName'))
        if len(songs) >= 10:
            break
            
    all_track_names = [s['trackName'] for s in songs]
    
    for idx, s in enumerate(songs):
        track_name = s['trackName']
        preview_url = s['previewUrl']
        
        correct_ans = f"{artist_name} - {track_name}"
        other_songs = [x for x in all_track_names if x != track_name]
        wrong_ans = [f"{artist_name} - {x}" for x in random.sample(other_songs, min(3, len(other_songs)))]
        while len(wrong_ans) < 3:
            wrong_ans.append(f"{artist_name} - Diğer Şarkı")
        
        temp_file = f"{dir_path}/temp_real_{idx}.m4a"
        final_file = f"{dir_path}/song_real_{idx}.m4a"
        
        try:
            urllib.request.urlretrieve(preview_url, temp_file)
            os.system(f'ffmpeg -y -ss 00:00:10 -i "{temp_file}" -t 5 -c copy "{final_file}" 2>/dev/null')
            os.remove(temp_file)
            
            opts = wrong_ans + [correct_ans]
            random.shuffle(opts)
            secenekler_str = ",".join(opts)
            
            cur.execute('''
                INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
                VALUES (%s, %s, %s, %s)
            ''', (oyun_id, secenekler_str, correct_ans, f"/{final_file}"))
            
            print(f"Added {correct_ans}")
        except Exception as e:
            print(f"ERROR downloading/processing {track_name}: {e}")
        
        time.sleep(1)

conn.commit()
cur.close()
conn.close()
print("UZI and Ezhel completely fixed!")
