import gevent.monkey
gevent.monkey.patch_all()

import os
import time
import uuid
import random
import string
import threading
from datetime import date

# --- FLASK VE EKLENTİLER ---
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import requests
import json

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
# --- 📧 HANGIEASY POSTACI (RESEND API) ---
def send_email_via_resend(to_email, subject, html_content):
    api_key = os.getenv('RESEND_API_KEY')
    if not api_key:
        print("❌ RESEND_API_KEY bulunamadı! Lütfen Vercel veya .env'ye ekleyin.")
        return False, "Sistemde API anahtarı eksik."
        
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "HangiEasy <noreply@hangieasy.com>",
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"✅ Resend API ile e-posta gönderildi: {to_email}")
        return True, "E-posta başarıyla gönderildi."
    except requests.exceptions.RequestException as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response is not None:
            error_detail = e.response.text
        print(f"❌ Resend API Hatası: {e} - {error_detail}")
        return False, f"Resend API Hatası: {error_detail}"
# --- 💾 YEREL VERİTABANI (SQLITE) VE KLASÖR AYARLARI ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'ogg'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 🚀 3. EKLENTİLERİ MOTORA BAĞLA

# Mail config removed
CORS(app)
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
    onay_kodu = db.Column(db.String(10), nullable=True)
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

