import urllib.parse
from app import app, db, Oyun, Soru, Kullanici

# Soru verileri: (Soru Metni, Seçenekler (virgülle ayrılmış), Doğru Cevap)
soru_verileri = [
    ("Hangi gezegen Gunes\nSistemi'ndeki en\nbuyuk gezegendir?", "Jupiter,Saturn,Uranus,Neptun", "Jupiter"),
    ("'Mona Lisa' tablosu\nhangi unlu ressama aittir?", "Van Gogh,Da Vinci,Picasso,Monet", "Da Vinci"),
    ("Dunya'nin en uzun\nnehri hangisidir?", "Amazon,Nil,Yangtze,Mississippi", "Nil"),
    ("Hangi elementin kimyasal\nsembolu 'O' harfidir?", "Oksijen,Altin,Karbon,Demir", "Oksijen"),
    ("Insan vucudundaki en\nbuyuk organ hangisidir?", "Kalp,Karaciger,Deri,Akciger", "Deri"),
    ("Turkiye Cumhuriyeti hangi\nyil kurulmustur?", "1920,1923,1919,1924", "1923"),
    ("'Sefiller' adli unlu\nromanin yazari kimdir?", "Victor Hugo,Dickens,Tolstoy,Dostoevsky", "Victor Hugo"),
    ("Hangi kita dunyanin\nen soguk kitasidir?", "Asya,Avrupa,Antarktika,Kuzey Amerika", "Antarktika"),
    ("Telefonu icat eden\nkisi kimdir?", "Thomas Edison,Graham Bell,Nikola Tesla,Marconi", "Graham Bell"),
    ("Istanbul'un fethi hangi\npadisah doneminde gerceklesti?", "Yavuz Sultan Selim,Fatih Sultan Mehmet,Kanuni,II. Abdulhamit", "Fatih Sultan Mehmet"),
    ("Hangi okyanus dunyanin\nen buyuk okyanusudur?", "Atlas,Hint,Pasifik,Arktik", "Pasifik"),
    ("DNA'nin acilimi\nnedir?", "Deoksiribonukleik Asit,Dioksinukleik Asit,Dinamik Asit,Deoksin Asit", "Deoksiribonukleik Asit"),
    ("'Romeo ve Juliet'\neserinin yazari kimdir?", "Shakespeare,Jane Austen,Mark Twain,Dickens", "Shakespeare"),
    ("Hangi ulke 'Dogan\nGunesin Ulkesi' olarak bilinir?", "Cin,Guney Kore,Japonya,Tayland", "Japonya"),
    ("Bir gun tam\nolarak kac dakikadir?", "1440,1200,3600,2400", "1440"),
    ("Hangi hayvan memelidir\nancak ucar?", "Kartal,Yarasa,Penguen,Devekusu", "Yarasa"),
    ("Ilk Nobel odulunu\nkazanan kadin kimdir?", "Rosalind Franklin,Marie Curie,Ada Lovelace,Jane Goodall", "Marie Curie"),
    ("Hangi renk ana renklerden\nbiri degildir?", "Kirmizi,Mavi,Sari,Yesil", "Yesil"),
    ("Olimpiyat oyunlari ilk\nkez nerede duzenlenmistir?", "Italya,Yunanistan,Fransa,Misir", "Yunanistan"),
    ("Matbaayi kim\nicat etmistir?", "Gutenberg,Galileo,Isaac Newton,Einstein", "Gutenberg")
]

def get_question_image(text):
    # Kullanıcı test modunda soruyu görselin içine yazdığı için,
    # fakeimg.pl ile dinamik olarak soruyu resme basıyoruz.
    safe_text = urllib.parse.quote(text)
    return f"https://fakeimg.pl/800x400/1e1e24/00f2fe/?text={safe_text}&font_size=55"

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Zorlu Genel Kültür Maratonu').first()
    if eski_oyun:
        Soru.query.filter_by(oyun_id=eski_oyun.id).delete()
        db.session.delete(eski_oyun)
        db.session.commit()

    # Admin kullanıcıyı bul
    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Zorlu Genel Kültür Maratonu',
        aciklama='Tarihten bilime, coğrafyadan sanata uzanan klasikleşmiş 20 soruluk genel kültür testi. Gerçek bilgi seviyeni ölçmeye hazır mısın?',
        resim_url='https://fakeimg.pl/800x400/1e1e24/f39c12/?text=Genel+Kultur+Maratonu',
        kategori='Genel Kültür',
        oyun_modu='normal',  # KLASIK TEST
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    # Soruları ekle
    for index, (soru_metni, secenekler, dogru) in enumerate(soru_verileri):
        img_url = get_question_image(f"Soru {index+1}:\n{soru_metni}")
        
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=img_url,
            secenekler=secenekler,
            dogru_cevap=dogru
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print("✅ Genel Kültür testi (20 soru) başarıyla eklendi!")
