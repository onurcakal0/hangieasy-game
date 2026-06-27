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

artists_fix = [
    {
        "name": "Motive",
        "songs": ["Inkar", "Karar", "Makina", "Kumbara"]
    },
    {
        "name": "Ezhel",
        "songs": ["Sehrimin Tadi", "Imkansizim", "Lolo"]
    },
    {
        "name": "Blok3",
        "songs": ["Patliyor", "Yaptiricaz Tirnaklarini", "Guzel Ve Iddiali", "Escobar", "Woum Baby", "N'aptin"]
    }
]

for a in artists_fix:
    artist_name = a["name"]
    dir_path = f"static/audio/{artist_name.lower().replace(' ', '_')}"
    os.makedirs(dir_path, exist_ok=True)
    
    cur.execute("SELECT id FROM oyun WHERE baslik = %s LIMIT 1", (f"{artist_name} Ne Kadar Tanıyorsun?",))
    oyun_id = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM soru WHERE oyun_id = %s", (oyun_id,))
    count = cur.fetchone()[0]
    
    for s in a["songs"]:
        if count >= 10: break
        query = f"{artist_name} {s}"
        correct_ans = f"{artist_name} - {s}"
        wrong_ans = [f"{artist_name} - {x}" for x in random.sample(a["songs"], 2)] + [f"{artist_name} - Diğer"]
        
        try:
            url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(query) + "&entity=song&limit=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read().decode('utf-8')
            data = json.loads(res)
            
            if data['resultCount'] > 0:
                preview_url = data['results'][0]['previewUrl']
                
                temp_file = f"{dir_path}/temp_fix_{count}.m4a"
                final_file = f"{dir_path}/song_fix_{count}.m4a"
                
                urllib.request.urlretrieve(preview_url, temp_file)
                os.system(f"ffmpeg -y -ss 00:00:10 -i {temp_file} -t 5 -c copy {final_file} 2>/dev/null")
                os.remove(temp_file)
                
                opts = wrong_ans + [correct_ans]
                random.shuffle(opts)
                secenekler_str = ",".join(opts)
                
                cur.execute('''
                    INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
                    VALUES (%s, %s, %s, %s)
                ''', (oyun_id, secenekler_str, correct_ans, f"/{final_file}"))
                
                print(f"Added {correct_ans}")
                count += 1
            else:
                print(f"NOT FOUND: {query}")
        except Exception as e:
            print(f"ERROR on {query}: {e}")
        time.sleep(2)  # Delay to avoid 429

conn.commit()
cur.close()
conn.close()
print("Fixed missing songs!")
