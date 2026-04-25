from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Oturumların (login) güvenliği için gizli bir anahtar şarttır!
app.secret_key = "edux_gizli_anahtar_cto"

# --- VERİTABANI AYARLARI ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edux_v4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)

# 1. Tablo: Skorlar
class SkorTablosu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(50), nullable=False)
    skor = db.Column(db.Integer, nullable=False)

# 2. Tablo: KULLANICILAR 
class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(50), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(200), nullable=False)

# 3. Tablo: OYUNLAR 
class Oyun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.String(200))
    resim_url = db.Column(db.String(300))
    kategori = db.Column(db.String(50))
    oyun_modu = db.Column(db.String(50), nullable=False, default='normal') 
    olusturan_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'))
    sorular = db.relationship('Soru', backref='oyun', lazy=True)

# 4. Tablo: SORULAR 
class Soru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oyun_id = db.Column(db.Integer, db.ForeignKey('oyun.id'), nullable=False)
    resim_url = db.Column(db.String(300)) 
    resim_url_2 = db.Column(db.String(300), nullable=True) 
    secenekler = db.Column(db.String(500))
    dogru_cevap = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# --- ÜYELİK SİSTEMİ (AUTH) ROTALARI ---

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        kadi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        
        mevcut_kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
        if mevcut_kullanici:
            return "Bu kullanıcı adı alınmış patron, başka bir tane dene!"
            
        yeni_kullanici = Kullanici(kullanici_adi=kadi, sifre_hash=generate_password_hash(sifre))
        db.session.add(yeni_kullanici)
        db.session.commit()
        return redirect(url_for('giris'))
        
    return render_template('kayit.html')

@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        kadi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        
        kullanici = Kullanici.query.filter_by(kullanici_adi=kadi).first()
        if kullanici and check_password_hash(kullanici.sifre_hash, sifre):
            session['kullanici_adi'] = kullanici.kullanici_adi 
            return redirect(url_for('dashboard'))
        else:
            return "Hatalı şifre veya kullanıcı adı!"
            
    return render_template('giris.html')

@app.route('/cikis')
def cikis():
    session.pop('kullanici_adi', None) 
    return redirect(url_for('dashboard'))

# --- MEVCUT OYUN ROTALARI ---

@app.route('/')
def dashboard():
    tum_oyunlar = Oyun.query.all()
    return render_template('dashboard.html', oyunlar=tum_oyunlar)

@app.route('/test-olustur', methods=['GET', 'POST'])
def test_olustur():
    if 'kullanici_adi' not in session:
        return redirect(url_for('giris'))
        
    if request.method == 'POST':
        aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
        
        if not aktif_kullanici:
            session.pop('kullanici_adi', None)
            return redirect(url_for('giris'))
            
        kapak_dosyasi = request.files['kapak_resmi']
        kapak_isim = secure_filename(kapak_dosyasi.filename)
        kapak_yolu = os.path.join(app.config['UPLOAD_FOLDER'], kapak_isim)
        kapak_dosyasi.save(kapak_yolu)
        
        secilen_mod = request.form['oyun_modu']
        
        yeni_oyun = Oyun(
            baslik=request.form['baslik'],
            aciklama=request.form['aciklama'],
            resim_url="/" + kapak_yolu,
            kategori=request.form['kategori'],
            oyun_modu=secilen_mod,
            olusturan_id=aktif_kullanici.id
        )
        db.session.add(yeni_oyun)
        db.session.commit()
        
        return redirect(url_for('soru_ekle', oyun_id=yeni_oyun.id))
        
    return render_template('test_olustur.html')

