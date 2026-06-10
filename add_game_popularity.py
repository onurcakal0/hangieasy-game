import random
from app import app, db, Oyun, Soru, Kullanici

# Steam oyunları ve tüm zamanların anlık oyuncu rekoru (All-Time Peak Concurrent Players)
# Steam App IDs are used to fetch high-quality adblock-safe images from Akamai CDN
games = [
    {"isim": "PUBG: Battlegrounds", "puan": 3257248, "app_id": 578080},
    {"isim": "Palworld", "puan": 2101867, "app_id": 1623730},
    {"isim": "Counter-Strike 2", "puan": 1818773, "app_id": 730},
    {"isim": "Lost Ark", "puan": 1325305, "app_id": 1599340},
    {"isim": "Dota 2", "puan": 1295114, "app_id": 570},
    {"isim": "Cyberpunk 2077", "puan": 1054388, "app_id": 1091500},
    {"isim": "Elden Ring", "puan": 953426, "app_id": 1245620},
    {"isim": "Banana", "puan": 917272, "app_id": 2923300},
    {"isim": "New World", "puan": 913634, "app_id": 1063730},
    {"isim": "Hogwarts Legacy", "puan": 879308, "app_id": 990080},
    {"isim": "Baldur's Gate 3", "puan": 875343, "app_id": 1086940},
    {"isim": "Black Myth: Wukong", "puan": 2415714, "app_id": 2358720},
    {"isim": "Apex Legends", "puan": 624473, "app_id": 1172470},
    {"isim": "Valheim", "puan": 502387, "app_id": 892970},
    {"isim": "Terraria", "puan": 489886, "app_id": 105600},
    {"isim": "Helldivers 2", "puan": 458709, "app_id": 553850},
    {"isim": "Among Us", "puan": 438524, "app_id": 945360},
    {"isim": "Grand Theft Auto V", "puan": 364548, "app_id": 271590},
    {"isim": "Monster Hunter: World", "puan": 334684, "app_id": 582010},
    {"isim": "Destiny 2", "puan": 316750, "app_id": 1085660},
    {"isim": "Rust", "puan": 244394, "app_id": 252490},
    {"isim": "Team Fortress 2", "puan": 253997, "app_id": 440},
    {"isim": "The Witcher 3: Wild Hunt", "puan": 103329, "app_id": 292030},
    {"isim": "Left 4 Dead 2", "puan": 162423, "app_id": 550},
    {"isim": "Stardew Valley", "puan": 236614, "app_id": 413150},
    {"isim": "The Elder Scrolls V: Skyrim", "puan": 287411, "app_id": 489830},
    {"isim": "Fallout 4", "puan": 472962, "app_id": 377160},
    {"isim": "Lethal Company", "puan": 240817, "app_id": 1966720},
    {"isim": "Phasmophobia", "puan": 112717, "app_id": 739630},
    {"isim": "Dead by Daylight", "puan": 105093, "app_id": 381210}
]

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Kim Daha Popüler: Steam Rekorları').first()
    if eski_oyun:
        Soru.query.filter_by(oyun_id=eski_oyun.id).delete()
        db.session.delete(eski_oyun)
        db.session.commit()

    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Kim Daha Popüler: Steam Rekorları',
        aciklama='Hangi oyunun aynı anda daha fazla kişi tarafından oynandığını tahmin edebilir misin? Karşında Steam eşzamanlı oyuncu rekorları!',
        resim_url='https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/730/header.jpg', # CS2
        kategori='Spor', # Ya da Oyun kategorisi, spor espor altinda
        oyun_modu='kim_populer',
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    # 30 oyunu ikili gruplara ayırarak soru oluştur (Frontend hepsini ayırıp karıştıracak zaten)
    random.shuffle(games)
    
    for i in range(0, len(games), 2):
        oyun1 = games[i]
        oyun2 = games[i+1]
        
        # secenekler string = "Isim=Puan, Isim=Puan"
        secenekler = f"{oyun1['isim']}={oyun1['puan']},{oyun2['isim']}={oyun2['puan']}"
        
        # resimler string = "url1, url2"
        url1 = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{oyun1['app_id']}/header.jpg"
        url2 = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{oyun2['app_id']}/header.jpg"
        resim_url = f"{url1},{url2}"
        
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=resim_url,
            secenekler=secenekler,
            dogru_cevap="" # Kim populer modunda dogru_cevap backendde tutulmuyor, frontend puana gore anliyor
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print("✅ Kim Daha Popüler: Steam Rekorları başarıyla eklendi!")
