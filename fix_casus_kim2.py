import psycopg2
import os
import time
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

os.makedirs("static/img/game_chars", exist_ok=True)

cur.execute("SELECT id FROM oyun WHERE baslik = 'Casus Kim: Oyun Karakterleri' LIMIT 1")
row = cur.fetchone()
if not row:
    print("Oyun bulunamadı")
    exit()

oyun_id = row[0]
cur.execute("DELETE FROM soru WHERE oyun_id = %s", (oyun_id,))

def d(name):
    return f"https://api.dicebear.com/9.x/adventurer/png?seed={urllib.parse.quote(name)}&backgroundColor=151520"

questions = [
    {
        "names": ["Michael", "Trevor", "Franklin", "Arthur Morgan"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/Michael_De_Santa.png/220px-Michael_De_Santa.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/7/75/Trevor_Philips.png/220px-Trevor_Philips.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Franklin_Clinton.png/220px-Franklin_Clinton.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Arthur_Morgan.png/220px-Arthur_Morgan.png"
        ],
        "spy": "Arthur Morgan"
    },
    {
        "names": ["Geralt", "Ciri", "Yennefer", "Kratos"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/8/88/Geralt_of_Rivia.png/220px-Geralt_of_Rivia.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/Ciri_The_Witcher_3.png/220px-Ciri_The_Witcher_3.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/9/90/Yennefer_of_Vengerberg.png/220px-Yennefer_of_Vengerberg.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/a/a5/Kratos_PS4.jpg/220px-Kratos_PS4.jpg"
        ],
        "spy": "Kratos"
    },
    {
        "names": ["Mario", "Luigi", "Bowser", "Sonic"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/MarioPortrait.png/220px-MarioPortrait.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/7/73/Luigi_MACW.png/220px-Luigi_MACW.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/Bowser_-_Super_Mario_Bros_Wonder.png/220px-Bowser_-_Super_Mario_Bros_Wonder.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/2/28/Sonic_the_Hedgehog.png/220px-Sonic_the_Hedgehog.png"
        ],
        "spy": "Sonic"
    },
    {
        "names": ["Scorpion", "Sub-Zero", "Raiden", "Ryu"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Scorpion_MK11.png/220px-Scorpion_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/38/Sub-Zero_MK11.png/220px-Sub-Zero_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/Raiden_MK11.png/220px-Raiden_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Ryu_SF6.png/220px-Ryu_SF6.png"
        ],
        "spy": "Ryu"
    },
    {
        "names": ["Joel", "Ellie", "Clicker", "Nathan Drake"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/2/24/Joel_TLOU.jpg/220px-Joel_TLOU.jpg",
            "https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/Ellie_The_Last_of_Us_Part_II.png/220px-Ellie_The_Last_of_Us_Part_II.png",
            d("Clicker"),
            "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Nathan_Drake_U4.png/220px-Nathan_Drake_U4.png"
        ],
        "spy": "Nathan Drake"
    },
    {
        "names": ["Leon Kennedy", "Claire Redfield", "Chris Redfield", "Pyramid Head"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/Leon_S._Kennedy.png/220px-Leon_S._Kennedy.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/Claire_Redfield_RE2_Remake.png/220px-Claire_Redfield_RE2_Remake.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/9/90/Chris_Redfield_RE_Village.png/220px-Chris_Redfield_RE_Village.png",
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/36/Pyramid_Head.png/220px-Pyramid_Head.png"
        ],
        "spy": "Pyramid Head"
    },
    {
        "names": ["Jett", "Phoenix", "Sage", "Yasuo"],
        "urls": [
            d("Jett"), d("Phoenix"), d("Sage"),
            "https://upload.wikimedia.org/wikipedia/en/thumb/1/1a/Yasuo_LoL_splash.jpg/220px-Yasuo_LoL_splash.jpg"
        ],
        "spy": "Yasuo"
    },
    {
        "names": ["Steve", "Alex", "Enderman", "Roblox Noob"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/34/Steve_%28Minecraft%29.png/220px-Steve_%28Minecraft%29.png",
            d("Alex"), d("Enderman"), d("Roblox Noob")
        ],
        "spy": "Roblox Noob"
    },
    {
        "names": ["Jinx", "Vi", "Caitlyn", "Pudge"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/9/96/Jinx_from_League_of_Legends.jpg/220px-Jinx_from_League_of_Legends.jpg",
            d("Vi"), d("Caitlyn"), d("Pudge")
        ],
        "spy": "Pudge"
    },
    {
        "names": ["Lara Croft", "Jonah", "Roth", "Aloy"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Lara_Croft_Shadow_of_the_Tomb_Raider.png/220px-Lara_Croft_Shadow_of_the_Tomb_Raider.png",
            d("Jonah"), d("Roth"), 
            "https://upload.wikimedia.org/wikipedia/en/thumb/9/94/Aloy_Horizon_Forbidden_West.png/220px-Aloy_Horizon_Forbidden_West.png"
        ],
        "spy": "Aloy"
    }
]

import random

for q_idx, q in enumerate(questions):
    names = q['names']
    urls = q['urls']
    spy = q['spy']
    
    local_urls = []
    for i, url in enumerate(urls):
        safe_name = names[i].replace(" ", "_").replace(".", "").lower()
        filepath = f"static/img/game_chars/{safe_name}.png"
        
        # Download if it's a wikipedia image
        if "wikimedia.org" in url:
            if not os.path.exists(filepath):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                    with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                        out_file.write(response.read())
                    time.sleep(1) # Delay to prevent 429
                    print(f"Downloaded {names[i]}")
                except Exception as e:
                    print(f"Failed to download {names[i]} from {url}: {e}")
                    filepath = d(names[i]) # fallback
                    
            if filepath.startswith("http"):
                local_urls.append(filepath)
            else:
                local_urls.append(f"/{filepath}")
        else:
            local_urls.append(url) # keep dicebear
            
    # Bundle names and local_urls
    bundled = list(zip(names, local_urls))
    random.shuffle(bundled)
    
    shuffled_names = [b[0] for b in bundled]
    shuffled_urls = [b[1] for b in bundled]
    
    secenekler_str = ",".join(shuffled_names)
    resim_str = ",".join(shuffled_urls)
    
    cur.execute('''
        INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
        VALUES (%s, %s, %s, %s)
    ''', (oyun_id, secenekler_str, spy, resim_str))

conn.commit()
cur.close()
conn.close()
print("Casus Kim: Oyun Karakterleri 100% FIXED successfully!")
