import os
import psycopg2
from dotenv import load_dotenv
import random
import urllib.request

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Insert Game
cur.execute('''
    INSERT INTO hangisi_oyun (baslik, aciklama, resim_url, olusturan_adi) 
    VALUES (%s, %s, %s, %s) RETURNING id
''', (
    "Kaç Logo Biliyorsun? (Zor Seviye)", 
    "İsimleri gizledik! Sadece amblemlere bakarak bu dünya devi 30 markayı tanıyabilecek misin? Süren 20 saniye!",
    "https://images.unsplash.com/photo-1601158935942-52255782d322?q=80&w=800&auto=format&fit=crop", # Generic colorful brand/neon image
    "HangiEasy"
))
oyun_id = cur.fetchone()[0]

sorular_data = [
    {"img": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg", "correct": "Apple", "wrongs": ["Samsung", "Microsoft", "Huawei"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg", "correct": "Nike", "wrongs": ["Adidas", "Puma", "Reebok"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg", "correct": "McDonald's", "wrongs": ["Burger King", "KFC", "Wendy's"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/9/90/Mercedes-Logo.svg", "correct": "Mercedes-Benz", "wrongs": ["BMW", "Audi", "Volkswagen"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/9/92/Audi-Logo_2016.svg", "correct": "Audi", "wrongs": ["Mercedes-Benz", "Porsche", "Lexus"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Pepsi_logo_2014.svg", "correct": "Pepsi", "wrongs": ["Coca-Cola", "Fanta", "Sprite"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", "correct": "Spotify", "wrongs": ["Apple Music", "SoundCloud", "Tidal"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Target_Corporation_logo_%28vector%29.svg", "correct": "Target", "wrongs": ["Walmart", "Kmart", "Costco"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/e/e8/Shell_logo.svg", "correct": "Shell", "wrongs": ["BP", "Chevron", "ExxonMobil"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg", "correct": "Adidas", "wrongs": ["Nike", "Under Armour", "New Balance"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Toyota_carlogo.svg", "correct": "Toyota", "wrongs": ["Honda", "Nissan", "Hyundai"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", "correct": "Instagram", "wrongs": ["Facebook", "Snapchat", "TikTok"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/8/86/Puma_Logo.svg", "correct": "Puma", "wrongs": ["Jaguar", "Slazenger", "Lacoste"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/2/25/Lacoste_logo.svg", "correct": "Lacoste", "wrongs": ["Ralph Lauren", "Tommy Hilfiger", "Crocs"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg", "correct": "Windows", "wrongs": ["Google", "Intel", "IBM"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Android_robot.svg", "correct": "Android", "wrongs": ["Linux", "WhatsApp", "Line"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Google_Chrome_icon_%28February_2022%29.svg", "correct": "Google Chrome", "wrongs": ["Firefox", "Safari", "Edge"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/2/24/WWF_logo.svg", "correct": "WWF", "wrongs": ["Greenpeace", "PETA", "Animal Planet"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/NBC_logo.svg", "correct": "NBC", "wrongs": ["CBS", "ABC", "Fox"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/d/d3/BP_Helios_logo.svg", "correct": "BP", "wrongs": ["Shell", "Total", "Sunoco"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/8/8e/Unilever_logo.svg", "correct": "Unilever", "wrongs": ["P&G", "Nestle", "Johnson & Johnson"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/b/b7/MasterCard_Logo.svg", "correct": "Mastercard", "wrongs": ["Visa", "American Express", "Discover"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/9/92/Chanel_logo_interlocking_cs.svg", "correct": "Chanel", "wrongs": ["Gucci", "Louis Vuitton", "Prada"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Mitsubishi_logo.svg", "correct": "Mitsubishi", "wrongs": ["Subaru", "Suzuki", "Mazda"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/5/58/Playboy_bunny.svg", "correct": "Playboy", "wrongs": ["Bugs Bunny", "Energizer", "Nesquik"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", "correct": "Olimpiyatlar", "wrongs": ["FİFA", "UEFA", "NBA"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg", "correct": "X (Twitter)", "wrongs": ["Threads", "Discord", "Twitch"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg", "correct": "TikTok", "wrongs": ["Instagram", "Kwai", "Snapchat"]},
    {"img": "https://upload.wikimedia.org/wikipedia/en/c/c4/Snapchat_logo.svg", "correct": "Snapchat", "wrongs": ["Telegram", "WhatsApp", "Bumble"]},
    {"img": "https://upload.wikimedia.org/wikipedia/commons/0/08/Pinterest-logo.png", "correct": "Pinterest", "wrongs": ["Tumblr", "Reddit", "Flickr"]}
]

for s in sorular_data:
    options = s['wrongs'] + [s['correct']]
    random.shuffle(options)
    
    dogru_harf = ""
    if options[0] == s['correct']: dogru_harf = "A"
    elif options[1] == s['correct']: dogru_harf = "B"
    elif options[2] == s['correct']: dogru_harf = "C"
    else: dogru_harf = "D"
    
    cur.execute('''
        INSERT INTO hangisi_soru (oyun_id, soru_metni, resim_url, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (oyun_id, "Bu amblem hangi dünya markasına ait?", s['img'], options[0], options[1], options[2], options[3], dogru_harf))

conn.commit()
cur.close()
conn.close()
print("Logos Game Seeded Successfully!")
