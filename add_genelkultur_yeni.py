from app import app, db, Oyun, Soru, Kullanici

# Soru verileri: (Soru Metni, Seçenekler, Doğru Cevap)
soru_verileri = [
    ("Hangi gezegen Güneş Sistemi'ndeki en büyük gezegendir?", "Jüpiter,Satürn,Uranüs,Neptün", "Jüpiter"),
    ("'Mona Lisa' tablosu hangi ünlü ressama aittir?", "Vincent van Gogh,Leonardo da Vinci,Pablo Picasso,Claude Monet", "Leonardo da Vinci"),
    ("Dünya'nın en uzun nehri hangisidir?", "Amazon Nehri,Nil Nehri,Yangtze Nehri,Mississippi Nehri", "Nil Nehri"),
    ("Hangi elementin kimyasal sembolü 'O' harfidir?", "Oksijen,Altın,Karbon,Demir", "Oksijen"),
    ("İnsan vücudundaki en büyük organ hangisidir?", "Kalp,Karaciğer,Deri,Akciğer", "Deri"),
    ("Türkiye Cumhuriyeti hangi yıl kurulmuştur?", "1920,1923,1919,1924", "1923"),
    ("'Sefiller' adlı ünlü romanın yazarı kimdir?", "Victor Hugo,Charles Dickens,Leo Tolstoy,Fyodor Dostoevsky", "Victor Hugo"),
    ("Hangi kıta dünyanın en soğuk kıtasıdır?", "Asya,Avrupa,Antarktika,Kuzey Amerika", "Antarktika"),
    ("Telefonu icat eden kişi kimdir?", "Thomas Edison,Alexander Graham Bell,Nikola Tesla,Guglielmo Marconi", "Alexander Graham Bell"),
    ("İstanbul'un fethi hangi padişah döneminde gerçekleşmiştir?", "Yavuz Sultan Selim,Fatih Sultan Mehmet,Kanuni Sultan Süleyman,II. Abdülhamit", "Fatih Sultan Mehmet"),
    ("Hangi okyanus dünyanın en büyük okyanusudur?", "Atlas Okyanusu,Hint Okyanusu,Pasifik Okyanusu,Arktik Okyanusu", "Pasifik Okyanusu"),
    ("DNA'nın açılımı nedir?", "Deoksiribonükleik Asit,Dioksinükleik Asit,Dinamik Nükleik Asit,Deoksin Asit", "Deoksiribonükleik Asit"),
    ("'Romeo ve Juliet' adlı eserin yazarı kimdir?", "William Shakespeare,Jane Austen,Mark Twain,Charles Dickens", "William Shakespeare"),
    ("Hangi ülke 'Doğan Güneşin Ülkesi' olarak bilinir?", "Çin,Güney Kore,Japonya,Tayland", "Japonya"),
    ("Bir gün tam olarak kaç dakikadır?", "1440,1200,3600,2400", "1440"),
    ("Hangi hayvan memelidir ancak uçar?", "Kartal,Yarasa,Penguen,Devekuşu", "Yarasa"),
    ("İlk Nobel ödülünü kazanan kadın bilim insanı kimdir?", "Rosalind Franklin,Marie Curie,Ada Lovelace,Jane Goodall", "Marie Curie"),
    ("Hangi renk ışığın ana renklerinden biri değildir?", "Kırmızı,Mavi,Sarı,Yeşil", "Sarı"),
    ("Olimpiyat oyunları ilk kez hangi ülkede düzenlenmiştir?", "İtalya,Yunanistan,Fransa,Mısır", "Yunanistan"),
    ("Matbaayı kim icat etmiştir?", "Johannes Gutenberg,Galileo Galilei,Isaac Newton,Albert Einstein", "Johannes Gutenberg")
]

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Zorlu Genel Kültür Maratonu').first()
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
        baslik='Zorlu Genel Kültür Maratonu',
        aciklama='Tarihten bilime, coğrafyadan sanata uzanan klasikleşmiş 20 soruluk genel kültür testi. Artık yepyeni, resimsiz ve saf zeka odaklı "Klasik Test" modunda!',
        resim_url='https://fakeimg.pl/800x400/1e1e24/f39c12/?text=Genel+Kultur+Maratonu',
        kategori='Genel Kültür',
        oyun_modu='klasik_test', # YENI MOD!
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    # Soruları ekle
    for soru_metni, secenekler, dogru in soru_verileri:
        # Klasik Test modunda 'resim_url' alanına direkt soru metnini yazıyoruz!
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=soru_metni,
            secenekler=secenekler,
            dogru_cevap=dogru
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print("✅ Yeni 'Klasik Test' modunda Genel Kültür testi (20 soru) başarıyla eklendi!")
