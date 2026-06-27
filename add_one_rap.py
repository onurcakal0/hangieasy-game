import urllib.request
import urllib.parse
import json
import os
import random
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id FROM oyun WHERE baslik = 'Türkçe Rap: 5 Saniye Challenge' LIMIT 1")
oyun_id = cur.fetchone()[0]

song = {"query": "Khontkar Surtuge Bak", "correct": "Khontkar - Sürtüğe Bak", "wrong": ["Ati242 - Gringo", "Patron - Goal", "Şehinşah - Karma"]}
idx = 10

try:
    url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(song["query"]) + "&entity=song&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    
    if data['resultCount'] > 0:
        preview_url = data['results'][0]['previewUrl']
        temp_file = f"static/audio/rap/temp_{idx}.m4a"
        final_file = f"static/audio/rap/song_{idx}.m4a"
        
        urllib.request.urlretrieve(preview_url, temp_file)
        os.system(f"ffmpeg -y -ss 00:00:10 -i {temp_file} -t 5 -c copy {final_file} 2>/dev/null")
        os.remove(temp_file)
        
        opts = song["wrong"] + [song["correct"]]
        random.shuffle(opts)
        secenekler_str = ",".join(opts)
        
        cur.execute('''
            INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
            VALUES (%s, %s, %s, %s)
        ''', (oyun_id, secenekler_str, song["correct"], f"/{final_file}"))
        
        print(f"Added {song['correct']}")
except Exception as e:
    print(f"Error: {e}")

conn.commit()
cur.close()
conn.close()
