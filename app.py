import os
import time
import uuid
import random
import string
import threading
from datetime import date

# --- FLASK VE EKLENTİLER ---
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit, join_room

# --- GÜVENLİK VE ARAÇLAR ---
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from datetime import datetime

# --- DIŞ SERVİSLER ---
from supabase import create_client, Client
import stripe

# 🛡️ 1. GİZLİ KASAYI AÇ (.env dosyasını okur)
load_dotenv()

# 🚀 2. MOTORU ÇALIŞTIR
app = Flask(__name__)

# --- 🔐 GÜVENLİK VE UYGULAMA AYARLARI ---
# İki farklı secret key vardı, onları kasadan çekip tek bir mühürde birleştirdik.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.secret_key = app.config['SECRET_KEY']
# --- 📧 HANGIEASY POSTACI (MAIL) AYARLARI ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465             # 587'yi çöpe attık, 465 SSL portuna geçtik!
app.config['MAIL_USE_TLS'] = False        # TLS'i kapattık
app.config['MAIL_USE_SSL'] = True         # Zırhlı SSL bağlantısını aktif ettik!
app.config['MAIL_USERNAME'] = 'hangieasy@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('HangiEasy Merkez', 'hangieasy@gmail.com')
# --- 💾 YEREL VERİTABANI (SQLITE) VE KLASÖR AYARLARI ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'ogg'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 🚀 3. EKLENTİLERİ MOTORA BAĞLA

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
socketio = SocketIO(app, cors_allowed_origins="*")

# --- 🥷 4. SUPABASE BULUT DEPOLAMA AYARLARI ---
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 💳 5. STRIPE GLOBAL ÖDEME ALTYAPISI ---
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# --- BUNDAN SONRASI SENİN MODELLERİNLE (class Kullanici) DEVAM EDİYOR ---
db = SQLAlchemy(app)

# --- MODELLER ---
# --- MODELLER ---
takipciler = db.Table('takipciler',
    db.Column('takip_eden_id', db.Integer, db.ForeignKey('kullanici.id')),
    db.Column('takip_edilen_id', db.Integer, db.ForeignKey('kullanici.id'))
)

class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # --- 🔒 TEMEL KİMLİK BİLGİLERİ (BUNLAR EKSİKTİ, EKLENDİ) ---
    ad_soyad = db.Column(db.String(100), nullable=False)
    kullanici_adi = db.Column(db.String(50), unique=True, nullable=False)
    eposta = db.Column(db.String(120), unique=True, nullable=False)
    dogum_tarihi = db.Column(db.String(20), nullable=False)
    sifre_hash = db.Column(db.String(255), nullable=False) # Postgres için sınırı 255 yaptık
    onayli_mi = db.Column(db.Boolean, default=False) # E-posta onayı için şart!
    profil_resmi = db.Column(db.String(300), nullable=True)
    # --- 💰 EKONOMİ VE OYUN SİSTEMİ ---
    he_coin = db.Column(db.Integer, default=50) 
    oyunlar = db.relationship('Oyun', backref='olusturan', lazy=True)
    
    # --- 🚀 YENİ EKLENEN VİZYONER ÖZELLİKLER ---
    rutbe = db.Column(db.String(50), default="Stajyer") # Rütbe Sistemi (Stajyer, Müdür, CEO)
    referans_kodu = db.Column(db.String(10), unique=True) # Referans Sistemi (Arkadaşını getir)
    cozulen_test_sayisi = db.Column(db.Integer, default=0) # Görevler ve Rütbe atlamak için sayaç
    profil_cercevesi = db.Column(db.String(50), default="standart") # Mağazadan alınacak kozmetikler
    son_gorev_tarihi = db.Column(db.String(20), default="")
    gunluk_test_sayaci = db.Column(db.Integer, default=0)
    gunluk_odul_alindi = db.Column(db.Boolean, default=False)
    boss_bileti_alindi = db.Column(db.Boolean, default=False)  # Boss Arenası bilet kontrolü

    takip_ettikleri = db.relationship(
        'Kullanici', secondary=takipciler,
        primaryjoin=(takipciler.c.takip_eden_id == id),
        secondaryjoin=(takipciler.c.takip_edilen_id == id),
        backref=db.backref('takipcileri', lazy='dynamic'), lazy='dynamic')
    
    bildirimler = db.relationship('Bildirim', backref='kullanici', lazy=True)
    
    # --- MAĞAZA ENVANTERİ ---
    sahip_olunan_cerceveler = db.Column(db.Text, default="") # Örn: "siber_komuta,cehennem_atesi"
    sahip_olunan_unvanlar = db.Column(db.Text, default="") # Örn: "siber_korsan,ceo"
class Oyun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.String(200))
    resim_url = db.Column(db.String(300))
    kategori = db.Column(db.String(50))
    oyun_modu = db.Column(db.String(50), nullable=False, default='normal') 
    olusturan_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'))
    sorular = db.relationship('Soru', backref='oyun', lazy=True)
    oynanma_sayisi = db.Column(db.Integer, default=0)
    bitirilme_sayisi = db.Column(db.Integer, default=0)

class Soru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_id = db.Column(db.Integer, db.ForeignKey('oyun.id'), nullable=False)
    resim_url = db.Column(db.String(500)) 
    resim_url_2 = db.Column(db.String(300), nullable=True) 
    secenekler = db.Column(db.String(500))
    dogru_cevap = db.Column(db.String(100))

class Istatistik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_id = db.Column(db.Integer, db.ForeignKey('oyun.id'), nullable=False)
    secenek_ismi = db.Column(db.String(100), nullable=False)
    sampiyonluk_sayisi = db.Column(db.Integer, default=1)