class HaritaSkor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_turu = db.Column(db.String(50), nullable=False) # 'tr_map' or 'world_map'
    kullanici_adi = db.Column(db.String(100), nullable=False)
    bulunan_sehir_sayisi = db.Column(db.Integer, nullable=False)
    gecen_sure_saniye = db.Column(db.Integer, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

class BossAbone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eposta = db.Column(db.String(120), nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

class HangisiOyun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text, nullable=True)
    resim_url = db.Column(db.String(500), nullable=True)
    olusturan_id = db.Column(db.Integer, nullable=True) # Admin for now
    olusturan_adi = db.Column(db.String(100), default="HangiEasy")
    oynanma_sayisi = db.Column(db.Integer, default=0)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

class HangisiSoru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_id = db.Column(db.Integer, db.ForeignKey('hangisi_oyun.id'), nullable=False)
    soru_metni = db.Column(db.Text, nullable=False)
    resim_url = db.Column(db.String(500), nullable=True)
    secenek_a = db.Column(db.String(200), nullable=False)
    secenek_b = db.Column(db.String(200), nullable=False)
    secenek_c = db.Column(db.String(200), nullable=False)
    secenek_d = db.Column(db.String(200), nullable=False)
    dogru_cevap = db.Column(db.String(1), nullable=False) # A, B, C or D

class HangisiSkor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_id = db.Column(db.Integer, db.ForeignKey('hangisi_oyun.id'), nullable=False)
    kullanici_adi = db.Column(db.String(100), nullable=False)
    puan = db.Column(db.Integer, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

class HangisiTepki(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_id = db.Column(db.Integer, db.ForeignKey('hangisi_oyun.id'), nullable=False)
    kullanici_adi = db.Column(db.String(100), nullable=False)
    tepki = db.Column(db.String(50), nullable=False) # e.g. 'ates', 'beyin', 'gulme'
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
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS sahip_olunan_unvanlar TEXT DEFAULT ''",
        "ALTER TABLE kullanici ADD COLUMN IF NOT EXISTS onay_kodu VARCHAR(10)"
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

    # 🔄 GÜNLÜK SIFIRLAMA KONTROLÜ — Her profil ziyaretinde günü kontrol et
    bugun = datetime.now().strftime('%Y-%m-%d')
    if aktif.son_gorev_tarihi != bugun:
        aktif.gunluk_test_sayaci = 0
        aktif.gunluk_odul_alindi = False
        aktif.son_gorev_tarihi = bugun
        db.session.commit()

    kullanicinin_oyunlari = Oyun.query.filter_by(olusturan_id=aktif.id).all()
    
    aktif_test_sayisi = len(kullanicinin_oyunlari)
    global_etkilesim = sum((getattr(oyun, 'oynanma_sayisi', 0) or 0) for oyun in kullanicinin_oyunlari)
    
    try:
        taclanan_sampiyon = Skor.query.join(Oyun).filter(Oyun.olusturan_id == aktif.id).count()
    except Exception:
        taclanan_sampiyon = sum((getattr(oyun, 'bitirilme_sayisi', 0) or 0) for oyun in kullanicinin_oyunlari)

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
    global_etkilesim = sum((getattr(oyun, 'oynanma_sayisi', 0) or 0) for oyun in kullanicinin_oyunlari)
    
    try:
        taclanan_sampiyon = Skor.query.join(Oyun).filter(Oyun.olusturan_id == hedef_kullanici.id).count()
    except Exception:
        taclanan_sampiyon = sum((getattr(oyun, 'bitirilme_sayisi', 0) or 0) for oyun in kullanicinin_oyunlari)
        
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
# ANA SAYFA MOTORU
# --- 🌍 DIŞARIDAN GELENLER İÇİN ANA SAYFA ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Tüm testleri oynanma sayısına göre sırala (en popüler üstte)
    oyunlar = Oyun.query.order_by(Oyun.oynanma_sayisi.desc()).all()
    
    kullanici = None
    kadi = session.get('kullanici_adi')
    if kadi and not kadi.startswith('Misafir_'):
        kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    
    return render_template('dashboard.html', oyunlar=oyunlar, kullanici=kullanici)

@app.route('/world-cup-2026')
def world_cup_2026():
    # Sadece World Cup 2026 kategorisindeki veya başlığındaki oyunları filtrele
    oyunlar = Oyun.query.filter(Oyun.kategori == 'World Cup 2026').all()
    return render_template('world_cup_2026.html', oyunlar=oyunlar)

@app.route('/gizli-test-odasi')
def gizli_oda():
    return redirect(url_for('dashboard'))

@app.route('/guess-valorant')
def guess_valorant():
    return render_template('guess_valorant.html')

@app.route('/guess-lol')
def guess_lol():
    return render_template('guess_lol.html')

@app.route('/guess-turkey')
def guess_turkey():
    return render_template('guess_turkey.html')

@app.route('/guess-world')
def guess_world():
    return render_template('guess_world.html')

@app.route('/guess-word')
def guess_word():
    return render_template('guess_word.html')



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
                    
        elif oyun.oyun_modu == 'klasik_test':
            soru_metni = request.form.get('soru_metni', 'Metin yok')
            # resim_url alanını soru metnini tutmak için kullanıyoruz
            yeni = Soru(oyun_id=oyun.id, resim_url=soru_metni, secenekler=request.form.get('secenekler'), dogru_cevap=request.form.get('dogru_cevap'))
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
        'sesli_quiz': 'sesli_quiz.html',
        'klasik_test': 'klasik_test.html'
    }
    if oyun.oynanma_sayisi is None:
        oyun.oynanma_sayisi = 0
    oyun.oynanma_sayisi += 1
    db.session.commit()
    return render_template(sablonlar.get(oyun.oyun_modu, 'index.html'), aktif_oyun=oyun_id, oyun_basligi=oyun.baslik, oyun=oyun)
@app.route('/api/harita_skor_kaydet', methods=['POST'])
def harita_skor_kaydet():
    data = request.json
    try:
        yeni_skor = HaritaSkor(
            oyun_turu=data['oyun_turu'],
            kullanici_adi=data['kullanici_adi'],
            bulunan_sehir_sayisi=int(data['bulunan_sehir_sayisi']),
            gecen_sure_saniye=int(data['gecen_sure_saniye'])
        )
        db.session.add(yeni_skor)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/harita_liderlik_tablosu/<oyun_turu>')
def harita_liderlik_tablosu(oyun_turu):
    skorlar = HaritaSkor.query.filter_by(oyun_turu=oyun_turu)\
        .order_by(HaritaSkor.bulunan_sehir_sayisi.desc(), HaritaSkor.gecen_sure_saniye.asc())\
        .limit(10).all()
    
    sonuclar = []
    for s in skorlar:
        sonuclar.append({
            'kullanici_adi': s.kullanici_adi,
            'bulunan_sehir_sayisi': s.bulunan_sehir_sayisi,
            'gecen_sure_saniye': s.gecen_sure_saniye,
            'tarih': s.tarih.strftime('%d.%m.%Y')
        })
    return jsonify(sonuclar)

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

@app.route('/api/bilet_kullan', methods=['POST'])
def bilet_kullan():
    if 'kullanici_adi' not in session or session['kullanici_adi'].startswith('Misafir_'):
        return jsonify({"status": "error", "mesaj": "Giriş yapmanız gerekiyor!"}), 401
    
    kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    
    data = request.json
    tip = data.get('tip', 'boss')
    
    if tip == 'boss':
        if not kullanici.boss_bileti_alindi:
            return jsonify({"status": "error", "mesaj": "Aktif bir Boss biletin yok!"}), 400
        kullanici.boss_bileti_alindi = False
        db.session.commit()
        return jsonify({"status": "success", "mesaj": "Boss bileti kullanıldı!"})
    
    return jsonify({"status": "error", "mesaj": "Geçersiz bilet tipi!"}), 400


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
@app.route('/api/boss_abone', methods=['POST'])
def boss_abone():
    data = request.json
    eposta = data.get('eposta', '').strip()
    if not eposta or '@' not in eposta:
        return jsonify({'status': 'error', 'message': 'Geçersiz e-posta'}), 400
    
    # Check if already subscribed
    mevcut = BossAbone.query.filter_by(eposta=eposta).first()
    if mevcut:
        return jsonify({'status': 'success', 'message': 'Zaten kayıtlı'})
    
    yeni_abone = BossAbone(eposta=eposta)
    db.session.add(yeni_abone)
    db.session.commit()
    
    # Send email via Resend
    html_content = f"""
    <div style="font-family: sans-serif; text-align: center; color: #fff; background-color: #111; padding: 40px; border-radius: 10px;">
        <h1 style="color: #ff0055;">Boss Arenası Radarı Aktif! 🎯</h1>
        <p style="font-size: 16px;">Selamlar cesur savaşçı,</p>
        <p style="font-size: 16px;">E-posta adresin Boss Arenası radar sistemimize kaydedildi.</p>
        <p style="font-size: 16px;">Büyük Boss uyandığı anda sana ilk haberi biz vereceğiz. Kılıcını bileyip hazır bekle!</p>
        <br>
        <p style="color: #666; font-size: 12px;">HangiEasy Krallığı</p>
    </div>
    """
    send_email_via_resend(eposta, "Boss Uyandığında İlk Sen Öğren! 🐉", html_content)
    
    return jsonify({'status': 'success'})

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
    kadi = session.get('kullanici_adi')
    if not kadi or kadi.startswith('Misafir_'):
        return redirect(url_for('giris'))
    
    oyun = Oyun.query.get_or_404(oyun_id)
    if oyun.olusturan_kullanici_adi != kadi:
        return "Bu testi silme yetkiniz yok!", 403
        
    Soru.query.filter_by(oyun_id=oyun.id).delete()
    db.session.delete(oyun); db.session.commit()
    return redirect(url_for('profil', kadi=kadi))

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    # Misafir olarak skor kaydedip gelenleri yakala
    if request.args.get('hangisi_oyun_id') and request.args.get('hangisi_skor'):
        session['pending_hangisi_oyun_id'] = request.args.get('hangisi_oyun_id')
        session['pending_hangisi_skor'] = request.args.get('hangisi_skor')

    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        kullanici_adi = request.form.get('kullanici_adi')
        eposta = request.form.get('eposta')
        dogum_tarihi = request.form.get('dogum_tarihi')
        sifre = request.form.get('sifre')

        mevcut_kullanici = Kullanici.query.filter((Kullanici.eposta == eposta) | (Kullanici.kullanici_adi == kullanici_adi)).first()
        if mevcut_kullanici:
            flash("Bu e-posta veya kullanıcı adı zaten kullanımda! Lütfen giriş yapın veya başka bir tane deneyin.", "error")
            return redirect(url_for('kayit'))

        hashed_sifre = generate_password_hash(sifre, method='pbkdf2:sha256')
        rastgele_kod = str(random.randint(100000, 999999))

        yeni_kullanici = Kullanici(
            ad_soyad=ad_soyad,
            kullanici_adi=kullanici_adi,
            eposta=eposta,
            dogum_tarihi=dogum_tarihi,
            sifre_hash=hashed_sifre, 
            onayli_mi=False,
            onay_kodu=rastgele_kod
        )
        
        db.session.add(yeni_kullanici)
        db.session.commit()
        
        html_content = f"""
        <div style="background-color:#0b0c10; color:white; padding:30px; font-family:sans-serif; border-radius:10px; text-align:center;">
            <h1 style="color:#00b09b;">Aramıza Hoş Geldin {kullanici_adi}!</h1>
            <p style="color:#aaa; font-size:16px;">Hesabını onaylamak ve <strong style="color:#f39c12;">100 HE-Coin</strong> kazanmak için gereken kodun aşağıda!</p>
            <div style="font-size:32px; font-weight:900; letter-spacing:10px; color:#f39c12; margin:30px 0; padding:20px; background:rgba(255,255,255,0.05); border-radius:10px; border:2px dashed #f39c12;">
                {rastgele_kod}
            </div>
            <p style="color:#666; font-size:12px; margin-top:30px;">Bu kod senin içindir, lütfen kimseyle paylaşma.</p>
        </div>
        """

        success, err_msg = send_email_via_resend(eposta, 'HangiEasy Krallığına Hoş Geldin! 👑', html_content)
        if not success:
            flash(f"E-posta gönderilemedi! Hata: {err_msg}", "error")

        session['onay_bekleyen_eposta'] = eposta
        return redirect(url_for('dogrula'))

    return render_template('kayit.html')

@app.route('/dogrula', methods=['GET', 'POST'])
def dogrula():
    eposta = session.get('onay_bekleyen_eposta')
    if not eposta:
        flash("Önce giriş yapmalısınız veya kayıt olmalısınız.", "error")
        return redirect(url_for('giris'))
        
    kullanici = Kullanici.query.filter_by(eposta=eposta).first()
    if not kullanici:
        session.pop('onay_bekleyen_eposta', None)
        return redirect(url_for('giris'))
        
    if kullanici.onayli_mi:
        session.pop('onay_bekleyen_eposta', None)
        return render_template('dogrulama_basarili.html')

    if request.method == 'POST':
        girilen_kod = request.form.get('kod')
        
        if girilen_kod and girilen_kod.strip() == kullanici.onay_kodu:
            kullanici.onayli_mi = True
            kullanici.onay_kodu = None
            kullanici.he_coin += 100
            db.session.commit()
            
            session.pop('onay_bekleyen_eposta', None)
            session['kullanici_adi'] = kullanici.kullanici_adi
            session['onayli_mi'] = True
            
            # --- MİSAFİR TRIVIA SKOR KAYDI KONTROLÜ ---
            pending_oyun = session.get('pending_hangisi_oyun_id')
            pending_skor = session.get('pending_hangisi_skor')
            if pending_oyun and pending_skor:
                try:
                    yeni_skor = HangisiSkor(
                        oyun_id=int(pending_oyun),
                        kullanici_adi=kullanici.kullanici_adi,
                        puan=int(pending_skor)
                    )
                    db.session.add(yeni_skor)
                    db.session.commit()
                    # Temizle
                    session.pop('pending_hangisi_oyun_id', None)
                    session.pop('pending_hangisi_skor', None)
                except Exception as e:
                    pass
            # ------------------------------------------
            
            return render_template('dogrulama_basarili.html')
        else:
            flash("Hatalı kod girdiniz! Lütfen e-postanızı kontrol edin.", "error")
            
    return render_template('dogrula.html', eposta=eposta)
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

@app.route('/sifremi-unuttum', methods=['GET', 'POST'])
def sifremi_unuttum():
    if request.method == 'POST':
        eposta = request.form.get('eposta')
        kullanici = Kullanici.query.filter_by(eposta=eposta).first()
        
        if kullanici:
            token = s.dumps(eposta, salt='sifre-sifirlama')
            site_url = os.getenv('SITE_URL', 'https://hangieasy.com').rstrip('/')
            sifirlama_linki = f"{site_url}/sifreyi-yenile/{token}"
            
            html_content = f"""
            <div style="background-color:#0b0c10; color:white; padding:30px; font-family:sans-serif; border-radius:10px; text-align:center;">
                <h1 style="color:#f39c12;">Şifre Sıfırlama ⚡</h1>
                <p style="color:#aaa;">Merhaba {kullanici.kullanici_adi}! Şifreni sıfırlamak için aşağıdaki butona tıkla:</p>
                <a href="{sifirlama_linki}" style="display:inline-block; padding:15px 30px; background-color:#f39c12; color:#000; text-decoration:none; font-weight:bold; border-radius:10px; margin-top:20px;">ŞİFREMİ YENİLE ⚡</a>
                <p style="color:#666; font-size:12px; margin-top:30px;">Bu link 1 saat geçerlidir.</p>
                <p style="color:#666; font-size:12px;">Eğer bu isteği sen yapmadıysan, bu mesajı görmezden gelebilirsin.</p>
            </div>
            """
            
            success, err_msg = send_email_via_resend(eposta, 'HangiEasy — Şifre Sıfırlama ⚡', html_content)
            if not success:
                flash(f"E-posta gönderilemedi! Hata: {err_msg}", "error")
            
        flash("Eğer bu e-posta adresi sistemimizde kayıtlıysa, şifre sıfırlama bağlantısı gönderdik.", "success")
        return redirect(url_for('sifremi_unuttum'))
        
    return render_template('sifremi_unuttum.html')

@app.route('/sifreyi-yenile/<token>', methods=['GET', 'POST'])
def sifreyi_yenile(token):
    try:
        eposta = s.loads(token, salt='sifre-sifirlama', max_age=3600)
    except SignatureExpired:
        flash("Şifre sıfırlama linkinin süresi dolmuş. Lütfen tekrar istek gönderin.", "error")
        return redirect(url_for('sifremi_unuttum'))
    except Exception:
        flash("Geçersiz şifre sıfırlama linki.", "error")
        return redirect(url_for('sifremi_unuttum'))
        
    if request.method == 'POST':
        sifre = request.form.get('sifre')
        sifre_tekrar = request.form.get('sifre_tekrar')
        
        if sifre != sifre_tekrar:
            flash("Şifreler eşleşmiyor!", "error")
            return redirect(url_for('sifreyi_yenile', token=token))
            
        kullanici = Kullanici.query.filter_by(eposta=eposta).first()
        if not kullanici:
            flash("Kullanıcı bulunamadı.", "error")
            return redirect(url_for('giris'))
            
        hashed_sifre = generate_password_hash(sifre, method='pbkdf2:sha256')
        kullanici.sifre_hash = hashed_sifre
        db.session.commit()
        
        flash("Şifreniz başarıyla güncellendi. Şimdi giriş yapabilirsiniz.", "success")
        return redirect(url_for('giris'))
        
    return render_template('sifreyi_yenile.html')


@app.route('/yeniden-dogrula')
def yeniden_dogrula():
    kadi = session.get('kullanici_adi')
    eposta = session.get('onay_bekleyen_eposta')
    
    kullanici = None
    if kadi and not kadi.startswith('Misafir_'):
        kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
    elif eposta:
        kullanici = Kullanici.query.filter_by(eposta=eposta).first()
        
    if not kullanici:
        return redirect(url_for('giris'))

    if kullanici.onayli_mi:
        flash("✅ Hesabın zaten onaylanmış!", "success")
        return redirect(url_for('profil'))

    rastgele_kod = str(random.randint(100000, 999999))
    kullanici.onay_kodu = rastgele_kod
    db.session.commit()

    html_content = f"""
    <div style="background-color:#0b0c10; color:white; padding:30px; font-family:sans-serif; border-radius:10px; text-align:center;">
        <h1 style="color:#f39c12;">E-posta Doğrulama ⚡</h1>
        <p style="color:#aaa;">Merhaba {kullanici.kullanici_adi}! Hesabını aktifleştirmek için yeni kodun aşağıda:</p>
        <div style="font-size:32px; font-weight:900; letter-spacing:10px; color:#f39c12; margin:30px 0; padding:20px; background:rgba(255,255,255,0.05); border-radius:10px; border:2px dashed #f39c12;">
            {rastgele_kod}
        </div>
        <p style="color:#666; font-size:12px; margin-top:30px;">Eğer kod çalışmazsa sayfadan tekrar kod isteyebilirsin.</p>
    </div>
    """

    success, err_msg = send_email_via_resend(kullanici.eposta, 'HangiEasy — Yeni Onay Kodun ⚡', html_content)
    if not success:
        flash(f"E-posta gönderilemedi! Hata: {err_msg}", "error")
    else:
        session['onay_bekleyen_eposta'] = kullanici.eposta
        flash("Yeni kod e-posta adresinize gönderildi.", "success")
    return redirect(url_for('dogrula'))

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

@app.route('/api/takip_listesi/<kadi>/<tip>', methods=['GET'])
def takip_listesi(kadi, tip):
    # kadi: profili görüntülenen kişi
    # tip: 'takipciler' veya 'takip_edilenler'
    hedef = Kullanici.query.filter_by(kullanici_adi=kadi).first_or_404()
    oturum_kadi = session.get('kullanici_adi')
    aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=oturum_kadi).first() if oturum_kadi and not oturum_kadi.startswith('Misafir_') else None

    if tip == 'takipciler':
        liste = hedef.takipcileri.all()
    elif tip == 'takip_edilenler':
        liste = hedef.takip_ettikleri.all()
    else:
        return jsonify({"hata": "Geçersiz tip"}), 400

    sonuc = []
    for k in liste:
        takip_ediyor_mu = False
        if aktif_kullanici and aktif_kullanici.id != k.id:
            takip_ediyor_mu = aktif_kullanici.takip_ettikleri.filter(takipciler.c.takip_edilen_id == k.id).count() > 0
        
        avatar = k.profil_resmi if k.profil_resmi else '/static/default-avatar.png'
        sonuc.append({
            "kullanici_adi": k.kullanici_adi,
            "avatar_url": avatar,
            "takip_ediyor_mu": takip_ediyor_mu,
            "kendisi_mi": (aktif_kullanici and aktif_kullanici.id == k.id)
        })

    return jsonify({"kullanicilar": sonuc})

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

# --- 📱 MOBİL UYGULAMA API UÇ NOKTALARI (PHASE 1) ---

@app.route('/api/auth/register', methods=['POST'])
def api_auth_register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Veri alınamadı.'}), 400
    
    ad_soyad = data.get('ad_soyad')
    kullanici_adi = data.get('kullanici_adi')
    eposta = data.get('eposta')
    sifre = data.get('sifre')
    
    if not all([ad_soyad, kullanici_adi, eposta, sifre]):
        return jsonify({'success': False, 'message': 'Lütfen tüm alanları doldurun.'}), 400
        
    mevcut_kullanici = Kullanici.query.filter((Kullanici.eposta == eposta) | (Kullanici.kullanici_adi == kullanici_adi)).first()
    if mevcut_kullanici:
        return jsonify({'success': False, 'message': 'Bu e-posta veya kullanıcı adı zaten kullanımda.'}), 409
        
    hashed_sifre = generate_password_hash(sifre, method='pbkdf2:sha256')
    yeni_kullanici = Kullanici(
        ad_soyad=ad_soyad,
        kullanici_adi=kullanici_adi,
        eposta=eposta,
        dogum_tarihi="",
        sifre_hash=hashed_sifre,
        onayli_mi=True  # Mobil için otomatik onay
    )
    db.session.add(yeni_kullanici)
    db.session.commit()
    
    token = s.dumps({'kullanici_adi': kullanici_adi}, salt='mobil-api-token')
    return jsonify({'success': True, 'message': 'Kayıt başarılı.', 'token': token}), 201

@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Veri alınamadı.'}), 400
        
    kullanici_adi = data.get('kullanici_adi')
    sifre = data.get('sifre')
    
    kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
    if kullanici and check_password_hash(kullanici.sifre_hash, sifre):
        token = s.dumps({'kullanici_adi': kullanici.kullanici_adi}, salt='mobil-api-token')
        return jsonify({
            'success': True, 
            'token': token,
            'user': {
                'kullanici_adi': kullanici.kullanici_adi,
                'ad_soyad': kullanici.ad_soyad,
                'he_coin': kullanici.he_coin,
                'rutbe': kullanici.rutbe
            }
        }), 200
    
    return jsonify({'success': False, 'message': 'Kullanıcı adı veya şifre hatalı.'}), 401

@app.route('/api/user/profile', methods=['GET'])
def api_user_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'success': False, 'message': 'Token bulunamadı.'}), 401
        
    token = auth_header.split(' ')[1]
    try:
        data = s.loads(token, salt='mobil-api-token', max_age=86400 * 30) # 30 gün geçerli token
        kullanici_adi = data.get('kullanici_adi')
    except Exception:
        return jsonify({'success': False, 'message': 'Geçersiz veya süresi dolmuş token.'}), 401
        
    kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
    if not kullanici:
        return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı.'}), 404
        
    return jsonify({
        'success': True,
        'profile': {
            'ad_soyad': kullanici.ad_soyad,
            'kullanici_adi': kullanici.kullanici_adi,
            'he_coin': kullanici.he_coin,
            'rutbe': kullanici.rutbe,
            'cozulen_test_sayisi': kullanici.cozulen_test_sayisi,
            'profil_resmi': kullanici.profil_resmi
        }
    }), 200

