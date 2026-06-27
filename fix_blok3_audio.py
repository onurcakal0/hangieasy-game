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

cur.execute("SELECT id FROM oyun WHERE baslik = 'Blok3 Ne Kadar Tanıyorsun?'")
oyun_id = cur.fetchone()[0]

# Delete old questions
cur.execute("DELETE FROM soru WHERE oyun_id = %s", (oyun_id,))

blok3_songs = [
    "Çok Güzel Gülüyorsun",
    "Kırgınım",
    "KUSURA BAKMA",
    "Kayıp Kalp",
    "napıyosun mesela ?",
    "Sebebi Yar",
    "git",
    "Son Bi Dans",
    "Affetmem",
    "Vur"
]

dir_path = "static/audio/blok3"
os.makedirs(dir_path, exist_ok=True)

for count, s in enumerate(blok3_songs):
    query = f"Blok3 {s}"
    correct_ans = f"Blok3 - {s}"
    wrong_ans = [f"Blok3 - {x}" for x in random.sample([x for x in blok3_songs if x != s], 3)]
    
    try:
        url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(query) + "&entity=song&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        
        if data['resultCount'] > 0:
            preview_url = data['results'][0]['previewUrl']
            # Get actual track name to be safe
            actual_track = data['results'][0]['trackName']
            if actual_track.lower() != s.lower():
                correct_ans = f"Blok3 - {actual_track}"
            
            temp_file = f"{dir_path}/temp_real_{count}.m4a"
            final_file = f"{dir_path}/song_real_{count}.m4a"
            
            urllib.request.urlretrieve(preview_url, temp_file)
            os.system(f"ffmpeg -y -ss 00:00:10 -i {temp_file} -t 5 -c copy {final_file} 2>/dev/null")
            os.remove(temp_file)
            
            opts = wrong_ans[:3] + [correct_ans]
            random.shuffle(opts)
            secenekler_str = ",".join(opts)
            
            cur.execute('''
                INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
                VALUES (%s, %s, %s, %s)
            ''', (oyun_id, secenekler_str, correct_ans, f"/{final_file}"))
            
            print(f"Added {correct_ans}")
        else:
            print(f"NOT FOUND: {query}")
    except Exception as e:
        print(f"ERROR on {query}: {e}")
    time.sleep(1.5)

conn.commit()
cur.close()
conn.close()
print("Blok3 completely fixed!")