class Bildirim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    mesaj = db.Column(db.String(255), nullable=False)
    okundu = db.Column(db.Boolean, default=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

    
# Veritabanını kuran kodun (Burası doğru, kalsın)
with app.app_context():
    db.create_all()

    # --- GÜVENLİ MIGRATION: Eksik kolonları PostgreSQL'e ekle ---
    # db.create_all() mevcut tablolara yeni kolon EKLEMEZ.
    # Bu blok her deploy'da çalışır, IF NOT EXISTS sayesinde güvenlidir.
    from sqlalchemy import text
    migrasyonlar = [
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS boss_bileti_alindi BOOLEAN DEFAULT FALSE",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS onayli_mi BOOLEAN DEFAULT FALSE",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS profil_resmi VARCHAR(300)",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS rutbe VARCHAR(50) DEFAULT 'Stajyer'",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS referans_kodu VARCHAR(10)",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS cozulen_test_sayisi INTEGER DEFAULT 0",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS profil_cercevesi VARCHAR(50) DEFAULT 'standart'",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS son_gorev_tarihi VARCHAR(20) DEFAULT ''",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS gunluk_test_sayaci INTEGER DEFAULT 0",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS gunluk_odul_alindi BOOLEAN DEFAULT FALSE",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS sahip_olunan_cerceveler TEXT DEFAULT ''",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS sahip_olunan_unvanlar TEXT DEFAULT ''"
    ]
    with db.engine.connect() as conn:
        for sql in migrasyonlar:
            try:
                conn.execute(text(sql))
            except Exception as mig_err:
                print(f"Migration atlandı (zaten var): {mig_err}")
        conn.commit()
    print("✅ Migration tamamlandı.")

# --- GLOBAL VERİLER ---
SOZLUK = {
    'tr': {
        'yeni_test': '+ Test Oluştur', 'studyo': '👤 Stüdyom', 'cikis': 'Çıkış Yap',
        'giris': 'Giriş Yap', 'kayit': 'Kayıt Ol', 'oyna': 'Testi Çöz'
    },
    'en': {
        'yeni_test': '+ Create Quiz', 'studyo': '👤 My Studio', 'cikis': 'Logout',
        'giris': 'Login', 'kayit': 'Sign Up', 'oyna': 'Play Now'
    }
}

@app.context_processor
def inject_global_data():
    aktif_dil = session.get('dil', 'tr')
    bakiye = 0
    if 'kullanici_adi' in session and not session['kullanici_adi'].startswith('Misafir_'):
        kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
        if kullanici:
            bakiye = kullanici.he_coin
    return dict(aktif_dil=aktif_dil, t=SOZLUK[aktif_dil], bakiye=bakiye)

# --- 💰 EKONOMİ & 🚀 RÜTBE & GÖREV YAPAY ZEKASI ---
# --- 💰 EKONOMİ YAPAY ZEKASI ---
# --- 💰 EKONOMİ YAPAY ZEKASI ---
@app.route('/api/odul_al', methods=['POST'])
def odul_al():
    # Adam misafirse veya giriş yapmamışsa 0 coin ver, çökme!
    if 'kullanici_adi' not in session or session['kullanici_adi'].startswith('Misafir_'): 
        return jsonify({"status": "error", "kazanc": 0, "yeni_bakiye": 0}), 401
    
    # JSON bozuk gelirse diye güvenlik önlemi
    data = request.json or {}
    kazanc = data.get('miktar', 20) # Oyun bittiğinde gelen para
    
    # 🚀 CTO MOTORU DEVREDE! (Fişi prize taktık)
    # Bu fonksiyon hem parayı ekler, hem sayacı artırır, hem de rütbeyi günceller!
    motor_calisti_mi = ilerleme_kaydet(session['kullanici_adi'], kazanilan_puan=kazanc)
    
    if motor_calisti_mi:
        # Motordan sonra en güncel bakiyeyi ekrana yansıtmak için kasaya son bir kez bakıyoruz
        kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
        return jsonify({"status": "success", "kazanc": kazanc, "yeni_bakiye": kullanici.he_coin})
        
    return jsonify({"status": "error", "kazanc": 0}), 400
@app.route('/api/gorev_odulu_al', methods=['POST'])
def gorev_odulu_al():
    kadi = session.get('kullanici_adi')
    kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    
    if kullanici.gunluk_test_sayaci >= 3 and not kullanici.gunluk_odul_alindi:
        kullanici.he_coin += 100 # Görev Başarılı! 100 Coin ateşle.
        kullanici.gunluk_odul_alindi = True
        db.session.commit()
        return jsonify({"status": "success", "yeni_bakiye": kullanici.he_coin})
        
    return jsonify({"status": "error"})

@app.route('/profil')
def profil():
    kadi = session.get('kullanici_adi')
    if not kadi or kadi.startswith('Misafir_'): 
        return redirect(url_for('giris'))
        
    aktif = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    
    if aktif is None:
        session.clear() 
        return redirect(url_for('giris'))

    # 🚀 CTO OTO-TAMİR SİSTEMİ (Self-Healing)
    # Eğer adamın kodu None ise, ona hemen fiyakalı bir şirket kodu üret!
    if not aktif.referans_kodu:
        # Kullanıcı adının ilk 3 harfini alıp büyüt, yanına 4 haneli şifre ekle. (Örn: ONU5829)
        isim_kismi = aktif.kullanici_adi[:3].upper()
        # Eğer kullanıcı adı 3 harften kısaysa yanına X ekle
        if len(isim_kismi) < 3:
            isim_kismi = isim_kismi.ljust(3, 'X')
            
        rastgele_sayi = str(random.randint(1000, 9999))
        aktif.referans_kodu = f"{isim_kismi}{rastgele_sayi}"
        db.session.commit() # Kasaya kaydet ki bir daha None olmasın!

    kullanicinin_oyunlari = Oyun.query.filter_by(olusturan_id=aktif.id).all()
    
    aktif_test_sayisi = len(kullanicinin_oyunlari)
    global_etkilesim = sum(getattr(oyun, 'oynanma_sayisi', 0) for oyun in kullanicinin_oyunlari)
    
    try:
        taclanan_sampiyon = Skor.query.join(Oyun).filter(Oyun.olusturan_id == aktif.id).count()
    except Exception:
        taclanan_sampiyon = sum(getattr(oyun, 'bitirilme_sayisi', 0) for oyun in kullanicinin_oyunlari)

    return render_template('profil.html', 
        kullanici=aktif,
        oyunlar=kullanicinin_oyunlari,
        aktif_test_sayisi=aktif_test_sayisi,
        global_etkilesim=global_etkilesim,
        taclanan_sampiyon=taclanan_sampiyon,
        takip_edilen=aktif.takip_ettikleri.count(),
        takipci_sayisi=aktif.takipcileri.count(),
        kendi_profili_mi=True
    )

@app.route('/profil/<kullanici_adi>')
def baska_profil(kullanici_adi):
    if session.get('kullanici_adi') == kullanici_adi:
        return redirect(url_for('profil'))
        
    hedef_kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first_or_404()
    
    kullanicinin_oyunlari = Oyun.query.filter_by(olusturan_id=hedef_kullanici.id).all()
    aktif_test_sayisi = len(kullanicinin_oyunlari)
    global_etkilesim = sum(getattr(oyun, 'oynanma_sayisi', 0) for oyun in kullanicinin_oyunlari)
    
    try:
        taclanan_sampiyon = Skor.query.join(Oyun).filter(Oyun.olusturan_id == hedef_kullanici.id).count()
    except Exception:
        taclanan_sampiyon = sum(getattr(oyun, 'bitirilme_sayisi', 0) for oyun in kullanicinin_oyunlari)
        
    aktif_kullanici = None
    takip_ediyor_mu = False
    
    if 'kullanici_adi' in session and not session['kullanici_adi'].startswith('Misafir_'):
        aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
        if aktif_kullanici:
            takip_ediyor_mu = aktif_kullanici.takip_ettikleri.filter(takipciler.c.takip_edilen_id == hedef_kullanici.id).count() > 0

    return render_template('profil.html',
        kullanici=hedef_kullanici,
        oyunlar=kullanicinin_oyunlari,
        aktif_test_sayisi=aktif_test_sayisi,
        global_etkilesim=global_etkilesim,
        taclanan_sampiyon=taclanan_sampiyon,
        takip_edilen=hedef_kullanici.takip_ettikleri.count(),
        takipci_sayisi=hedef_kullanici.takipcileri.count(),
        kendi_profili_mi=False,
        takip_ediyor_mu=takip_ediyor_mu
    )

@app.route('/api/takip/<kullanici_adi>', methods=['POST'])
def takip_et(kullanici_adi):
    if 'kullanici_adi' not in session or session['kullanici_adi'].startswith('Misafir_'):
        return jsonify({"status": "error", "mesaj": "Giriş yapmanız gerekiyor!"}), 401
        
    aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    hedef_kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first_or_404()
    
    if aktif_kullanici.id == hedef_kullanici.id:
        return jsonify({"status": "error", "mesaj": "Kendinizi takip edemezsiniz!"}), 400
        
    takip_ediyor = aktif_kullanici.takip_ettikleri.filter(takipciler.c.takip_edilen_id == hedef_kullanici.id).count() > 0
    
    if takip_ediyor:
        aktif_kullanici.takip_ettikleri.remove(hedef_kullanici)
        durum = "takipten_cikarildi"
    else:
        aktif_kullanici.takip_ettikleri.append(hedef_kullanici)
        durum = "takip_edildi"
        # Bildirim oluştur
        bildirim = Bildirim(
            kullanici_id=hedef_kullanici.id,
            mesaj=f"@{aktif_kullanici.kullanici_adi} seni takip etmeye başladı!"
        )
        db.session.add(bildirim)
        
    db.session.commit()
    return jsonify({
        "status": "success", 
        "durum": durum, 
        "takipci_sayisi": hedef_kullanici.takipcileri.count()
    })

@app.route('/api/bildirimler')
def bildirimleri_getir():
    if 'kullanici_adi' not in session or session['kullanici_adi'].startswith('Misafir_'):
        return jsonify({"bildirimler": []})
        
    aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    if not aktif_kullanici:
         return jsonify({"bildirimler": []})
         
    okunmamislar = Bildirim.query.filter_by(kullanici_id=aktif_kullanici.id, okundu=False).all()
    
    sonuclar = [{"id": b.id, "mesaj": b.mesaj} for b in okunmamislar]
    
    # Görüntülenenleri okundu yap
    for b in okunmamislar:
        b.okundu = True
    db.session.commit()
    
    return jsonify({"bildirimler": sonuclar})

@app.route('/api/ai_analiz', methods=['POST'])
def ai_analiz():
    data = request.json
    secimler = data.get('secimler', [])
    if not secimler: return jsonify({"analiz": "Seçim yapmadığın için analiz edemedim patron."})
    
    secim_metni = ", ".join(secimler)
    analizler = [
        f"Seçimlerin ({secim_metni}) gösteriyor ki risk almayı seviyorsun ama her zaman bir B planın var. Tam bir patronsun!",
        f"Zevklerin oldukça rafine. Herkesin seçtiğini değil, en kalitelisini istiyorsun. Bu kadroyla piyasada taş bırakmazsın!",
        f"Sen bir duygu insanısın. Kararların sadece güç değil, estetik ve vizyon barındırıyor."
    ]
    return jsonify({"analiz": random.choice(analizler)})

# --- ⚔️ CANLI DÜELLO (MİSAFİR DESTEKLİ) ---
aktif_odalar = {}

@app.route('/duello-kur/<int:oyun_id>')
def duello_kur(oyun_id):
    if 'kullanici_adi' not in session:
        session['kullanici_adi'] = f"Misafir_{random.randint(1000, 9999)}"
        
    oda_kodu = str(random.randint(10000, 99999))
    aktif_odalar[oda_kodu] = {'oyun_id': oyun_id, 'oyuncular': [], 'skorlar': {}}
    return redirect(url_for('duello_lobisi', oda_kodu=oda_kodu))

@app.route('/duello/<oda_kodu>')
def duello_lobisi(oda_kodu):
    if 'kullanici_adi' not in session:
        session['kullanici_adi'] = f"Misafir_{random.randint(1000, 9999)}"
        
    if oda_kodu not in aktif_odalar: return "Böyle bir düello odası yok, maç bitmiş olabilir."
    
    oyun_id = aktif_odalar[oda_kodu]['oyun_id']
    oyun = Oyun.query.get_or_404(oyun_id)
    return render_template('duello.html', oda_kodu=oda_kodu, oyun=oyun)

@app.route('/odaya-katil', methods=['POST'])
def odaya_katil():
    oda_kodu = request.form.get('oda_kodu', '').strip()

    # ⚔️ 1. ÖNCE DÜELLO ODASI MI?
    if oda_kodu in aktif_odalar:
        if 'kullanici_adi' not in session:
            session['kullanici_adi'] = f"Misafir_{random.randint(1000, 9999)}"
        return redirect(url_for('duello_lobisi', oda_kodu=oda_kodu))

    # 🎥 2. SONRA YAYIN ODASI MI?
    if oda_kodu in aktif_yayinlar:
        return redirect(url_for('canli_yayin_izle', oda_kodu=oda_kodu))

    # ❌ İKİSİ DE DEĞİLSE
    flash("Böyle bir oda bulunamadı veya sona ermiş! Kodu kontrol et.", "error")
    return redirect(url_for('dashboard'))
@app.route('/canli-izle/<oda_kodu>')
def canli_yayin_izle(oda_kodu):
    if oda_kodu not in aktif_yayinlar:
        return redirect(url_for('dashboard'))
        
    oyun_id = aktif_yayinlar[oda_kodu]['oyun_id']
    oyun = Oyun.query.get(oyun_id) # Veritabanından oyunu çek
    
    # İŞTE BURASI: Hazırladığın o neon tasarımlı izleyici HTML'ini çağırıyoruz!
    # (Parantez içine o HTML dosyasının adını tam olarak yaz, örn: 'izleyici_ekrani.html')
    return render_template('izleyici_ekrani.html', yayin_kodu=oda_kodu, oyun=oyun)
@socketio.on('odaya_katil')
def socket_odaya_katil(data):
    """Düello lobisine socket bağlantısı. 2 oyuncu dolunca maçı başlatır."""
    oda = data.get('oda')
    oyuncu = session.get('kullanici_adi') or f"Misafir_{random.randint(1000,9999)}"

    if oda not in aktif_odalar:
        return

    join_room(oda)

    oyuncular = aktif_odalar[oda]['oyuncular']
    if oyuncu not in oyuncular:
        oyuncular.append(oyuncu)

    # Lobi güncellemesi — kim geldi haber ver
    emit('lobi_guncelle', {'oyuncular': oyuncular}, room=oda)

    # İki oyuncu doldu → MAÇI BAŞLAT!
    if len(oyuncular) >= 2:
        emit('maci_baslat', {}, room=oda)


@socketio.on('cevap_yolla')
def cevap_yolla(data):
    oda    = data.get('oda')
    oyuncu = data.get('oyuncu') or session.get('kullanici_adi', 'Bilinmeyen')
    puan   = data.get('puan', 0)

    if oda not in aktif_odalar:
        return

    aktif_odalar[oda]['skorlar'][oyuncu] = puan
    emit('skor_guncelle', aktif_odalar[oda]['skorlar'], room=oda)


@socketio.on('oyun_bitti')
def oyun_bitti_handler(data):
    """Bir oyuncu tüm soruları bitirince çağrılır. İkisi de bitince mac_bitti."""
    oda    = data.get('oda')
    oyuncu = data.get('oyuncu') or session.get('kullanici_adi', 'Bilinmeyen')
    puan   = data.get('puan', 0)

    if oda not in aktif_odalar:
        return

    aktif_odalar[oda]['skorlar'][oyuncu] = puan

    if 'bitenler' not in aktif_odalar[oda]:
        aktif_odalar[oda]['bitenler'] = []
    if oyuncu not in aktif_odalar[oda]['bitenler']:
        aktif_odalar[oda]['bitenler'].append(oyuncu)

    # İki oyuncu da bitirdiyse maç sonu
    if len(aktif_odalar[oda]['bitenler']) >= 2:
        emit('mac_bitti', aktif_odalar[oda]['skorlar'], room=oda)



# --- 🎥 YAYINCI (STREAMER) MODU ---
aktif_yayinlar = {}

@app.route('/yayin-baslat/<int:oyun_id>')
def yayin_baslat(oyun_id):
    kadi = session.get('kullanici_adi')
    if not kadi or kadi.startswith('Misafir_'):
        return "Yayın başlatmak için gerçek bir hesapla giriş yapmalısın patron!"
        
    yayin_kodu = str(random.randint(100000, 999999))
    oyun = Oyun.query.get_or_404(oyun_id)
    aktif_yayinlar[yayin_kodu] = {
        'oyun_id': oyun_id,
        'oyun_modu': oyun.oyun_modu,
        'yayinci': kadi,
        'izleyiciler': {},       # { isim: oy_sayisi }
        'aktif_soru_index': 0
    }
    return redirect(url_for('yayinci_odasi', yayin_kodu=yayin_kodu))

@app.route('/yayin/<yayin_kodu>')
def yayinci_odasi(yayin_kodu):
    if yayin_kodu not in aktif_yayinlar:
        return "Yayın bitmiş veya böyle bir oda yok. Başka kapıya!"
        
    oyun = Oyun.query.get_or_404(aktif_yayinlar[yayin_kodu]['oyun_id'])
    yayinci = aktif_yayinlar[yayin_kodu]['yayinci']
    
    kadi = session.get('kullanici_adi')
    if not kadi:
        kadi = f"Misafir_{random.randint(1000,9999)}"
        session['kullanici_adi'] = kadi
    
    if kadi == yayinci:
        return render_template('yayinci_paneli.html', yayin_kodu=yayin_kodu, oyun=oyun)
    else:
        return render_template('izleyici_ekrani.html', yayin_kodu=yayin_kodu, oyun=oyun)

@socketio.on('yayina_katil')
def yayina_katil(data):
    oda = data.get('yayin_kodu')
    
    # 🚀 CTO HACK: Artık adamın o neon ekranda kendi elleriyle yazdığı ismi yakalıyoruz!
    # Eğer boş gelirse (hata olursa) session'dan alır, o da yoksa Misafir deriz.
    oyuncu = data.get('oyuncu_adi') or session.get('kullanici_adi') or "GizemliOyuncu"
    
    if oda in aktif_yayinlar:
        join_room(oda)
        
        # Adamı yayıncının listesine ekle
        if oyuncu != aktif_yayinlar[oda]['yayinci'] and oyuncu not in aktif_yayinlar[oda]['izleyiciler']:
            aktif_yayinlar[oda]['izleyiciler'][oyuncu] = 0
            
        emit('izleyici_listesi_guncelle', aktif_yayinlar[oda]['izleyiciler'], room=oda)
@socketio.on('yayin_hareketi')
def yayin_hareketi(data):
    oda = data.get('yayin_kodu')
    yayinci = session.get('kullanici_adi')
    aksiyon = data.get('aksiyon')

    if oda not in aktif_yayinlar:
        return
    if aktif_yayinlar[oda]['yayinci'] != yayinci:
        return

    if aksiyon == 'baslat':
        # İlk soruya geç, index sıfırda kalır
        aktif_yayinlar[oda]['aktif_soru_index'] = 0
    elif aksiyon == 'siradaki_soru':
        aktif_yayinlar[oda]['aktif_soru_index'] += 1
    elif aksiyon == 'bitir':
        # Yayını sonlandır
        pass

    emit('yayinci_emri', {
        'aksiyon': aksiyon,
        'index': aktif_yayinlar[oda]['aktif_soru_index']
    }, room=oda)

@socketio.on('izleyici_cevap_gonder')
def izleyici_cevap_gonder(data):
    oda = data.get('yayin_kodu')
    # Oyuncu adını data'dan al (isim-ekranında girilen ad)
    oyuncu = data.get('oyuncu_adi') or session.get('kullanici_adi') or 'Anonim'
    puan = data.get('puan', 0)

    if oda in aktif_yayinlar:
        aktif_yayinlar[oda]['izleyiciler'][oyuncu] = puan
        emit('canli_skor_guncelle', aktif_yayinlar[oda]['izleyiciler'], room=oda)

@socketio.on('kapisma_oy_gonder')
def kapisma_oy_gonder(data):
    """Omu Bumu / Turnuva modlarında seçenek oyunu yayıncıya ilet."""
    oda   = data.get('yayin_kodu')
    secim = data.get('secim')
    if oda in aktif_yayinlar and secim:
        # Yayıncı paneline özel oy event'i gönder
        emit('kapisma_oy', {'secim': secim}, room=oda)

# --- DIŞARIDAN GELENLER İÇİN YENİ ANA SAYFA ---
# --- 🌍 HANGIEASY ANA SAYFA (LANSMAN BİTTİ, SİSTEM CANLI!) ---
# --- 🌍 HANGIEASY ANA SAYFA (LANSMAN BİTTİ, SİSTEM CANLI!) ---
# ANA SAYFA MOTORU
# --- 🌍 DIŞARIDAN GELENLER İÇİN (GERİ SAYIM VİTRİNİ) ---
@app.route('/')
def coming_soon():
    # Toplam test sayısını da geçir
    toplam_test = Oyun.query.count()
    return render_template('countdown.html', toplam_test=toplam_test)

# --- 🕵️‍♂️ PATRON VE TEST EKİBİ İÇİN GİZLİ KAPI (ASIL SİSTEM) ---
@app.route('/dashboard')
def dashboard():
    # Tüm testleri oynanma sayısına göre sırala (en popüler üstte)
    oyunlar = Oyun.query.order_by(Oyun.oynanma_sayisi.desc()).all()
    return render_template('dashboard.html', oyunlar=oyunlar)

@app.route('/gizli-test-odasi')
def gizli_oda():
    return redirect(url_for('dashboard'))

@app.route('/guess-valorant')
def guess_valorant():
    return render_template('guess_valorant.html')


@app.route('/test-olustur', methods=['GET', 'POST'])
def test_olustur():
    kadi = session.get('kullanici_adi')
    if not kadi or kadi.startswith('Misafir_'): return redirect(url_for('giris'))
    
    if request.method == 'POST':
        aktif = Kullanici.query.filter_by(kullanici_adi=kadi).first()
        f = request.files.get('kapak_resmi')
        resim_url = ""
        
        # 🚀 Kapak resmi buluta gidiyor (Zırhlı ve Çökmez Versiyon)
        if f and f.filename != '':
            # Orijinal isimdeki boşluk veya bozuk karakterleri es geçmek için sadece uzantıyı alıyoruz
            uzanti = f.filename.split('.')[-1]
            dosya_adi = f"{uuid.uuid4().hex}.{uzanti}"
            
            # x-upsert: "true" ile Supabase'e "Çökme, gerekirse üstüne yaz!" emri veriyoruz
            supabase.storage.from_("medya").upload(
                path=dosya_adi, 
                file=f.read(), 
                file_options={"content-type": f.content_type, "x-upsert": "true"}
            )
            
            # Herkese açık (Public) bulut linkini alıyoruz
            resim_url = supabase.storage.from_("medya").get_public_url(dosya_adi)
            
        yeni = Oyun(baslik=request.form['baslik'], aciklama=request.form['aciklama'],
                    resim_url=resim_url, kategori=request.form['kategori'],
                    oyun_modu=request.form['oyun_modu'], olusturan_id=aktif.id)
        db.session.add(yeni)
        db.session.commit()
        
        return redirect(url_for('soru_ekle', oyun_id=yeni.id))
        
    return render_template('test_olustur.html')
import time
import uuid

@app.route('/soru-ekle/<int:oyun_id>', methods=['GET', 'POST'])
def soru_ekle(oyun_id):
    kadi = session.get('kullanici_adi')
    if not kadi or kadi.startswith('Misafir_'): return redirect(url_for('giris'))
    oyun = Oyun.query.get_or_404(oyun_id)
    
    if request.method == 'POST':
        
        # 🚀 CTO ÖZEL SİLAHI: Tüm oyun modlarına hizmet eden inatçı yükleyici ajan!
        def guvenli_yukle(dosya):
            if not dosya or dosya.filename == '':
                return ""
            
            uzanti = dosya.filename.split('.')[-1]
            dosya_adi = f"{uuid.uuid4().hex}.{uzanti}"
            dosya_verisi = dosya.read() # Hafızaya al ki bağlantı koparsa tekrar gönderebilelim
            
            # 3 Kere İnatla Dene (Errno 35 Katili)
            for deneme in range(3):
                try:
                    supabase.storage.from_("medya").upload(
                        dosya_adi, 
                        dosya_verisi, 
                        {"content-type": dosya.content_type, "x-upsert": "true"}
                    )
                    break # Başarılı olursa döngüyü kır!
                except Exception as e:
                    print(f"⚠️ Yükleme Hatası ({deneme+1}/3): {e}")
                    time.sleep(1.5) # 1.5 saniye soluklan, tekrar saldır
                    
            # URL'yi oluşturup tertemiz geri ver
            return supabase.storage.from_("medya").get_public_url(dosya_adi)

        # ==========================================
        # 🎮 OYUN MODLARI (Zırhlı Ajan Kullanılarak)
        # ==========================================

        if oyun.oyun_modu == 'butce_savasi':
            resim_url = guvenli_yukle(request.files.get('soru_resmi'))
            secenekler_verisi = f"{request.form.get('secenek_1')},{request.form.get('secenek_2')}"
            yeni = Soru(oyun_id=oyun.id, resim_url=resim_url, secenekler=secenekler_verisi, dogru_cevap=request.form.get('dogru_cevap'))
            db.session.add(yeni)
            
        elif oyun.oyun_modu == 'casus_kim':
            yollar = []
            for i in range(1, 5):
                url = guvenli_yukle(request.files.get(f'resim_{i}'))
                if url: yollar.append(url)
            yeni = Soru(oyun_id=oyun.id, resim_url=",".join(yollar), secenekler=request.form.get('secenekler'), dogru_cevap=request.form.get('dogru_cevap'))
            db.session.add(yeni)
            
        elif oyun.oyun_modu == 'sesli_quiz':
            ses_url = guvenli_yukle(request.files.get('soru_sesi'))
            yeni = Soru(oyun_id=oyun.id, resim_url=ses_url, secenekler=request.form.get('secenekler'), dogru_cevap=request.form.get('dogru_cevap'))
            db.session.add(yeni)
            
        elif oyun.oyun_modu in ['omu_bumu', 'surat_yarisi', 'kim_populer']:
            is1 = request.form.get('secenek_1', 'İsimsiz 1')
            is2 = request.form.get('secenek_2', 'İsimsiz 2')
            birlesik_isimler = f"{is1},{is2}"
            
            resim_yollari = []
            for alan in ['resim_1', 'resim_2']:
                url = guvenli_yukle(request.files.get(alan))
                if url: resim_yollari.append(url)
            
            # Resim yoksa veya 1 tane geldiyse yedekleme yap
            if len(resim_yollari) == 1: 
                resim_yollari.append(resim_yollari[0])
            
            birlesik_resimler = ",".join(resim_yollari)
            yeni = Soru(oyun_id=oyun.id, resim_url=birlesik_resimler, secenekler=birlesik_isimler, dogru_cevap="Farketmez")
            db.session.add(yeni)

        elif oyun.oyun_modu in ['kor_siralama', 'turnuva']:
            resimler = request.files.getlist('soru_resmi')
            isimler = request.form.getlist('secenekler')
            for i in range(len(resimler)):
                url = guvenli_yukle(resimler[i])
                if url: # Sadece resim başarıyla yüklendiyse veritabanına yaz
                    yeni = Soru(oyun_id=oyun.id, resim_url=url, secenekler=isimler[i], dogru_cevap="Farketmez")
                    db.session.add(yeni)
                    
        else: # Normal Test
            resim_url = guvenli_yukle(request.files.get('soru_resmi'))
            yeni = Soru(oyun_id=oyun.id, resim_url=resim_url, secenekler=request.form.get('secenekler'), dogru_cevap=request.form.get('dogru_cevap'))
            db.session.add(yeni)

        # Değişiklikleri Kaydet ve Yönlendir
        db.session.commit()
        if request.form.get('aksiyon') == 'devam': 
            return redirect(url_for('soru_ekle', oyun_id=oyun.id))
        return redirect(url_for('dashboard'))
        
    return render_template('soru_ekle.html', oyun=oyun, soru_sayisi=Soru.query.filter_by(oyun_id=oyun.id).count() + 1)
@app.route('/oyun/<int:oyun_id>')
def oyun_sayfasi(oyun_id):
    oyun = Oyun.query.get_or_404(oyun_id)
    sablonlar = {
        'omu_bumu': 'omu_bumu.html',
        'kor_siralama': 'kor_siralama.html',
        'turnuva': 'turnuva.html',
        'surat_yarisi': 'surat_yarisi.html', 
        'kim_populer': 'kim_populer.html',
        'butce_savasi': 'butce_savasi.html',
        'piksel_avcisi': 'piksel_avcisi.html',
        'casus_kim': 'casus_kim.html',
        'sesli_quiz': 'sesli_quiz.html'
    }
    if oyun.oynanma_sayisi is None:
        oyun.oynanma_sayisi = 0
    oyun.oynanma_sayisi += 1
    db.session.commit()
    return render_template(sablonlar.get(oyun.oyun_modu, 'index.html'), aktif_oyun=oyun_id, oyun_basligi=oyun.baslik, oyun=oyun)
@app.route('/api/sorular/<int:oyun_id>')
def api_sorular(oyun_id):
    sorular = Soru.query.filter_by(oyun_id=oyun_id).all()
    # 🚀 VİTRİNE GİDEN KARGO: Artık doğru cevap (casus) da paketin içinde!
    return jsonify([{
        "id": s.id,
        "secenekler": str(s.secenekler), 
        "resim_url": str(s.resim_url),
        "dogru_cevap": str(s.dogru_cevap) # <-- SİSTEMİ ÇÖKERTEN EKSİK BUYDU!
    } for s in sorular])
# --- 🛒 MAĞAZA & SATIN ALMA SİSTEMİ ---
# (flash zaten yukarıda import edildi)

# ==========================================
# 🛒 MAĞAZA VE ÖDEME SİSTEMLERİ (GEÇİCİ OLARAK ASKIYA ALINDI)
# Şirket stratejisi gereği ödeme altyapısı onaylanana kadar uyku modundalar.
# ==========================================

@app.route('/magaza')
def magaza():
    if 'kullanici_adi' not in session or session['kullanici_adi'].startswith('Misafir_'):
        return redirect(url_for('giris'))
    kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    return render_template('magaza.html', kullanici=kullanici)

@app.route('/api/satin_al', methods=['POST'])
def satin_al():
    if 'kullanici_adi' not in session or session['kullanici_adi'].startswith('Misafir_'):
        return jsonify({"status": "error", "mesaj": "Giriş yapmanız gerekiyor!"}), 401
        
    data = request.json
    urun_id = data.get('urun_id')
    fiyat = data.get('fiyat')
    urun_tipi = data.get('urun_tipi') # 'cerceve', 'unvan', 'bilet' vb.
    
    if not all([urun_id, fiyat, urun_tipi]):
        return jsonify({"status": "error", "mesaj": "Eksik bilgi!"}), 400
        
    kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    
    if kullanici.he_coin < int(fiyat):
        return jsonify({"status": "error", "mesaj": "Yetersiz HE-Coin bakiyesi!"}), 400
        
    # Eğer bu ürüne zaten sahipse engelle (Biletler hariç, biletler tekrar alınabilir)
    if urun_tipi == 'cerceve':
        envanter = kullanici.sahip_olunan_cerceveler.split(',') if kullanici.sahip_olunan_cerceveler else []
        if urun_id in envanter:
            return jsonify({"status": "error", "mesaj": "Bu çerçeveye zaten sahipsiniz!"}), 400
        envanter.append(urun_id)
        kullanici.sahip_olunan_cerceveler = ','.join(envanter)
        kullanici.profil_cercevesi = urun_id # Otomatik kuşan
        
    elif urun_tipi == 'unvan':
        envanter = kullanici.sahip_olunan_unvanlar.split(',') if kullanici.sahip_olunan_unvanlar else []
        if urun_id in envanter:
            return jsonify({"status": "error", "mesaj": "Bu unvana zaten sahipsiniz!"}), 400
        envanter.append(urun_id)
        kullanici.sahip_olunan_unvanlar = ','.join(envanter)
        kullanici.rutbe = urun_id # Otomatik kuşan
        
    elif urun_tipi == 'boss_bileti':
        if kullanici.boss_bileti_alindi:
             return jsonify({"status": "error", "mesaj": "Zaten aktif bir Boss Arenası biletin var!"}), 400
        kullanici.boss_bileti_alindi = True
    
    # Parayı düş
    kullanici.he_coin -= int(fiyat)
    
    # Bildirim oluştur
    bildirim = Bildirim(
        kullanici_id=kullanici.id,
        mesaj=f"Sistem: {fiyat} 🪙 karşılığında yeni eşya aldın. Envanterini kontrol et!"
    )
    db.session.add(bildirim)
    
    db.session.commit()
    return jsonify({"status": "success", "mesaj": "Satın alma başarılı!", "kalan_coin": kullanici.he_coin})


# --- 💳 STRIPE GERÇEK ÖDEME AKIŞI ---
# @app.route('/odeme-baslat/<paket>')
# def odeme_baslat(paket):
#     ... (Buradaki tüm kodlar yorum satırında kalacak) ...

# @app.route('/odeme-basarili/<int:miktar>')
# def odeme_basarili(miktar):
#     ... (Buradaki tüm kodlar yorum satırında kalacak) ...

# --- 💎 KOZMETİK MAĞAZASI YAPAY ZEKASI ---
# @app.route('/api/cerceve_al/<cerceve_id>', methods=['POST'])
# def cerceve_al(cerceve_id):
#     ... (Buradaki tüm kodlar yorum satırında kalacak) ...
@app.route('/istatistikler/<int:oyun_id>')
def istatistikler_sayfasi(oyun_id):
    # 1. Oyunu bul
    oyun = Oyun.query.get_or_404(oyun_id)
    
    # 🚀 İŞTE MOTOR BURADA ÇALIŞACAK!
    ist_listesi = Istatistik.query.filter_by(oyun_id=oyun_id).order_by(Istatistik.sampiyonluk_sayisi.desc()).all()
    
    # 3. Toplam oyu hesapla
    toplam = sum(ist.sampiyonluk_sayisi for ist in ist_listesi)
    
    # 4. Paketi HTML'e teslim et
    return render_template('istatistikler.html', 
                           oyun=oyun, 
                           istatistikler=ist_listesi, 
                           toplam_oy=toplam)
@app.route('/boss-arenasi')
def boss_arenasi():
    kadi = session.get('kullanici_adi')
    if not kadi or kadi.startswith('Misafir_'):
        return redirect(url_for('giris'))

    kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    return render_template('boss_arenasi.html',
                           bakiye=kullanici.he_coin,
                           bilet_alindi=kullanici.boss_bileti_alindi)

@app.route('/api/boss_giris', methods=['POST'])
def boss_giris():
    kadi = session.get('kullanici_adi')
    kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    giris_ucreti = 250

    # — Zaten bilet almış mı?
    if kullanici.boss_bileti_alindi:
        return jsonify({"status": "error", "mesaj": "Zaten bir bileting var patron! Etkinlik başlayana kadar bekle."}), 400

    if kullanici.he_coin >= giris_ucreti:
        kullanici.he_coin -= giris_ucreti
        kullanici.boss_bileti_alindi = True   # Bir daha alamaz
        db.session.commit()
        return jsonify({"status": "success", "yeni_bakiye": kullanici.he_coin, "mesaj": "Arenaya giriş bileti alındı!"})
    else:
        return jsonify({"status": "error", "mesaj": "Fakirler giremez! Mağazadan coin al patron."}), 400

@app.route('/oyun-sil/<int:oyun_id>', methods=['POST'])
def oyun_sil(oyun_id):
    oyun = Oyun.query.get_or_404(oyun_id)
    Soru.query.filter_by(oyun_id=oyun.id).delete()
    db.session.delete(oyun); db.session.commit()
    return redirect(url_for('profil'))

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        kullanici_adi = request.form.get('kullanici_adi')
        eposta = request.form.get('eposta')
        dogum_tarihi = request.form.get('dogum_tarihi')
        sifre = request.form.get('sifre')

        # 1. VERİTABANI KONTROLÜ
        mevcut_kullanici = Kullanici.query.filter((Kullanici.eposta == eposta) | (Kullanici.kullanici_adi == kullanici_adi)).first()
        if mevcut_kullanici:
            flash("Bu e-posta veya kullanıcı adı zaten kullanımda! Lütfen giriş yapın veya başka bir tane deneyin.", "error")
            return redirect(url_for('kayit'))

        hashed_sifre = generate_password_hash(sifre, method='pbkdf2:sha256')

        # 2. YENİ KULLANICI (onayli_mi = False olarak geri döndü!)
        yeni_kullanici = Kullanici(
            ad_soyad=ad_soyad,
            kullanici_adi=kullanici_adi,
            eposta=eposta,
            dogum_tarihi=dogum_tarihi,
            sifre_hash=hashed_sifre, 
            onayli_mi=False  # Patronun emriyle doğrulama sistemi devrede!
        )
        
        db.session.add(yeni_kullanici)
        db.session.commit()
        
        # 3. MAİL GÖNDER — arka plan thread'inde (sayfayı bloke etmesin!)
        token = s.dumps(eposta, salt='eposta-dogrulama')
        site_url = os.getenv('SITE_URL', 'https://hangieasy.com').rstrip('/')
        dogrulama_linki = f"{site_url}/dogrula/{token}"

        msg = Message('HangiEasy Krallığına Hoş Geldin! 👑', recipients=[eposta])
        msg.html = f"""
        <div style="background-color:#0b0c10; color:white; padding:30px; font-family:sans-serif; border-radius:10px; text-align:center;">
            <h1 style="color:#00b09b;">Aramıza Hoş Geldin {kullanici_adi}!</h1>
            <p style="color:#aaa; font-size:16px;">HangiEasy'de rakiplerini ezmeye başlamadan önce son bir adım kaldı.</p>
            <p>Aşağıdaki butona tıklayarak e-posta adresini doğrula ve hesabını aktifleştir:</p>
            <a href="{dogrulama_linki}" style="display:inline-block; padding:15px 30px; background-color:#f39c12; color:#000; text-decoration:none; font-weight:bold; border-radius:10px; margin-top:20px;">HESABIMI ONAYLA ⚡</a>
            <p style="color:#666; font-size:12px; margin-top:30px;">Bu link 1 saat boyunca geçerlidir.</p>
        </div>
        """

        def mail_gonder_bg(flask_app, mesaj):
            """Mail'i arka planda gönder — isteği bloke etme."""
            with flask_app.app_context():
                try:
                    mail.send(mesaj)
                    print(f"✅ Doğrulama maili gönderildi: {eposta}")
                except Exception as ex:
                    print(f"❌ Mail gönderilemedi ({eposta}): {ex}")

        t = threading.Thread(target=mail_gonder_bg, args=(app, msg), daemon=True)
        t.start()

        # Kullanıcıyı BEKLETMEDEN anında başarı sayfasına gönder
        return render_template('kayit_basarili.html',
                               mail_gonderildi=True,   # Arka planda gönderiliyor, iyimser göster
                               eposta=eposta,
                               dogrulama_linki=dogrulama_linki)

    return render_template('kayit.html')
@app.route('/dogrula/<token>')
def dogrula(token):
    try:
        # Token'ı çözüyoruz, max_age=3600 (1 saat) geçerlilik süresi var
        eposta = s.loads(token, salt='eposta-dogrulama', max_age=3600)
    except SignatureExpired:
        return "<h1>⏳ Doğrulama linkinin süresi dolmuş! Lütfen tekrar kayıt olun.</h1>"
    except Exception:
        return "<h1>❌ Geçersiz doğrulama linki!</h1>"

    # BURADA VERİTABANINI GÜNCELLE (CTO Dokunuşu)
    # 1. Bu e-postaya sahip kullanıcıyı bul.
    kullanici = Kullanici.query.filter_by(eposta=eposta).first()
    
    if not kullanici:
        return "<h1>❌ Bu e-postaya ait bir hesap bulunamadı!</h1>"
        
    if kullanici.onayli_mi:
        # Adam zaten onaylamış, tekrar basarsa hata vermesin
        return render_template('dogrulama_basarili.html')

    # 2. kullanici.onayli_mi = True yap ve veritabanına kaydet (commit).
    kullanici.onayli_mi = True
    db.session.commit()
    
    # HER ŞEY BAŞARILIYSA EFSANE ONAY EKRANINI ÇAĞIR!
    return render_template('dogrulama_basarili.html')
@app.route('/giris', methods=['GET', 'POST'])
def giris():
    hata = None
    if request.method == 'POST':
        kullanici = Kullanici.query.filter_by(kullanici_adi=request.form['kullanici_adi']).first()
        if kullanici and check_password_hash(kullanici.sifre_hash, request.form['sifre']):
            # Onaylı olsun olmasın girişe izin ver
            session['kullanici_adi'] = kullanici.kullanici_adi
            session['onayli_mi'] = kullanici.onayli_mi  # Profile banner için
            return redirect(url_for('dashboard'))
        else:
            hata = "Kullanıcı adı veya şifre hatalı!"
    return render_template('giris.html', hata=hata)
@app.route('/cikis')
def cikis():
    session.clear()
    return redirect(url_for('dashboard'))

@app.route('/yeniden-dogrula')
def yeniden_dogrula():
    """Onaylı değil hesap için doğrulama mailini tekrar gönder."""
    kadi = session.get('kullanici_adi')
    if not kadi:
        return redirect(url_for('giris'))

    kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    if not kullanici:
        return redirect(url_for('giris'))

    if kullanici.onayli_mi:
        # Zaten onaylı, gerek yok
        flash("✅ Hesabın zaten onaylanmış!", "success")
        return redirect(url_for('profil'))

    token = s.dumps(kullanici.eposta, salt='eposta-dogrulama')
    site_url = os.getenv('SITE_URL', 'https://hangieasy.com').rstrip('/')
    dogrulama_linki = f"{site_url}/dogrula/{token}"

    msg = Message('HangiEasy — Hesabını Onayla ⚡', recipients=[kullanici.eposta])
    msg.html = f"""
    <div style="background-color:#0b0c10; color:white; padding:30px; font-family:sans-serif; border-radius:10px; text-align:center;">
        <h1 style="color:#f39c12;">E-posta Doğrulama ⚡</h1>
        <p style="color:#aaa;">Merhaba {kullanici.kullanici_adi}! Hesabını aktifleştirmek için aşağıya tıkla:</p>
        <a href="{dogrulama_linki}" style="display:inline-block; padding:15px 30px; background-color:#f39c12; color:#000; text-decoration:none; font-weight:bold; border-radius:10px; margin-top:20px;">HESABIMI ONAYLA ⚡</a>
        <p style="color:#666; font-size:12px; margin-top:30px;">Bu link 1 saat geçerlidir.</p>
    </div>
    """

    def mail_bg(flask_app, mesaj):
        with flask_app.app_context():
            try:
                mail.send(mesaj)
                print(f"✅ Yeniden doğrulama maili gönderildi: {kullanici.eposta}")
            except Exception as ex:
                print(f"❌ Mail hatası: {ex}")

    threading.Thread(target=mail_bg, args=(app, msg), daemon=True).start()
    return render_template('kayit_basarili.html',
                           mail_gonderildi=True,
                           eposta=kullanici.eposta,
                           dogrulama_linki=dogrulama_linki)

@app.route('/god-mode')
def god_mode():
    kadi = session.get('kullanici_adi')
    # Sadece senin yeni kullanıcı adın olan 'onur' girebilir!
    if kadi != "onur": 
        return "Hop hemşerim nereye? Burası Onur Çakal A.Ş. Yönetim Kurulu odası! Sadece patron girebilir.", 403
    
    # ... geri kalan kodlar ...
    toplam_kullanici = Kullanici.query.count()
    toplam_test = Oyun.query.count()
    tum_kullanicilar = Kullanici.query.order_by(Kullanici.he_coin.desc()).all() 
    tum_oyunlar = Oyun.query.all()
    
    return render_template('admin.html', 
                           tk=toplam_kullanici, 
                           tt=toplam_test, 
                           kullanicilar=tum_kullanicilar,
                           oyunlar=tum_oyunlar)
# 🚀 CEO İNFAZ MOTORU: KULLANICI BANLAMA
# 🚀 CEO İNFAZ MOTORU: KULLANICI BANLAMA (SQLAlchemy Versiyonu)
@app.route('/admin-kullanici-sil/<int:id>', methods=['POST'])
def kullanici_sil(id):
    silinecek_kullanici = Kullanici.query.get_or_404(id)
    
    # Kullanıcının oluşturduğu testleri de beraberinde buharlaştırıyoruz
    Oyun.query.filter_by(olusturan_id=id).delete()
    
    # Kullanıcıyı veritabanından kalıcı olarak sil
    db.session.delete(silinecek_kullanici)
    db.session.commit()
    
    # İşlem bitince hemen CEO paneline geri dön
    return redirect(url_for('god_mode'))


# 🚀 CEO İNFAZ MOTORU: TEST SİLME (SQLAlchemy Versiyonu)
@app.route('/admin-test-sil/<int:id>', methods=['POST'])
def test_sil(id):
    silinecek_test = Oyun.query.get_or_404(id)
    
    # Teste bağlı soruları da komple temizle
    Soru.query.filter_by(oyun_id=id).delete()
    
    # Testi kalıcı olarak sil
    db.session.delete(silinecek_test)
    db.session.commit()
    
    # İşlem bitince hemen CEO paneline geri dön
    return redirect(url_for('god_mode'))

@app.route('/aydinlatma-metni') # Bak burada tire (-) var!
def aydinlatma_metni():
    return render_template('aydinlatma_metni.html') # Burada alt çizgi (_) var çünkü dosya adı böyle.

@app.route('/kullanici-sozlesmesi')
def kullanici_sozlesmesi():
    return render_template('kullanici_sozlesmesi.html')

@app.route('/pp-guncelle', methods=['POST'])
def pp_guncelle():
    kadi = session.get('kullanici_adi')
    if not kadi: return redirect(url_for('giris'))
    
    dosya = request.files.get('profil_fotografi')
    if dosya and dosya.filename != '':
        uzanti = dosya.filename.split('.')[-1]
        dosya_adi = f"pp_{kadi}_{uuid.uuid4().hex}.{uzanti}"
        
        # Supabase'e fırlatıyoruz!
        supabase.storage.from_("medya").upload(
            path=dosya_adi, 
            file=dosya.read(), 
            file_options={"content-type": dosya.content_type, "x-upsert": "true"}
        )
        
        # Resmin herkese açık URL'ini çek ve kasaya kaydet
        resim_url = supabase.storage.from_("medya").get_public_url(dosya_adi)
        
        kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
        kullanici.profil_resmi = resim_url
        db.session.commit()
        
    return redirect(url_for('profil'))

@app.route('/veri-gizlilik')
def veri_gizlilik():
    return render_template('veri_gizlilik.html')
from datetime import datetime

# 🚀 CTO DOKUNUŞU: HangiEasy Rütbe ve İlerleme Motoru
def ilerleme_kaydet(kullanici_adi, kazanilan_puan=0):
    kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
    
    if not kullanici:
        return False # Eğer misafirse ilerleme kaydetme
        
    bugun = datetime.now().strftime('%Y-%m-%d')

    # 1. Günlük Sıfırlama Kontrolü (Yeni bir gün mü?)
    if kullanici.son_gorev_tarihi != bugun:
        kullanici.gunluk_test_sayaci = 0
        kullanici.gunluk_odul_alindi = False
        kullanici.son_gorev_tarihi = bugun

    # 2. İlerlemeyi Yaz (Skor Ekle ve Sayaçları Artır)
    kullanici.he_coin += kazanilan_puan # Oyundan kazandığı puanı coin'e veya puana dönüştür
    kullanici.cozulen_test_sayisi += 1
    kullanici.gunluk_test_sayaci += 1

    # 3. RÜTBE ALGORİTMASI (Şirket Hiyerarşisi)
    toplam_test = kullanici.cozulen_test_sayisi
    
    if toplam_test >= 100:
        kullanici.rutbe = "CEO" # Patron sensin, ama 100 teste ulaşan oyuncu da CEO olur!
    elif toplam_test >= 50:
        kullanici.rutbe = "Müdür"
    elif toplam_test >= 20:
        kullanici.rutbe = "Uzman"
    elif toplam_test >= 5:
        kullanici.rutbe = "Asistan"
    else:
        kullanici.rutbe = "Stajyer"

    # Kasayı Kilitle
    db.session.commit()
    return True
@app.route('/kimim-ben')
def kimim_ben():
    kullanicilar = Kullanici.query.all()
    liste = [f"{k.kullanici_adi} - {k.eposta}" for k in kullanicilar]
    return f"Sistemdeki Krallar: {liste}"
@app.route('/robots.txt')
def robots():
    # Google botlarına "Bütün siteyi tarayabilirsin" emrini veriyoruz.
    return "User-agent: *\nAllow: /"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)