import psycopg2
import os
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

os.makedirs("static/img/game_chars", exist_ok=True)

# Find the game
cur.execute("SELECT id FROM oyun WHERE baslik = 'Casus Kim: Oyun Karakterleri' LIMIT 1")
row = cur.fetchone()
if not row:
    print("Oyun bulunamadı")
    exit()

oyun_id = row[0]

# We will drop all questions for this game and re-insert them cleanly
cur.execute("DELETE FROM soru WHERE oyun_id = %s", (oyun_id,))

def d(name):
    return f"https://dummyimage.com/600x600/151520/ffffff&text={urllib.parse.quote(name)}"

questions = [
    {
        "names": ["Michael", "Trevor", "Franklin", "Arthur Morgan"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/e/e4/Michael_De_Santa.png",
            "https://upload.wikimedia.org/wikipedia/en/7/75/Trevor_Philips.png",
            "https://upload.wikimedia.org/wikipedia/en/3/3b/Franklin_Clinton.png",
            "https://upload.wikimedia.org/wikipedia/en/3/3b/Arthur_Morgan.png"
        ],
        "spy": "Arthur Morgan"
    },
    {
        "names": ["Geralt", "Ciri", "Yennefer", "Kratos"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/8/88/Geralt_of_Rivia.png",
            "https://upload.wikimedia.org/wikipedia/en/4/45/Ciri_The_Witcher_3.png",
            "https://upload.wikimedia.org/wikipedia/en/9/90/Yennefer_of_Vengerberg.png",
            "https://upload.wikimedia.org/wikipedia/en/a/a5/Kratos_PS4.jpg"
        ],
        "spy": "Kratos"
    },
    {
        "names": ["Mario", "Luigi", "Bowser", "Sonic"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/a/a9/MarioPortrait.png",
            "https://upload.wikimedia.org/wikipedia/en/7/73/Luigi_MACW.png",
            "https://upload.wikimedia.org/wikipedia/en/f/f6/Bowser_-_Super_Mario_Bros_Wonder.png",
            "https://upload.wikimedia.org/wikipedia/en/2/28/Sonic_the_Hedgehog.png"
        ],
        "spy": "Sonic"
    },
    {
        "names": ["Scorpion", "Sub-Zero", "Raiden", "Ryu"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/a/a2/Scorpion_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/3/38/Sub-Zero_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/a/a9/Raiden_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/e/e5/Ryu_SF6.png"
        ],
        "spy": "Ryu"
    },
    {
        "names": ["Joel", "Ellie", "Clicker", "Nathan Drake"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/2/24/Joel_TLOU.jpg",
            "https://upload.wikimedia.org/wikipedia/en/f/fa/Ellie_The_Last_of_Us_Part_II.png",
            d("Clicker"),
            "https://upload.wikimedia.org/wikipedia/en/5/5f/Nathan_Drake_U4.png"
        ],
        "spy": "Nathan Drake"
    },
    {
        "names": ["Leon S. Kennedy", "Claire Redfield", "Chris Redfield", "Pyramid Head"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/1/1c/Leon_S._Kennedy.png",
            "https://upload.wikimedia.org/wikipedia/en/9/9e/Claire_Redfield_RE2_Remake.png",
            "https://upload.wikimedia.org/wikipedia/en/9/90/Chris_Redfield_RE_Village.png",
            "https://upload.wikimedia.org/wikipedia/en/3/36/Pyramid_Head.png"
        ],
        "spy": "Pyramid Head"
    },
    {
        "names": ["Jett", "Phoenix", "Sage", "Yasuo"],
        "urls": [
            d("Jett"), d("Phoenix"), d("Sage"),
            "https://upload.wikimedia.org/wikipedia/en/1/1a/Yasuo_LoL_splash.jpg"
        ],
        "spy": "Yasuo"
    },
    {
        "names": ["Steve", "Alex", "Enderman", "Roblox Noob"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/3/34/Steve_%28Minecraft%29.png",
            d("Alex"), d("Enderman"), d("Roblox Noob")
        ],
        "spy": "Roblox Noob"
    },
    {
        "names": ["Jinx", "Vi", "Caitlyn", "Pudge"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/9/96/Jinx_from_League_of_Legends.jpg",
            d("Vi"), d("Caitlyn"), d("Pudge")
        ],
        "spy": "Pudge"
    },
    {
        "names": ["Lara Croft", "Jonah", "Roth", "Aloy"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/f/f1/Lara_Croft_Shadow_of_the_Tomb_Raider.png",
            d("Jonah"), d("Roth"), 
            "https://upload.wikimedia.org/wikipedia/en/9/94/Aloy_Horizon_Forbidden_West.png"
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
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
                local_urls.append(f"/{filepath}")
            except Exception as e:
                print(f"Failed to download {names[i]}: {e}")
                local_urls.append(d(names[i]))
        else:
            local_urls.append(url) # keep dummy
            
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
print("Casus Kim: Oyun Karakterleri FIXED successfully!")
