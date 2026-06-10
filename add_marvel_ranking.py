import urllib.parse
from app import app, db, Oyun, Soru, Kullanici

# TMDB (The Movie Database) afiş linkleri - Hotlink'e izin verir, asla engellenmez!
marvel_filmleri = [
    {
        "isim": "Iron Man (2008)",
        "resim": "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg"
    },
    {
        "isim": "The Avengers (2012)",
        "resim": "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmja8y.jpg"
    },
    {
        "isim": "Captain America: The Winter Soldier",
        "resim": "https://image.tmdb.org/t/p/w500/tVFRpFw3xTedgPGqxW0AOI8Qhh0.jpg"
    },
    {
        "isim": "Guardians of the Galaxy (2014)",
        "resim": "https://image.tmdb.org/t/p/w500/r7vmZjiyZw9rpJMQJmLzVtnixc5.jpg"
    },
    {
        "isim": "Captain America: Civil War",
        "resim": "https://image.tmdb.org/t/p/w500/rAGiXaUfPzY7C1iGIlKKp8pPQZ.jpg"
    },
    {
        "isim": "Thor: Ragnarok (2017)",
        "resim": "https://image.tmdb.org/t/p/w500/rzRwTcFvttce1VKwBWHlTvB81i.jpg"
    },
    {
        "isim": "Black Panther (2018)",
        "resim": "https://image.tmdb.org/t/p/w500/uxzzxijgPIY7slzFvMotPv8wjKA.jpg"
    },
    {
        "isim": "Avengers: Infinity War (2018)",
        "resim": "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg"
    },
    {
        "isim": "Avengers: Endgame (2019)",
        "resim": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
    },
    {
        "isim": "Spider-Man: No Way Home",
        "resim": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1ZrsPtA3g3N3.jpg"
    },
    {
        "isim": "Doctor Strange: Multiverse of Madness",
        "resim": "https://image.tmdb.org/t/p/w500/9Gtg2DzBhmYamXBS1hKAhiwbBKS.jpg"
    },
    {
        "isim": "Spider-Man: Into the Spider-Verse",
        "resim": "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg"
    },
    {
        "isim": "Deadpool & Wolverine (2024)",
        "resim": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg"
    },
    {
        "isim": "Logan (2017)",
        "resim": "https://image.tmdb.org/t/p/w500/fnbjcRDYn6YviCcePDnGdyAkYsB.jpg"
    },
    {
        "isim": "Deadpool (2016)",
        "resim": "https://image.tmdb.org/t/p/w500/zq8Cl3PNIDGU3pzWXVbQeXf93m.jpg"
    }
]

with app.app_context():
    # Eski oyunu bul ve resmini/sorularını güncelle
    oyun = Oyun.query.filter_by(baslik='Marvel Sinematik Evreni: Kör Sıralama').first()
    
    if oyun:
        # Steam CDN üzerinden Marvel kapak resmi (Çok güvenilir)
        oyun.resim_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/997070/header.jpg'
        
        # Eski Wikipedia resimli soruları sil
        Soru.query.filter_by(oyun_id=oyun.id).delete()
        db.session.commit()
        
        # Yeni TMDB resimli soruları ekle
        for film in marvel_filmleri:
            yeni_soru = Soru(
                oyun_id=oyun.id,
                resim_url=film["resim"],
                secenekler=film["isim"],
                dogru_cevap="Farketmez"
            )
            db.session.add(yeni_soru)
        
        db.session.commit()
        print("✅ Marvel Kör Sıralama testi resimleri TMDB ve Steam CDN ile güncellendi!")
    else:
        print("Oyun bulunamadı, scripti kontrol et.")
