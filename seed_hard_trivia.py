import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Create the Game
cur.execute('''
    INSERT INTO oyun (baslik, aciklama, resim_url, kategori, oyun_modu, oynanma_sayisi) 
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
''', (
    "Sınırları Zorlayan Genel Kültür", 
    "İnternetten bakmadan 10'da 10 yapabilenin alnından öpüleceği, beynini yakacak kadar zorlayıcı seçkin genel kültür testi.",
    "/static/img/games/hard_trivia_cover.png",
    "Genel Kültür",
    "klasik_test",
    0
))
oyun_id = cur.fetchone()[0]

sorular = [
    {
        "soru_metni": "Tarihte bilinen ilk yazılı antlaşma olan Kadeş Antlaşması, hangi iki uygarlık arasında imzalanmıştır?",
        "secenekler": "Sümerler - Akadlar,Mısırlılar - Hititler,Babiller - Asurlar,Lidyalılar - Persler",
        "dogru_cevap": "Mısırlılar - Hititler"
    },
    {
        "soru_metni": "Periyodik tablodaki 'W' sembolü hangi elemente aittir?",
        "secenekler": "Tungsten,Platin,Antimon,Stronsiyum",
        "dogru_cevap": "Tungsten"
    },
    {
        "soru_metni": "İnsan vücudundaki en küçük kemik olan 'üzengi kemiği' (stapes) nerede bulunur?",
        "secenekler": "El bileği,Burun,Orta kulak,Ayak parmağı",
        "dogru_cevap": "Orta kulak"
    },
    {
        "soru_metni": "Edebiyat tarihinin en uzun romanı olarak bilinen ve 7 cilt, yaklaşık 1.2 milyon kelimeden oluşan 'Kayıp Zamanın İzinde' adlı eserin yazarı kimdir?",
        "secenekler": "James Joyce,Marcel Proust,Leo Tolstoy,Victor Hugo",
        "dogru_cevap": "Marcel Proust"
    },
    {
        "soru_metni": "Güneş sistemindeki en sıcak gezegen hangisidir?",
        "secenekler": "Merkür,Venüs,Mars,Jüpiter",
        "dogru_cevap": "Venüs"
    },
    {
        "soru_metni": "1911 yılında Mona Lisa tablosunu Louvre Müzesi'nden çalan İtalyan hırsız kimdir?",
        "secenekler": "Vincenzo Peruggia,Leonardo Notarbartolo,Albert Spaggiari,Stephane Breitwieser",
        "dogru_cevap": "Vincenzo Peruggia"
    },
    {
        "soru_metni": "Matematikte 'Altın Oran' hangi Yunan harfi ile ifade edilir?",
        "secenekler": "Pi (π),Sigma (Σ),Fi (Φ),Delta (Δ)",
        "dogru_cevap": "Fi (Φ)"
    },
    {
        "soru_metni": "Dünya üzerinde aynı anda hem Ekvator'dan hem de Başlangıç Meridyeni'nden (Greenwich) geçen tek kıta hangisidir?",
        "secenekler": "Asya,Güney Amerika,Afrika,Avrupa",
        "dogru_cevap": "Afrika"
    },
    {
        "soru_metni": "Felsefede 'Cogito, ergo sum' (Düşünüyorum, öyleyse varım) sözü hangi filozofa aittir?",
        "secenekler": "Immanuel Kant,Friedrich Nietzsche,René Descartes,Sokrates",
        "dogru_cevap": "René Descartes"
    },
    {
        "soru_metni": "Okyanusların en derin noktası olan Mariana Çukuru'nun en dibine verilen isim nedir?",
        "secenekler": "Challenger Çukuru,Sirena Derinliği,Horizon Noktası,Hades Bölgesi",
        "dogru_cevap": "Challenger Çukuru"
    }
]

for s in sorular:
    cur.execute('''
        INSERT INTO soru (oyun_id, resim_url, secenekler, dogru_cevap)
        VALUES (%s, %s, %s, %s)
    ''', (oyun_id, s["soru_metni"], s["secenekler"], s["dogru_cevap"]))

conn.commit()
cur.close()
conn.close()
print("Sınırları Zorlayan Genel Kültür testi başarıyla eklendi!")
