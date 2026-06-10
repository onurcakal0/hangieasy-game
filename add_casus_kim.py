import random
from app import app, db, Oyun, Soru, Kullanici

# Steam CDN (Adblocker takılmaz) kullanarak Efsanevi Oyun Stüdyoları
studyolar = {
    "Rockstar Games": [
        {"isim": "Grand Theft Auto V", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/271590/header.jpg"},
        {"isim": "Red Dead Redemption 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/header.jpg"},
        {"isim": "Grand Theft Auto IV", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/12210/header.jpg"},
        {"isim": "Max Payne 3", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/204100/header.jpg"},
        {"isim": "L.A. Noire", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/110800/header.jpg"}
    ],
    "CD Projekt RED": [
        {"isim": "The Witcher 3: Wild Hunt", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/292030/header.jpg"},
        {"isim": "Cyberpunk 2077", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1091500/header.jpg"},
        {"isim": "The Witcher 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/20920/header.jpg"},
        {"isim": "Thronebreaker", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/973760/header.jpg"},
        {"isim": "The Witcher", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/20900/header.jpg"}
    ],
    "Bethesda Game Studios": [
        {"isim": "The Elder Scrolls V: Skyrim", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/489830/header.jpg"},
        {"isim": "Fallout 4", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/377160/header.jpg"},
        {"isim": "Starfield", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1716740/header.jpg"},
        {"isim": "Fallout 3", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/22370/header.jpg"},
        {"isim": "Oblivion", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/22330/header.jpg"}
    ],
    "FromSoftware": [
        {"isim": "Elden Ring", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg"},
        {"isim": "Dark Souls III", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/374320/header.jpg"},
        {"isim": "Sekiro: Shadows Die Twice", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/814380/header.jpg"},
        {"isim": "Dark Souls II", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/335300/header.jpg"},
        {"isim": "Dark Souls Remastered", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/570940/header.jpg"}
    ],
    "Valve": [
        {"isim": "Half-Life 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/220/header.jpg"},
        {"isim": "Portal 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/620/header.jpg"},
        {"isim": "Left 4 Dead 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/550/header.jpg"},
        {"isim": "Counter-Strike 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/730/header.jpg"},
        {"isim": "Team Fortress 2", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/440/header.jpg"}
    ],
    "Capcom": [
        {"isim": "Resident Evil 4", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2050650/header.jpg"},
        {"isim": "Monster Hunter: World", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/582010/header.jpg"},
        {"isim": "Devil May Cry 5", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/601150/header.jpg"},
        {"isim": "Street Fighter 6", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1364780/header.jpg"},
        {"isim": "Resident Evil Village", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1196590/header.jpg"}
    ],
    "PlayStation Studios": [
        {"isim": "God of War", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1593500/header.jpg"},
        {"isim": "Marvel's Spider-Man", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1817070/header.jpg"},
        {"isim": "Horizon Zero Dawn", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1151640/header.jpg"},
        {"isim": "The Last of Us Part I", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1888930/header.jpg"},
        {"isim": "Ghost of Tsushima", "resim": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2215430/header.jpg"}
    ]
}

with app.app_context():
    # Eski sorunlu filmler oyununu sil
    eski_oyun = Oyun.query.filter_by(baslik='Sinema Gurmeleri: Yönetmenini Bul (Casus Kim)').first()
    if eski_oyun:
        Soru.query.filter_by(oyun_id=eski_oyun.id).delete()
        db.session.delete(eski_oyun)
        db.session.commit()

    # Yeni oyun
    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Oyun Gurmeleri: Farklı Stüdyoyu Bul (Casus Kim)',
        aciklama='4 efsanevi oyundan 3 tanesi aynı stüdyoya (ör. Rockstar, Valve) ait. Aralarına sızan CASUS stüdyonun oyununu saniyeler içinde bulabilir misin?',
        resim_url='https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/271590/header.jpg', # GTA V
        kategori='Eğlence',
        oyun_modu='casus_kim',
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    # Tam 25 soru üret (Rastgele kombinasyonlar)
    studyo_listesi = list(studyolar.keys())
    
    for i in range(25):
        # 2 farklı stüdyo seç
        ana_studyo, casus_studyo = random.sample(studyo_listesi, 2)
        
        # Ana stüdyodan rastgele 3 oyun seç
        ana_oyunlar = random.sample(studyolar[ana_studyo], 3)
        
        # Casus stüdyodan rastgele 1 oyun seç
        casus_oyun = random.sample(studyolar[casus_studyo], 1)[0]
        
        # Hepsini karıştır
        havuz = ana_oyunlar + [casus_oyun]
        random.shuffle(havuz)
        
        secenekler = [f["isim"] for f in havuz]
        resimler = [f["resim"] for f in havuz]
        dogru_cevap = casus_oyun["isim"]
        
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=','.join(resimler),
            secenekler=','.join(secenekler),
            dogru_cevap=dogru_cevap
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print("✅ Casus Kim: Oyun Gurmeleri başarıyla eklendi!")
