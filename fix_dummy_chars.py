import os
import psycopg2
import urllib.request
import re
import time
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id, soru_metni, resim_url FROM hangisi_soru WHERE resim_url LIKE '%dummyimage.com%' AND soru_metni LIKE '%ikonik karakter%'")
rows = cur.fetchall()

wiki_map = {
    "Mario": "Mario",
    "Lara Croft": "Lara_Croft",
    "Link": "Link_(The_Legend_of_Zelda)",
    "Arthur Morgan": "Arthur_Morgan_(Red_Dead)",
    "Ellie": "Ellie_(The_Last_of_Us)",
    "Gordon Freeman": "Gordon_Freeman",
    "Doomguy": "Doomguy",
    "Ezio Auditore": "Ezio_Auditore_da_Firenze",
    "Cloud Strife": "Cloud_Strife",
    "Ryu": "Ryu_(Street_Fighter)",
    "Scorpion": "Scorpion_(Mortal_Kombat)",
    "Pikachu": "Pikachu",
    "Pac-Man": "Pac-Man_(character)",
    "Steve": "Steve_(Minecraft)"
}

print(f"Found {len(rows)} dummy images to fix.")

for row in rows:
    q_id = row[0]
    soru = row[1]
    
    char_match = re.search(r'\((.*?)\)', soru)
    if char_match:
        char_name = char_match.group(1)
        if char_name in wiki_map:
            wiki_url = f"https://en.wikipedia.org/wiki/{wiki_map[char_name]}"
            try:
                req = urllib.request.Request(wiki_url, headers={'User-Agent': 'HangiEasyBot/1.0 (onur@hangieasy.com)'})
                html = urllib.request.urlopen(req).read().decode('utf-8')
                match = re.search(r'meta property="og:image" content="(.*?)"', html)
                if match:
                    img_url = match.group(1)
                    filepath = f"static/img/games/char_fixed_{q_id}.jpg"
                    req_img = urllib.request.Request(img_url, headers={'User-Agent': 'HangiEasyBot/1.0'})
                    with urllib.request.urlopen(req_img) as response, open(filepath, 'wb') as out_file:
                        out_file.write(response.read())
                    cur.execute("UPDATE hangisi_soru SET resim_url = %s WHERE id = %s", (f"/{filepath}", q_id))
                    print(f"Fixed: {char_name}")
                else:
                    print(f"No og:image for {char_name}")
            except Exception as e:
                print(f"Error fixing {char_name}: {e}")
            time.sleep(1)

conn.commit()
cur.close()
conn.close()
print("Fix completed.")
