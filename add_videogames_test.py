from app import app, db, Oyun, Soru, Kullanici

# Steam ve Wiki resim linkleri
pairs = [
    {
        "isimler": "The Witcher 3: Wild Hunt,Red Dead Redemption 2",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/292030/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1174180/header.jpg"
    },
    {
        "isimler": "PlayStation 5,Xbox Series X",
        "resimler": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/PlayStation_5_and_DualSense_with_disc_drive.jpg/640px-PlayStation_5_and_DualSense_with_disc_drive.jpg,https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Xbox_Series_X_Black.jpg/640px-Xbox_Series_X_Black.jpg"
    },
    {
        "isimler": "God of War,Halo",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1593500/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/976730/header.jpg"
    },
    {
        "isimler": "Grand Theft Auto V,Cyberpunk 2077",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/271590/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1091500/header.jpg"
    },
    {
        "isimler": "Minecraft,Terraria",
        "resimler": "https://upload.wikimedia.org/wikipedia/en/5/51/Minecraft_cover.png,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/105600/header.jpg"
    },
    {
        "isimler": "Valorant,Counter-Strike 2",
        "resimler": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Valorant_logo_-_pink_color_version.svg/640px-Valorant_logo_-_pink_color_version.svg.png,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/730/header.jpg"
    },
    {
        "isimler": "League of Legends,Dota 2",
        "resimler": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/League_of_Legends_2019_vector.svg/640px-League_of_Legends_2019_vector.svg.png,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/570/header.jpg"
    },
    {
        "isimler": "Super Mario,The Legend of Zelda",
        "resimler": "https://upload.wikimedia.org/wikipedia/en/a/a9/Mario_Nintendo.png,https://upload.wikimedia.org/wikipedia/en/2/21/The_Legend_of_Zelda_logo.png"
    },
    {
        "isimler": "Dark Souls,Bloodborne",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/211420/header.jpg,https://upload.wikimedia.org/wikipedia/en/6/68/Bloodborne_Cover_Wallpaper.jpg"
    },
    {
        "isimler": "Doom Eternal,Half-Life 2",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/782330/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/220/header.jpg"
    },
    {
        "isimler": "The Last of Us,The Walking Dead",
        "resimler": "https://upload.wikimedia.org/wikipedia/en/4/46/Video_Game_Cover_-_The_Last_of_Us.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/207610/header.jpg"
    },
    {
        "isimler": "Resident Evil 4,Silent Hill 2",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2050650/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2124490/header.jpg"
    },
    {
        "isimler": "Fallout: New Vegas,The Elder Scrolls V: Skyrim",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/22380/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/489830/header.jpg"
    },
    {
        "isimler": "Steam,Epic Games Store",
        "resimler": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/640px-Steam_icon_logo.svg.png,https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/640px-Epic_Games_logo.svg.png"
    },
    {
        "isimler": "Elden Ring,Sekiro: Shadows Die Twice",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/814380/header.jpg"
    },
    {
        "isimler": "Hades,Hollow Knight",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1145360/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/367520/header.jpg"
    },
    {
        "isimler": "Fortnite,Apex Legends",
        "resimler": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/FortniteLogo.svg/640px-FortniteLogo.svg.png,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1172470/header.jpg"
    },
    {
        "isimler": "Assassin's Creed,Ghost of Tsushima",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/15108/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2215430/header.jpg"
    },
    {
        "isimler": "Mortal Kombat 1,Street Fighter 6",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1971870/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1364780/header.jpg"
    },
    {
        "isimler": "Diablo IV,Path of Exile",
        "resimler": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2344520/header.jpg,https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/238960/header.jpg"
    }
]

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Büyük Çarpışma: Oyun Dünyası (O mu Bu mu?)').first()
    if eski_oyun:
        Soru.query.filter_by(oyun_id=eski_oyun.id).delete()
        db.session.delete(eski_oyun)
        db.session.commit()
        print("Eski oyun silindi.")

    # Admin kullanıcıyı bul
    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Büyük Çarpışma: Oyun Dünyası (O mu Bu mu?)',
        aciklama='Tüm zamanların en büyük oyunlarını, efsanevi karakterlerini ve konsollarını kıyaslıyoruz! Gerçek bir oyuncu olarak tarafını seç. Orijinal oyun görselleriyle tam 20 zorlu seçim seni bekliyor!',
        resim_url='https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/292030/header.jpg',
        kategori='Oyun',
        oyun_modu='omu_bumu',
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    # Soruları ekle
    for p in pairs:
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=p["resimler"],
            secenekler=p["isimler"],
            dogru_cevap="Farketmez"
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print("✅ Video Oyunları testi (Gerçek görsellerle 20 soru) başarıyla eklendi!")