@app.route('/api/games', methods=['GET'])
def api_games():
    oyunlar = Oyun.query.all()
    oyun_listesi = []
    for oyun in oyunlar:
        oyun_listesi.append({
            'id': oyun.id,
            'baslik': oyun.baslik,
            'kategori': oyun.kategori,
            'oyun_modu': oyun.oyun_modu,
            'oynanma_sayisi': oyun.oynanma_sayisi
        })
    return jsonify({'success': True, 'games': oyun_listesi}), 200

@app.route('/api/shop/items', methods=['GET'])
def api_shop_items():
    items = [
        {'id': 'cerceve_standart', 'name': 'Standart', 'price': 0, 'type': 'frame'},
        {'id': 'cerceve_siber', 'name': 'Siber Komuta', 'price': 500, 'type': 'frame'},
        {'id': 'unvan_korsan', 'name': 'Siber Korsan', 'price': 1000, 'type': 'title'}
    ]
    return jsonify({'success': True, 'items': items}), 200
# ==========================================
# 🚀 HANGISI (QUIZEI TARZI) TRIVIA SİSTEMİ
# ==========================================

@app.route('/hangisi')
def hangisi_panel():
    oyunlar = HangisiOyun.query.order_by(HangisiOyun.id.desc()).all()
    # Populate a dict with top 3 players for each game if needed
    liderler_dict = {}
    for o in oyunlar:
        top_skorlar = HangisiSkor.query.filter_by(oyun_id=o.id).order_by(HangisiSkor.puan.desc()).limit(3).all()
        liderler_dict[o.id] = [{'kullanici_adi': s.kullanici_adi, 'puan': s.puan} for s in top_skorlar]
        
    return render_template('hangisi_panel.html', oyunlar=oyunlar, liderler_dict=liderler_dict)

