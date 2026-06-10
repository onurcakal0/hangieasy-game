from app import app, db, Oyun, Kullanici

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Guess the Turkey City').first()
    if eski_oyun:
        db.session.delete(eski_oyun)
        db.session.commit()

    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Guess the Turkey City',
        aciklama='Türkiye coğrafyasına ne kadar hakimsin? 10 dakika içinde 81 ilin tamamını bulabilecek misin? Klavyene ve zekana güveniyorsan hemen başla!',
        resim_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Turkey_provinces_blank_numbered.svg/1024px-Turkey_provinces_blank_numbered.svg.png', 
        kategori='Özel Oyunlar', 
        oyun_modu='harita_tr',
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()
    
    print("✅ Guess the Turkey City başarıyla eklendi!")
