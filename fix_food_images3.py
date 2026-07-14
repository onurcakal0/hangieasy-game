import requests
import urllib.parse
from bs4 import BeautifulSoup
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

def get_wiki_html_image(title):
    try:
        url_title = urllib.parse.quote(title.replace(' ', '_'))
        res = requests.get(f'https://tr.wikipedia.org/wiki/{url_title}', headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        img = soup.select_one('.infobox img') or soup.select_one('.thumb img')
        if img and img.has_attr('src'):
            src = 'https:' + img['src']
            # Make image higher resolution
            if 'px-' in src:
                import re
                src = re.sub(r'\d+px-', '600px-', src)
            return src
        return None
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None

pairs = [
    {"f1": "Kokoreç", "f2": "Islak hamburger"},
    {"f1": "Çiğ köfte", "f2": "Midye dolma"},
    {"f1": "Döner", "f2": "Tantuni"},
    {"f1": "Lahmacun", "f2": "Pizza"},
    {"f1": "İşkembe çorbası", "f2": "Kelle paça"},
    {"f1": "Tost", "f2": "Gözleme"},
    {"f1": "Patates kızartması", "f2": "Soğan halkası"},
    {"f1": "Hamburger", "f2": "Sosisli sandviç"},
    {"f1": "Sucuk", "f2": "Pastırma"},
    {"f1": "Kumpir", "f2": "Boyoz"}
]

print("Fetching correct food images from Wikipedia HTML...")

cur.execute("SELECT id FROM oyun WHERE baslik = %s LIMIT 1", ("Gece Acıkınca Yenilecek En İyi Yemek",))
oyun_id = cur.fetchone()[0]

for pair in pairs:
    img1 = get_wiki_html_image(pair["f1"])
    img2 = get_wiki_html_image(pair["f2"])
    
    # Fallbacks in case Wikipedia page missing
    if not img1: img1 = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600"
    if not img2: img2 = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600"
    
    resim_url = f"{img1},{img2}"
    secenekler = f"{pair['f1']},{pair['f2']}"
    
    cur.execute('''
        UPDATE soru 
        SET resim_url = %s
        WHERE oyun_id = %s AND secenekler = %s
    ''', (resim_url, oyun_id, secenekler))
    print(f"Updated {pair['f1']} vs {pair['f2']}")

conn.commit()
cur.close()
conn.close()
print("All images correctly updated via Wikipedia HTML scraping!")
