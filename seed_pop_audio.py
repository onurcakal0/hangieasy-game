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

os.makedirs("static/audio/pop", exist_ok=True)

# Create game
cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "Türkçe Pop: 5 Saniye Challenge", 
    "Sadece 5 saniye dinleyerek en popüler Türkçe Pop şarkılarını bulabilir misin? Telifsiz ve eğlenceli!",
    "/static/img/games/pop_cover.jpg",
    "Müzik",
    "sesli_quiz",
    0
))
oyun_id = cur.fetchone()[0]

songs = [
    {"query": "Tarkan Simarik", "correct": "Tarkan - Şımarık", "wrong": ["Kenan Doğulu - Çakkıdı", "Mustafa Sandal - İsyankar", "Murat Boz - Janti"]},
    {"query": "Sezen Aksu Sinanay", "correct": "Sezen Aksu - Şinanay", "wrong": ["Nilüfer - Kavak Yelleri", "Sertab Erener - Rengarenk", "Zerrin Özer - Kıyamam"]},
    {"query": "Mustafa Sandal Isyankar", "correct": "Mustafa Sandal - İsyankar", "wrong": ["Tarkan - Dudu", "Burak Kut - Benimle Oynama", "Kenan Doğulu - Yaparım Bilirsin"]},
    {"query": "Sertab Erener Rengarenk", "correct": "Sertab Erener - Rengarenk", "wrong": ["Hande Yener - Bodrum", "Gülşen - Bangır Bangır", "Demet Akalın - Afedersin"]},
    {"query": "Edis Martilar", "correct": "Edis - Martılar", "wrong": ["Oğuzhan Koç - Bulutlara Esir Olduk", "Murat Dalkılıç - Derine", "Berkay - İnanırım"]},
    {"query": "Gulsen Bangir Bangir", "correct": "Gülşen - Bangır Bangır", "wrong": ["Hadise - Düm Tek Tek", "Hande Yener - Romeo", "Simge - Miş Miş"]},
    {"query": "Yalin Zalim", "correct": "Yalın - Zalim", "wrong": ["Gökhan Özen - Aramazsan Arama", "Keremcem - Nerelere Gideyim", "Murat Boz - Özledim"]},
    {"query": "Hande Yener Bodrum", "correct": "Hande Yener - Bodrum", "wrong": ["Demet Akalın - Türkan", "Gülşen - Yurtta Aşk Cihanda Aşk", "Hadise - Şampiyon"]},
    {"query": "Kenan Dogulu Cakkidi", "correct": "Kenan Doğulu - Çakkıdı", "wrong": ["Tarkan - Kuzu Kuzu", "Murat Boz - Uçurum", "Edis - Çok Çok"]},
    {"query": "Hadise Dum Tek Tek", "correct": "Hadise - Düm Tek Tek", "wrong": ["Sertab Erener - Everyway That I Can", "Gülşen - Dan Dan", "Simge - Öpücem"]}
]

for idx, song in enumerate(songs):
    try:
        url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(song["query"]) + "&entity=song&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        
        if data['resultCount'] > 0:
            preview_url = data['results'][0]['previewUrl']
            temp_file = f"static/audio/pop/temp_{idx}.m4a"
            final_file = f"static/audio/pop/song_{idx}.m4a"
            
            # Download full 30s preview
            urllib.request.urlretrieve(preview_url, temp_file)
            
            # Crop to exactly 5 seconds
            os.system(f"ffmpeg -y -ss 00:00:10 -i {temp_file} -t 5 -c copy {final_file} 2>/dev/null")
            os.remove(temp_file)
            
            # Shuffle options
            opts = song["wrong"] + [song["correct"]]
            random.shuffle(opts)
            secenekler_str = ",".join(opts)
            
            cur.execute('''
                INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
                VALUES (%s, %s, %s, %s)
            ''', (oyun_id, secenekler_str, song["correct"], f"/{final_file}"))
            
            print(f"Added {song['correct']}")
        else:
            print(f"Could not find iTunes preview for {song['query']}")
    except Exception as e:
        print(f"Error on {song['query']}: {e}")

conn.commit()
cur.close()
conn.close()
print("Sesli Quiz: Türkçe Pop seeded successfully!")
