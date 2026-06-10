from app import app, db, Oyun

with app.app_context():
    oyun = Oyun.query.filter_by(baslik='Formula 1 Dehası mısın?').first()
    if oyun:
        oyun.resim_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2488620/header.jpg'
        db.session.commit()
        print("✅ Oyun resmi güncellendi!")
    else:
        print("❌ Oyun bulunamadı!")
