import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Insert Game
cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "Casus Kim: Oyun Karakterleri", 
    "Her soruda 3 karakter aynı oyundan, 1 karakter farklı bir oyundan. Aralarındaki casusu bulabilir misin? En hızlı bulan kazanır!",
    "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?auto=format&fit=crop&q=80&w=800", # Gaming console
    "Oyun",
    "casus_kim",
    0
))
oyun_id = cur.fetchone()[0]

def d(name):
    import urllib.parse
    return f"https://dummyimage.com/600x600/151520/ffffff&text={urllib.parse.quote(name)}"

questions = [
    {
        "names": ["Michael (GTA)", "Trevor (GTA)", "Franklin (GTA)", "Arthur (RDR)"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/e/e4/Michael_De_Santa.png",
            "https://upload.wikimedia.org/wikipedia/en/7/75/Trevor_Philips.png",
            "https://upload.wikimedia.org/wikipedia/en/3/3b/Franklin_Clinton.png",
            "https://upload.wikimedia.org/wikipedia/en/3/3b/Arthur_Morgan.png"
        ],
        "spy": "Arthur (RDR)"
    },
    {
        "names": ["Geralt (Witcher)", "Ciri (Witcher)", "Yennefer (Witcher)", "Kratos (GoW)"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/8/88/Geralt_of_Rivia.png",
            "https://upload.wikimedia.org/wikipedia/en/4/45/Ciri_The_Witcher_3.png",
            "https://upload.wikimedia.org/wikipedia/en/9/90/Yennefer_of_Vengerberg.png",
            "https://upload.wikimedia.org/wikipedia/en/a/a5/Kratos_PS4.jpg"
        ],
        "spy": "Kratos (GoW)"
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
        "names": ["Scorpion (MK)", "Sub-Zero (MK)", "Raiden (MK)", "Ryu (SF)"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/a/a2/Scorpion_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/3/38/Sub-Zero_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/a/a9/Raiden_MK11.png",
            "https://upload.wikimedia.org/wikipedia/en/e/e5/Ryu_SF6.png"
        ],
        "spy": "Ryu (SF)"
    },
    {
        "names": ["Joel (TLOU)", "Ellie (TLOU)", "Clicker (TLOU)", "Nathan Drake"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/2/24/Joel_TLOU.jpg",
            "https://upload.wikimedia.org/wikipedia/en/f/fa/Ellie_The_Last_of_Us_Part_II.png",
            d("Clicker"),
            "https://upload.wikimedia.org/wikipedia/en/5/5f/Nathan_Drake_U4.png"
        ],
        "spy": "Nathan Drake"
    },
    {
        "names": ["Leon (RE)", "Claire (RE)", "Chris (RE)", "Pyramid Head"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/1/1c/Leon_S._Kennedy.png",
            "https://upload.wikimedia.org/wikipedia/en/9/9e/Claire_Redfield_RE2_Remake.png",
            "https://upload.wikimedia.org/wikipedia/en/9/90/Chris_Redfield_RE_Village.png",
            "https://upload.wikimedia.org/wikipedia/en/3/36/Pyramid_Head.png"
        ],
        "spy": "Pyramid Head"
    },
    {
        "names": ["Jett (Valorant)", "Phoenix (Valorant)", "Sage (Valorant)", "Yasuo (LoL)"],
        "urls": [
            d("Jett"), d("Phoenix"), d("Sage"),
            "https://upload.wikimedia.org/wikipedia/en/1/1a/Yasuo_LoL_splash.jpg"
        ],
        "spy": "Yasuo (LoL)"
    },
    {
        "names": ["Steve (MC)", "Alex (MC)", "Enderman (MC)", "Roblox Noob"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/3/34/Steve_%28Minecraft%29.png",
            d("Alex"), d("Enderman"), d("Roblox Noob")
        ],
        "spy": "Roblox Noob"
    },
    {
        "names": ["Jinx (LoL)", "Vi (LoL)", "Caitlyn (LoL)", "Pudge (Dota)"],
        "urls": [
            "https://upload.wikimedia.org/wikipedia/en/9/96/Jinx_from_League_of_Legends.jpg",
            d("Vi"), d("Caitlyn"), d("Pudge")
        ],
        "spy": "Pudge (Dota)"
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

for q in questions:
    names = q['names']
    urls = q['urls']
    spy = q['spy']
    
    # Bundle names and urls
    bundled = list(zip(names, urls))
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
print("Casus Kim: Oyun Karakterleri seeded successfully!")
