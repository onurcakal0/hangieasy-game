from app import app, db, Oyun, Soru, Kullanici

f1_sorulari = [
    {
        "soru": "Tarihte en fazla Formula 1 Dünya Şampiyonluğu (7 kez) kazanan pilotlar kimlerdir?",
        "secenekler": ["Michael Schumacher ve Lewis Hamilton", "Ayrton Senna ve Alain Prost", "Sebastian Vettel ve Fernando Alonso", "Max Verstappen ve Niki Lauda"],
        "dogru": "Michael Schumacher ve Lewis Hamilton"
    },
    {
        "soru": "Bir sezonda en çok yarış kazanma rekoruna sahip olan (19 galibiyet) Formula 1 pilotu kimdir?",
        "secenekler": ["Max Verstappen", "Lewis Hamilton", "Michael Schumacher", "Ayrton Senna"],
        "dogru": "Max Verstappen"
    },
    {
        "soru": "Formula 1 tarihinde en fazla Grand Prix'ye katılan (400'e yaklaşan) 'Emektar' pilot kimdir?",
        "secenekler": ["Fernando Alonso", "Kimi Räikkönen", "Rubens Barrichello", "Lewis Hamilton"],
        "dogru": "Fernando Alonso"
    },
    {
        "soru": "Scuderia Ferrari takımının ikonik rengi ve logosundaki efsanevi sembol nedir?",
        "secenekler": ["Kırmızı - Şahlanan At", "Gümüş - Üç Köşeli Yıldız", "Mavi - Boğa", "Sarı - Kalkan"],
        "dogru": "Kırmızı - Şahlanan At"
    },
    {
        "soru": "Hangi efsanevi Brezilyalı F1 pilotu, 1994 Imola (San Marino) Grand Prix'sindeki kazada hayatını kaybetmiştir?",
        "secenekler": ["Ayrton Senna", "Nelson Piquet", "Emerson Fittipaldi", "Rubens Barrichello"],
        "dogru": "Ayrton Senna"
    },
    {
        "soru": "Formula 1 takvimine eklenen ve tarihinde tamamen 'Gece Yarışı' olarak koşulan ilk Grand Prix hangisidir?",
        "secenekler": ["Singapur Grand Prix", "Bahreyn Grand Prix", "Abu Dabi Grand Prix", "Las Vegas Grand Prix"],
        "dogru": "Singapur Grand Prix"
    },
    {
        "soru": "Monako GP, Indy 500 ve Le Mans 24 Saat yarışlarını kazanarak tarihte 'Triple Crown' unvanını alan TEK pilot kimdir?",
        "secenekler": ["Graham Hill", "Fernando Alonso", "Juan Pablo Montoya", "Jackie Stewart"],
        "dogru": "Graham Hill"
    },
    {
        "soru": "Sadece 18 yaşındayken İspanya Grand Prix'sini kazanarak F1 tarihinin 'En Genç Yarış Kazanan Pilotu' olan isim kimdir?",
        "secenekler": ["Max Verstappen", "Sebastian Vettel", "Charles Leclerc", "Lando Norris"],
        "dogru": "Max Verstappen"
    },
    {
        "soru": "V6 Turbo Hibrit çağına damga vurup, 2014-2021 yılları arasında üst üste 8 kez Takımlar Şampiyonu olan takım hangisidir?",
        "secenekler": ["Mercedes", "Red Bull Racing", "Ferrari", "McLaren"],
        "dogru": "Mercedes"
    },
    {
        "soru": "Formula 1 araçlarındaki DRS (Drag Reduction System) sisteminin temel amacı nedir?",
        "secenekler": ["Arka kanadı açıp hava direncini azaltarak hızı artırmak", "Fren mesafesini kısaltmak", "Motoru soğutmak", "Yakıt tasarrufu sağlamak"],
        "dogru": "Arka kanadı açıp hava direncini azaltarak hızı artırmak"
    },
    {
        "soru": "Uzun düzlükleri nedeniyle dünya çapında 'Hız Tapınağı' (Temple of Speed) olarak bilinen ikonik pist hangisidir?",
        "secenekler": ["Monza (İtalya)", "Spa-Francorchamps (Belçika)", "Silverstone (İngiltere)", "Suzuka (Japonya)"],
        "dogru": "Monza (İtalya)"
    },
    {
        "soru": "Pilotların kafasını koruyan ve 2018 yılında tartışmalarla birlikte zorunlu hale getirilen güvenlik aparatının adı nedir?",
        "secenekler": ["Halo", "Aeroscreen", "Roll Hoop", "HANS Cihazı"],
        "dogru": "Halo"
    },
    {
        "soru": "Modern bir Formula 1 aracının 0'dan 100 km/s hıza ulaşması ortalama ne kadar sürer?",
        "secenekler": ["Yaklaşık 2.5 saniye", "Yaklaşık 3.5 saniye", "Yaklaşık 1.5 saniye", "Yaklaşık 4 saniye"],
        "dogru": "Yaklaşık 2.5 saniye"
    },
    {
        "soru": "F1 tarihinde en fazla yarışa ilk sıradan (Pole Pozisyonu) başlayan ve 100 barajını geçen ilk pilot kimdir?",
        "secenekler": ["Lewis Hamilton", "Ayrton Senna", "Michael Schumacher", "Sebastian Vettel"],
        "dogru": "Lewis Hamilton"
    },
    {
        "soru": "Bir yarış hafta sonunda En Hızlı Turu (Fastest Lap) atıp yarışı ilk 10'da bitiren pilota kaç ekstra puan verilir?",
        "secenekler": ["1 Puan", "2 Puan", "5 Puan", "Ekstra puan verilmez"],
        "dogru": "1 Puan"
    }
]

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Formula 1 Dehası mısın?').first()
    if eski_oyun:
        Soru.query.filter_by(oyun_id=eski_oyun.id).delete()
        db.session.delete(eski_oyun)
        db.session.commit()

    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Formula 1 Dehası mısın?',
        aciklama='Hız, aerodinamik, efsane pilotlar ve taktikler... Formula 1 tarihi ve kuralları hakkında 15 zorlu soru seni bekliyor. Pit stop yapmadan hepsini bilebilir misin?',
        resim_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/F1_car.svg/512px-F1_car.svg.png', 
        kategori='Spor', 
        oyun_modu='klasik_test',
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    for item in f1_sorulari:
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=item["soru"], # klasik_test modunda soru metnini buraya sakliyoruz
            secenekler=','.join(item["secenekler"]),
            dogru_cevap=item["dogru"]
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print("✅ Formula 1 Testi başarıyla eklendi!")
