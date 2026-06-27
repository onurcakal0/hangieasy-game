import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# 1. FIX AI OR REAL
ai_real_urls = [
    # REAL (Picsum reliable images)
    "https://picsum.photos/id/1011/800/600",
    "https://picsum.photos/id/1025/800/600",
    "https://picsum.photos/id/1043/800/600",
    "https://picsum.photos/id/1062/800/600",
    "https://picsum.photos/id/1074/800/600",
    "https://picsum.photos/id/1084/800/600",
    "https://picsum.photos/id/111/800/600",
    "https://picsum.photos/id/129/800/600",
    "https://picsum.photos/id/145/800/600",
    "https://picsum.photos/id/15/800/600",
    
    # AI (Pollinations AI reliable generated images)
    "https://image.pollinations.ai/prompt/A%20hyper%20realistic%20cyberpunk%20cityscape%20with%20neon%20lights?width=800&height=600&seed=1",
    "https://image.pollinations.ai/prompt/A%20hyper%20realistic%20portrait%20of%20a%20cyborg%20human?width=800&height=600&seed=2",
    "https://image.pollinations.ai/prompt/A%20realistic%20photo%20of%20an%20alien%20landscape%20with%20two%20suns?width=800&height=600&seed=3",
    "https://image.pollinations.ai/prompt/A%20hyper-detailed%20dragon%20breathing%20blue%20fire?width=800&height=600&seed=4",
    "https://image.pollinations.ai/prompt/A%20futuristic%20robot%20dog%20in%20a%20park?width=800&height=600&seed=5",
    "https://image.pollinations.ai/prompt/A%20surreal%20floating%20island%20in%20the%20sky%20with%20waterfalls?width=800&height=600&seed=6",
    "https://image.pollinations.ai/prompt/A%20magical%20forest%20with%20glowing%20mushrooms?width=800&height=600&seed=7",
    "https://image.pollinations.ai/prompt/An%20astronaut%20riding%20a%20horse%20on%20Mars?width=800&height=600&seed=8",
    "https://image.pollinations.ai/prompt/A%20giant%20steampunk%20clockwork%20owl?width=800&height=600&seed=9",
    "https://image.pollinations.ai/prompt/A%20hyper%20realistic%20glass%20frog%20on%20a%20leaf?width=800&height=600&seed=10"
]

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Yapay Zeka Mı? Gerçek Mi?' LIMIT 1")
oyun1 = cur.fetchone()
if oyun1:
    cur.execute("SELECT id, dogru_cevap FROM hangisi_soru WHERE oyun_id = %s ORDER BY id", (oyun1[0],))
    sorular1 = cur.fetchall()
    
    real_idx = 0
    ai_idx = 10
    
    for s_id, dogru in sorular1:
        # If dogru == 'A' (Yapay Zeka) -> use AI image
        # If dogru == 'B' (Gerçek) -> use Real image
        if dogru == 'A':
            url = ai_real_urls[ai_idx]
            ai_idx += 1
        else:
            url = ai_real_urls[real_idx]
            real_idx += 1
            
        cur.execute("UPDATE hangisi_soru SET resim_url = %s WHERE id = %s", (url, s_id))

# 2. FIX MOVIES
tmdb_base = "https://image.tmdb.org/t/p/w500"
movie_posters = {
    "Baba (The Godfather)": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Titanik": "/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "Avatar": "/kyeqWdyQkGAk5CRJvXQGv23T6m.jpg",
    "Kara Şövalye": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Forrest Gump": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
    "The Matrix": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Başlangıç (Inception)": "/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
    "Yüzüklerin Efendisi": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
    "Yıldızlararası": "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "Harry Potter": "/wuMc08IPKEb2GTrH186A911Z0z1.jpg",
    "Yenilmezler (Avengers)": "/RYMX2wcKCBAr24UyPD7xrm17o8.jpg",
    "Jurassic Park": "/oU7Oq2kFAAlGqbB4LSx1s0t4tD9.jpg",
    "Yıldız Savaşları (Star Wars)": "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg",
    "Örümcek Adam": "/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg",
    "Joker": "/udDclJoHjfpt8MvSMzNDI141nK.jpg",
    "Aslan Kral": "/sKCr78AS8X5b5F4Mv710H3yT7N9.jpg",
    "Gladyatör": "/ty8TGRWQ10BTEH44sZQxQvkG2wO.jpg",
    "Geleceğe Dönüş": "/fNOH9f126iA4XvO3D2r1o5yM3gJ.jpg",
    "Ucuz Roman (Pulp Fiction)": "/d5iIlFn5s0ImszYzBPbOYQe2gWl.jpg",
    "Dövüş Kulübü": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"
}

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Resimdeki Filmi Tahmin Edebilir Misin?' LIMIT 1")
oyun2 = cur.fetchone()
if oyun2:
    for brand, path in movie_posters.items():
        full_url = tmdb_base + path
        cur.execute("""
            UPDATE hangisi_soru 
            SET resim_url = %s 
            WHERE oyun_id = %s AND (
                (secenek_a = %s AND dogru_cevap = 'A') OR
                (secenek_b = %s AND dogru_cevap = 'B') OR
                (secenek_c = %s AND dogru_cevap = 'C') OR
                (secenek_d = %s AND dogru_cevap = 'D')
            )
        """, (full_url, oyun2[0], brand, brand, brand, brand))


# 3. FIX LOGOS (Use Clearbit for all to be 100% safe)
logo_domains = {
    "Apple": "apple.com", "Nike": "nike.com", "McDonald's": "mcdonalds.com",
    "Mercedes-Benz": "mercedes-benz.com", "Audi": "audi.com", "Pepsi": "pepsi.com",
    "Spotify": "spotify.com", "Target": "target.com", "Shell": "shell.com",
    "Adidas": "adidas.com", "Toyota": "toyota.com", "Instagram": "instagram.com",
    "Puma": "puma.com", "Lacoste": "lacoste.com", "Windows": "microsoft.com",
    "Android": "android.com", "Google Chrome": "google.com", "WWF": "worldwildlife.org",
    "NBC": "nbc.com", "BP": "bp.com", "Unilever": "unilever.com",
    "Mastercard": "mastercard.com", "Chanel": "chanel.com", "Mitsubishi": "mitsubishi.com",
    "Playboy": "playboy.com", "Olimpiyatlar": "olympics.com", "X (Twitter)": "x.com",
    "TikTok": "tiktok.com", "Snapchat": "snapchat.com", "Pinterest": "pinterest.com"
}

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik = 'Kaç Logo Biliyorsun? (Zor Seviye)' LIMIT 1")
oyun3 = cur.fetchone()
if oyun3:
    for brand, domain in logo_domains.items():
        full_url = f"https://logo.clearbit.com/{domain}"
        cur.execute("""
            UPDATE hangisi_soru 
            SET resim_url = %s 
            WHERE oyun_id = %s AND (
                (secenek_a = %s AND dogru_cevap = 'A') OR
                (secenek_b = %s AND dogru_cevap = 'B') OR
                (secenek_c = %s AND dogru_cevap = 'C') OR
                (secenek_d = %s AND dogru_cevap = 'D')
            )
        """, (full_url, oyun3[0], brand, brand, brand, brand))

conn.commit()
cur.close()
conn.close()
print("All images updated with robust sources!")
