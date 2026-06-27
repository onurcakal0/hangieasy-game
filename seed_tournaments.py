import urllib.request
import urllib.parse
import json
import os
import time
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

movies = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight", "The Godfather Part II", "12 Angry Men", 
    "Schindler's List", "The Lord of the Rings: The Return of the King", "Pulp Fiction", "The Lord of the Rings: The Fellowship of the Ring", "The Good, the Bad and the Ugly", 
    "Forrest Gump", "Fight Club", "The Lord of the Rings: The Two Towers", "Inception", "Star Wars: Episode V - The Empire Strikes Back", 
    "The Matrix", "Goodfellas", "One Flew Over the Cuckoo's Nest", "Se7en", "It's a Wonderful Life", 
    "Seven Samurai", "The Silence of the Lambs", "Saving Private Ryan", "City of God", "Interstellar", 
    "Life Is Beautiful", "The Green Mile", "Star Wars: Episode IV - A New Hope", "Terminator 2: Judgment Day", "Back to the Future", 
    "Spirited Away", "The Pianist", "Psycho", "Parasite", "Leon: The Professional", 
    "Gladiator", "The Lion King", "American History X", "The Departed", "Whiplash", 
    "The Prestige", "The Usual Suspects", "Casablanca", "Grave of the Fireflies", "Harakiri", 
    "The Intouchables", "Modern Times", "Once Upon a Time in the West", "Cinema Paradiso", "Rear Window"
]

tv_shows = [
    "Breaking Bad", "Planet Earth II", "Planet Earth", "Band of Brothers", "Chernobyl", 
    "The Wire", "Blue Planet II", "Avatar: The Last Airbender", "Cosmos: A Spacetime Odyssey", "The Sopranos", 
    "Cosmos", "Our Planet", "Game of Thrones", "Rick and Morty", "The World at War", 
    "Fullmetal Alchemist: Brotherhood", "The Last Dance", "Life", "Sherlock", "The Twilight Zone", 
    "Batman: The Animated Series", "Scam 1992", "Arcane", "The Blue Planet", "Attack on Titan", 
    "The Office", "Firefly", "Human Planet", "Frozen Planet", "Death Note", 
    "Only Fools and Horses", "True Detective", "The Civil War", "Hunter x Hunter", "The Beatles: Get Back", 
    "Fargo", "Persona", "Dekalog", "The Mandalorian", "Better Call Saul", 
    "Cowboy Bebop", "Nathan for You", "Gravity Falls", "Twin Peaks", "Friends", 
    "The Crown", "Stranger Things", "Black Mirror", "Peaky Blinders", "Succession"
]

def get_poster(title):
    try:
        url = "http://www.omdbapi.com/?apikey=trilogy&t=" + urllib.parse.quote(title)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        return data.get('Poster')
    except:
        return None

def process_tournament(title, desc, items, folder_name, category):
    print(f"Creating tournament: {title}")
    
    # Create cover using first item
    main_cover_url = get_poster(items[0])
    if not main_cover_url or main_cover_url == "N/A":
        main_cover_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800&auto=format&fit=crop"
        
    cur.execute('''
        INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    ''', (title, desc, main_cover_url, category, "omu_bumu", 0))
    oyun_id = cur.fetchone()[0]
    
    dir_path = f"static/img/{folder_name}"
    os.makedirs(dir_path, exist_ok=True)
    
    for i in range(0, 50, 2):
        item1 = items[i]
        item2 = items[i+1]
        
        poster1 = get_poster(item1)
        poster2 = get_poster(item2)
        
        if not poster1 or poster1 == "N/A": poster1 = main_cover_url
        if not poster2 or poster2 == "N/A": poster2 = main_cover_url
        
        # Download images
        path1 = f"{dir_path}/{i}.jpg"
        path2 = f"{dir_path}/{i+1}.jpg"
        
        try:
            urllib.request.urlretrieve(poster1, path1)
            urllib.request.urlretrieve(poster2, path2)
        except:
            print(f"Failed to download for {item1} or {item2}, using URLs")
            path1 = poster1
            path2 = poster2
            
        final_path1 = f"/{path1}" if not path1.startswith("http") else path1
        final_path2 = f"/{path2}" if not path2.startswith("http") else path2
        
        resim_url = f"{final_path1},{final_path2}"
        secenekler = f"{item1},{item2}"
        dogru_cevap = "Farketmez"
        
        cur.execute('''
            INSERT INTO soru (oyun_id, secenekler, dogru_cevap, resim_url)
            VALUES (%s, %s, %s, %s)
        ''', (oyun_id, secenekler, dogru_cevap, resim_url))
        print(f"Added pair: {item1} vs {item2}")
        time.sleep(0.5)

# Clear existing if any
cur.execute("DELETE FROM oyun WHERE baslik LIKE '%IMDB%'")

process_tournament(
    "Dizi Tarihinin En İyi Dizisi (IMDB Top 50)",
    "IMDB'nin en yüksek puanlı 50 dizisini turnuva ağacında çarpıştırıyoruz. Sana göre gelmiş geçmiş en iyi dizi hangisi? Tarafını seç, şampiyonu belirle!",
    tv_shows,
    "tv_tournament",
    "Dizi & Film"
)

process_tournament(
    "Film Tarihinin En İyi Filmi (IMDB Top 50)",
    "IMDB'nin en efsanevi 50 filmini karşı karşıya getiriyoruz. Sence sinema tarihinin en iyi başyapıtı hangisi? Elemeleri geç ve favorini zafere taşı!",
    movies,
    "movie_tournament",
    "Dizi & Film"
)

conn.commit()
cur.close()
conn.close()
print("Tournaments seeded successfully!")