@app.route('/soru-ekle/<int:oyun_id>', methods=['GET', 'POST'])
def soru_ekle(oyun_id):
    if 'kullanici_adi' not in session: return redirect(url_for('giris'))
    secilen_oyun = Oyun.query.get_or_404(oyun_id)
    
    if request.method == 'POST':
        # 1. DURUM: O MU BU MU MODU
        if secilen_oyun.oyun_modu == 'omu_bumu':
            dosya1 = request.files['resim_1']
            dosya2 = request.files['resim_2']
            yol1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(dosya1.filename))
            yol2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(dosya2.filename))
            dosya1.save(yol1)
            dosya2.save(yol2)
            
            yeni_soru = Soru(
                oyun_id=secilen_oyun.id,
                resim_url="/" + yol1,
                resim_url_2="/" + yol2,
                secenekler=request.form['secenek_1'] + "," + request.form['secenek_2'],
                dogru_cevap=request.form['dogru_cevap']
            )
            db.session.add(yeni_soru)

        # 2. DURUM: KÖR SIRALAMA VEYA TURNUVA
        elif secilen_oyun.oyun_modu in ['kor_siralama', 'turnuva']:
            resimler = request.files.getlist('soru_resmi') 
            isimler = request.form.getlist('secenekler')   
            
            for i in range(len(resimler)):
                dosya = resimler[i]
                if dosya.filename == '': continue 
                isim = isimler[i]
                
                yol = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(dosya.filename))
                dosya.save(yol)
                
                yeni_soru = Soru(
                    oyun_id=secilen_oyun.id,
                    resim_url="/" + yol,
                    secenekler=isim,
                    dogru_cevap="Farketmez"
                )
                db.session.add(yeni_soru)

        # 3. DURUM: NORMAL TEST
        else:
            soru_dosyasi = request.files['soru_resmi']
            soru_yolu = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(soru_dosyasi.filename))
            soru_dosyasi.save(soru_yolu)
            
            yeni_soru = Soru(
                oyun_id=secilen_oyun.id,
                resim_url="/" + soru_yolu,
                secenekler=request.form['secenekler'],
                dogru_cevap=request.form['dogru_cevap']
            )
            db.session.add(yeni_soru)
            
        db.session.commit() 
        
        if request.form['aksiyon'] == 'devam': 
            return redirect(url_for('soru_ekle', oyun_id=secilen_oyun.id))
        else: 
            return redirect(url_for('dashboard'))
            
    mevcut_soru_sayisi = Soru.query.filter_by(oyun_id=secilen_oyun.id).count()
    return render_template('soru_ekle.html', oyun=secilen_oyun, soru_sayisi=mevcut_soru_sayisi + 1)

@app.route('/oyun/<int:oyun_id>')
def oyun_sayfasi(oyun_id):
    secilen_oyun = Oyun.query.get_or_404(oyun_id)
    
    if secilen_oyun.oyun_modu == 'omu_bumu':
        return render_template('omu_bumu.html', aktif_oyun=oyun_id, oyun_basligi=secilen_oyun.baslik)
    elif secilen_oyun.oyun_modu == 'kor_siralama':
        return render_template('kor_siralama.html', aktif_oyun=oyun_id, oyun_basligi=secilen_oyun.baslik)
    elif secilen_oyun.oyun_modu == 'turnuva':
        return render_template('turnuva.html', aktif_oyun=oyun_id, oyun_basligi=secilen_oyun.baslik)
        
    return render_template('index.html', aktif_oyun=oyun_id, oyun_basligi=secilen_oyun.baslik)

@app.route('/api/sorular/<int:oyun_id>')
def sorulari_getir(oyun_id):
    oyunun_sorulari = Soru.query.filter_by(oyun_id=oyun_id).all()
    soru_listesi = []
    for soru in oyunun_sorulari:
        soru_listesi.append({
            "resim": soru.resim_url,
            "resim_2": soru.resim_url_2, 
            "secenekler": soru.secenekler.split(','),
            "dogru_cevap": soru.dogru_cevap
        })
    return jsonify(soru_listesi)
# --- İÇERİK ÜRETİCİSİ STÜDYOSU (PROFİL) ---
@app.route('/profil')
def profil():
    # Giriş yapılmadıysa kapıdan çevir
    if 'kullanici_adi' not in session:
        return redirect(url_for('giris'))
    
    aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    if not aktif_kullanici:
        session.pop('kullanici_adi', None)
        return redirect(url_for('giris'))
        
    # Veritabanından SADECE BU KULLANICININ ürettiği oyunları çek (Krallık arşivi)
    kullanicinin_oyunlari = Oyun.query.filter_by(olusturan_id=aktif_kullanici.id).all()
    
    return render_template('profil.html', oyunlar=kullanicinin_oyunlari, kullanici=aktif_kullanici)

@app.route('/oyun-sil/<int:oyun_id>', methods=['POST'])
def oyun_sil(oyun_id):
    if 'kullanici_adi' not in session: return redirect(url_for('giris'))
        
    aktif_kullanici = Kullanici.query.filter_by(kullanici_adi=session['kullanici_adi']).first()
    silinecek_oyun = Oyun.query.get_or_404(oyun_id)
    
    # GÜVENLİK DUVARI: Hackerlar URL değiştirip başkasının testini silemesin!
    if silinecek_oyun.olusturan_id != aktif_kullanici.id:
        return "Hop! Burası senin krallığın değil patron.", 403
        
    # 1. Önce bu oyuna ait tüm soruları veritabanından temizle
    Soru.query.filter_by(oyun_id=silinecek_oyun.id).delete()
    
    # 2. Sonra oyunun kendisini sil
    db.session.delete(silinecek_oyun)
    db.session.commit()
    
    # Stüdyoya geri dön
    return redirect(url_for('profil'))
if __name__ == '__main__':
    app.run(debug=True, port=5001)