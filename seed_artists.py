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

artists = [
    {
        "name": "Motive",
        "cover": "/static/img/games/motive_cover.png",
        "songs": ["Makmece", "10MG", "Kâr", "Chorus", "Ömrüm", "Romantik", "Nereye", "Trash", "Okyanus", "Yüce Aşk"]
    },
    {
        "name": "Ezhel",
        "cover": "/static/img/games/ezhel_cover.png",
        "songs": ["Geceler", "Felaket", "Şehrimin Tadı", "Alo", "Kazıdık Tırnaklarla", "İmkansızım", "Bul Beni", "Olay", "Allah'ından Bul", "Pavyon"]
    },
    {
        "name": "Ceza",
        "cover": "/static/img/games/ceza_cover.png",
        "songs": ["Suspus", "Holocaust", "Yerli Plaka", "Fark Var", "Panorama Harem", "Neyim Var Ki", "Kim Bilir", "Gelsin Hayat Bildiği Gibi", "Medcezir", "Ben Ağlamazken"]
    },
    {
        "name": "Sagopa Kajmer",
        "cover": "/static/img/games/sagopa_cover.png",
        "songs": ["Bir Pesimistin Gözyaşları", "Baytar", "Galiba", "Ateşten Gömlek", "İstisnalar Kaideyi Bozmaz", "Gölge Haramileri", "Avutsun Bahaneler", "366. Gün", "Sertlik Kanında Var Hayatın", "İki Tanık"]
    },
    {
        "name": "Blok3",
        "cover": "/static/img/games/blok3_cover.png",
        "songs": ["Affetmem", "Vur", "Baybay", "Okyanus", "Ciro", "Patlıyor", "10 Numara", "Yaptırıcaz Tırnaklarını", "Aklına Ben Gelicem", "Güzel ve İddialı"]
    }
]

for a in artists:
    artist_name = a["name"]
    cover_url = a["cover"]
    songs_list = a["songs"]
    
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
    
    for idx, s in enumerate(songs_list):
        query = f"{artist_name} {s}"
        correct_ans = f"{artist_name} - {s}"
        
        # Wrong options: Pick 3 other songs from the same artist
        other_songs = [x for x in songs_list if x != s]
        wrong_ans = [f"{artist_name} - {x}" for x in random.sample(other_songs, 3)]
        
        try:
            url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(query) + "&entity=song&limit=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read().decode('utf-8')
            data = json.loads(res)
            
            if data['resultCount'] > 0:
                preview_url = data['results'][0]['previewUrl']
                # Try to get the actual track name from API if possible to be more accurate
                # correct_ans = f"{artist_name} - {data['results'][0]['trackName']}"
                
                temp_file = f"{dir_path}/temp_{idx}.m4a"
                final_file = f"{dir_path}/song_{idx}.m4a"
                
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
            else:
                print(f"NOT FOUND: {query}")
        except Exception as e:
            print(f"ERROR on {query}: {e}")

conn.commit()
cur.close()
conn.close()
print("All artist games seeded successfully!")
