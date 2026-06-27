import os
import psycopg2
import requests
import time
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

def get_wiki_image(title):
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "format": "json",
            "pithumbsize": 500
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, params=params, headers=headers).json()
        pages = res.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                return page_data['thumbnail']['source']
    except Exception as e:
        print(f"Error fetching {title}: {e}")
    return None

wiki_titles = {
    "Esaretin Bedeli (1994)": "The_Shawshank_Redemption",
    "Baba (1972)": "The_Godfather",
    "Kara Şövalye (2008)": "The_Dark_Knight",
    "Baba 2 (1974)": "The_Godfather_Part_II",
    "12 Öfkeli Adam (1957)": "12_Angry_Men_(1957_film)",
    "Schindler'in Listesi (1993)": "Schindler's_List",
    "Yüzüklerin Efendisi: Kralın Dönüşü": "The_Lord_of_the_Rings:_The_Return_of_the_King",
    "Ucuz Roman (1994)": "Pulp_Fiction",
    "Yüzüklerin Efendisi: Yüzük Kardeşliği": "The_Lord_of_the_Rings:_The_Fellowship_of_the_Ring",
    "İyi, Kötü ve Çirkin (1966)": "The_Good,_the_Bad_and_the_Ugly",
    "Forrest Gump (1994)": "Forrest_Gump",
    "Dövüş Kulübü (1999)": "Fight_Club",
    "Yüzüklerin Efendisi: İki Kule": "The_Lord_of_the_Rings:_The_Two_Towers",
    "Başlangıç (Inception)": "Inception",
    "Yıldız Savaşları: İmparator": "The_Empire_Strikes_Back",
    "The Matrix (1999)": "The_Matrix",
    "Sıkı Dostlar (Goodfellas)": "Goodfellas",
    "Guguk Kuşu (1975)": "One_Flew_Over_the_Cuckoo's_Nest_(film)",
    "Yedi (Se7en)": "Seven_(1995_film)",
    "Şahane Hayat (1946)": "It's_a_Wonderful_Life"
}

cur.execute("SELECT id FROM oyun WHERE baslik='IMDb Top 20: En İyi Film Hangisi?' ORDER BY id DESC LIMIT 1")
row = cur.fetchone()
if not row:
    print("Oyun bulunamadı!")
    exit()
oyun_id = row[0]

cur.execute("SELECT id, secenekler FROM soru WHERE oyun_id=%s ORDER BY id", (oyun_id,))
sorular = cur.fetchall()

for s_id, secenekler in sorular:
    parts = secenekler.split(',')
    film1 = parts[0]
    film2 = parts[1]
    
    img1 = get_wiki_image(wiki_titles[film1])
    img2 = get_wiki_image(wiki_titles[film2])
    
    print(f"{film1}: {img1}")
    print(f"{film2}: {img2}")
    
    if img1 and img2:
        cur.execute("UPDATE soru SET resim_url=%s, resim_url_2=%s WHERE id=%s", (img1, img2, s_id))
    time.sleep(0.5)

conn.commit()
cur.close()
conn.close()
print("IMDb Top 20 game images updated successfully!")