@app.route('/hangisi/<int:id>')
def hangisi_oyun_sayfasi(id):
    oyun = HangisiOyun.query.get_or_404(id)
    sorular = HangisiSoru.query.filter_by(oyun_id=id).all()
    
    # Leaderboard
    liderlik = HangisiSkor.query.filter_by(oyun_id=id).order_by(HangisiSkor.puan.desc()).limit(10).all()
    
    # Reactions stats
    tepkiler_raw = db.session.query(HangisiTepki.tepki, db.func.count(HangisiTepki.id)).filter_by(oyun_id=id).group_by(HangisiTepki.tepki).all()
    tepkiler = {t[0]: t[1] for t in tepkiler_raw}
    
    # Related Quizzes
    benzer_oyunlar = HangisiOyun.query.filter(HangisiOyun.id != id).order_by(db.func.random()).limit(4).all()
    
    # Convert sorular to list of dicts for JS
    soru_listesi = []
    for s in sorular:
        soru_listesi.append({
            'id': s.id,
            'soru_metni': s.soru_metni,
            'resim_url': s.resim_url,
            'secenek_a': s.secenek_a,
            'secenek_b': s.secenek_b,
            'secenek_c': s.secenek_c,
            'secenek_d': s.secenek_d,
            'dogru_cevap': s.dogru_cevap
        })
        
    kullanici_adi = session.get('kullanici_adi', '')
    
    return render_template('hangisi_oyun.html', 
                           oyun=oyun, 
                           sorular=soru_listesi, 
                           liderlik=liderlik, 
                           tepkiler=tepkiler, 
                           benzer_oyunlar=benzer_oyunlar,
                           kullanici_adi=kullanici_adi)

