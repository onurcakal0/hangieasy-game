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
        "valid_artists": ["UZI"],
        "cover": "/static/img/games/uzi_cover.png"
    },
    {
        "name": "Ati242",
        "search_term": "Ati242",
        "valid_artists": ["Ati242", "Ati242 & BLOK3"],
        "cover": "/static/img/games/ati242_cover.png"
    },
    {
        "name": "Lvbel C5",
        "search_term": "Lvbel C5",
        "valid_artists": ["Lvbel C5", "Lvbel C5 & AKDO", "AKDO & Lvbel C5"],
        "cover": "/static/img/games/lvbelc5_cover.png"
    }
]

for a in artists:
    artist_name = a["name"]
    cover_url = a["cover"]
    valid_artists = a["valid_artists"]
    
    dir_path = f"static/audio/{artist_name.lower().replace(' ', '_')}"
    os.makedirs(dir_path, exist_ok=True)
    
    cur.execute('''
        INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    ''', (
        f"{artist_name} Ne Kadar Tanıyorsun?", 
        f"Sadece 5 saniye dinleyerek {artist_name} şarkılarını bulabilir misin? Gerçek bir dinleyiciysen kanıtla!",
        cover_url,
        "Müzik",
        "sesli_quiz",
        0
    ))
    oyun_id = cur.fetchone()[0]
    
    # Fetch songs dynamically from iTunes
    url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(a["search_term"]) + "&entity=song&limit=40"
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
        
        temp_file = f"{dir_path}/temp_{idx}.m4a"
        final_file = f"{dir_path}/song_{idx}.m4a"
        
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
print("All 3 new artist games seeded successfully!")
