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

os.makedirs("static/audio/rap", exist_ok=True)

# Create game
cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "Türkçe Rap: 5 Saniye Challenge", 
    "Sadece 5 saniye dinleyerek bu efsanevi Türkçe Rap parçalarını bulabilir misin? Telifsiz ve kıyasıya rekabet!",
    "https://images.unsplash.com/photo-1516280440502-86107328d000?auto=format&fit=crop&q=80&w=800",
    "Müzik",
    "sesli_quiz",
    0
))
oyun_id = cur.fetchone()[0]

songs = [
    {"query": "Ceza Holocaust", "correct": "Ceza - Holocaust", "wrong": ["Sagopa Kajmer - Neyim Var Ki", "Ezhel - Geceler", "Norm Ender - Mekanın Sahibi"]},
    {"query": "Sagopa Kajmer Bir Pesimistin Gözyaslari", "correct": "Sagopa Kajmer - Bir Pesimistin Gözyaşları", "wrong": ["Ceza - Suspus", "Gazapizm - Heyecanı Yok", "Fuat - Okyanuslar"]},
    {"query": "Norm Ender Mekanin Sahibi", "correct": "Norm Ender - Mekanın Sahibi", "wrong": ["Ben Fero - Demet Akalın", "Killa Hakan - Fight Kulüp", "Ezhel - Felaket"]},
    {"query": "Ezhel Geceler", "correct": "Ezhel - Geceler", "wrong": ["Murda - AYA", "UZI - Krvn", "Cakal - İmdat"]},
    {"query": "Ben Fero Demet Akalin", "correct": "Ben Fero - Demet Akalın", "wrong": ["Ezhel - Şehrimin Tadı", "Khontkar - Sürtüğe Bak", "Patron - Goal"]},
    {"query": "UZI Krvn", "correct": "UZI - Krvn", "wrong": ["Cakal - Mahvettim", "Batuflex - Dalgıç", "Reckol - İstediğim Olacak"]},
    {"query": "Murda Ezhel AYA", "correct": "Murda & Ezhel - AYA", "wrong": ["MERO - Olabilir", "Sefo - Bilmem Mi", "Reynmen - Derdim Olsun"]},
    {"query": "Patron Goal", "correct": "Patron - Goal", "wrong": ["Ati242 - Gringo", "Şehinşah - Karma", "Diyar Pala - Pompalamasyon"]},
    {"query": "Gazapizm Heyecani Yok", "correct": "Gazapizm - Heyecanı Yok", "wrong": ["Eypio - Günah Benim", "Sansar Salvo - Bombalar Hedef Bulur", "Ceza - Yerli Plaka"]},
    {"query": "Killa Hakan Fight Kulup", "correct": "Killa Hakan - Fight Kulüp", "wrong": ["Ceza - Fark Var", "Massaka - Katliam", "Diablo63 - Baba Yorgun"]}
]

for idx, song in enumerate(songs):
    try:
        url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(song["query"]) + "&entity=song&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        
        if data['resultCount'] > 0:
            preview_url = data['results'][0]['previewUrl']
            temp_file = f"static/audio/rap/temp_{idx}.m4a"
            final_file = f"static/audio/rap/song_{idx}.m4a"
            
            # Download full 30s preview
            urllib.request.urlretrieve(preview_url, temp_file)
            
            # Crop to exactly 5 seconds (from second 10 to second 15 to get the beat usually)
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
print("Sesli Quiz: Türkçe Rap seeded successfully!")
