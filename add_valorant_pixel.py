import urllib.request
import json
import random
import ssl
from app import app, db, Oyun, Soru, Kullanici

# Fetch Valorant Agents
url = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with urllib.request.urlopen(req, context=ctx) as response:
    data = json.loads(response.read().decode())

agents = data['data']
agent_names = [a['displayName'] for a in agents]

with app.app_context():
    # Eski oyunu sil (varsa)
    eski_oyun = Oyun.query.filter_by(baslik='Valorant Ajanları: Piksel Avcısı').first()
    if eski_oyun:
        Soru.query.filter_by(oyun_id=eski_oyun.id).delete()
        db.session.delete(eski_oyun)
        db.session.commit()

    user = Kullanici.query.filter_by(kullanici_adi='onur').first()
    if not user:
        user = Kullanici.query.first()
        
    yeni_oyun = Oyun(
        baslik='Valorant Ajanları: Piksel Avcısı',
        aciklama='Bulanıklaştırılmış fotoğraftaki Valorant ajanını 10 saniye içinde tahmin edebilir misin? Netleşmesini bekle ama puanın düşer!',
        resim_url='https://media.valorant-api.com/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/fullportrait.png', # Jett
        kategori='Spor',
        oyun_modu='piksel_avcisi',
        olusturan_id=user.id if user else None
    )
    db.session.add(yeni_oyun)
    db.session.commit()

    for agent in agents:
        isim = agent['displayName']
        # Full portrait piksel avcisi icin daha gorsel durur.
        resim = agent.get('fullPortrait') or agent.get('displayIcon')
        
        # 3 yanlis secenek bul
        yanlislar = random.sample([n for n in agent_names if n != isim], 3)
        secenekler = [isim] + yanlislar
        random.shuffle(secenekler)
        
        yeni_soru = Soru(
            oyun_id=yeni_oyun.id,
            resim_url=resim,
            secenekler=','.join(secenekler),
            dogru_cevap=isim
        )
        db.session.add(yeni_soru)
    
    db.session.commit()
    print(f"✅ Valorant Piksel Avcısı başarıyla eklendi! Toplam {len(agents)} ajan eklendi.")