@app.route('/api/hangisi/skor_kaydet', methods=['POST'])
def hangisi_skor_kaydet():
    data = request.json
    try:
        oyun = HangisiOyun.query.get(data['oyun_id'])
        if oyun:
            oyun.oynanma_sayisi += 1
            
        yeni_skor = HangisiSkor(
            oyun_id=data['oyun_id'],
            kullanici_adi=data['kullanici_adi'],
            puan=int(data['puan'])
        )
        db.session.add(yeni_skor)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/hangisi/tepki', methods=['POST'])
def hangisi_tepki_ver():
    data = request.json
    try:
        # Check if already reacted
        mevcut = HangisiTepki.query.filter_by(
            oyun_id=data['oyun_id'], 
            kullanici_adi=data['kullanici_adi']
        ).first()
        
        if mevcut:
            mevcut.tepki = data['tepki'] # Update reaction
        else:
            yeni_tepki = HangisiTepki(
                oyun_id=data['oyun_id'],
                kullanici_adi=data['kullanici_adi'],
                tepki=data['tepki']
            )
            db.session.add(yeni_tepki)
            
        db.session.commit()
        
        # Return new counts
        tepkiler_raw = db.session.query(HangisiTepki.tepki, db.func.count(HangisiTepki.id)).filter_by(oyun_id=data['oyun_id']).group_by(HangisiTepki.tepki).all()
        tepkiler = {t[0]: t[1] for t in tepkiler_raw}
        
        return jsonify({'status': 'success', 'tepkiler': tepkiler})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/ads.txt')
def serve_ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/sitemap.xml')
def serve_sitemap_xml():
    return send_from_directory('static', 'sitemap.xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)