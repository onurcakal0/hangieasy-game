import os
import psycopg2
from dotenv import load_dotenv
import random

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT id FROM hangisi_oyun WHERE baslik LIKE '%Kim HE-Coin%' LIMIT 1")
row = cur.fetchone()
if not row:
    print("Oyun bulunamadı!")
    exit()

oyun_id = row[0]

# Delete old questions
cur.execute("DELETE FROM hangisi_soru WHERE oyun_id = %s", (oyun_id,))

kolay_sorular = [
    ("Türkiye'nin başkenti neresidir?", "Ankara", "İstanbul", "İzmir", "Bursa"),
    ("Alfabemizin ilk harfi nedir?", "A", "B", "C", "D"),
    ("Hangisi bir meyvedir?", "Elma", "Patates", "Havuç", "Kereviz"),
    ("Hangi renk trafik ışığında 'Dur' anlamına gelir?", "Kırmızı", "Yeşil", "Sarı", "Mavi"),
    ("Dünyaya en yakın yıldız hangisidir?", "Güneş", "Kutup Yıldızı", "Sirius", "Vega"),
    ("Bir haftada kaç gün vardır?", "7", "5", "6", "8"),
    ("Hangi hayvan 'Miyav' sesi çıkarır?", "Kedi", "Köpek", "Kuş", "İnek"),
    ("Futbol takımları sahada kaç kişi ile mücadele eder?", "11", "10", "12", "9"),
    ("Suyun formülü nedir?", "H2O", "CO2", "O2", "NaCl"),
    ("Türk bayrağının renkleri nelerdir?", "Kırmızı - Beyaz", "Siyah - Beyaz", "Sarı - Kırmızı", "Mavi - Beyaz"),
    ("Hangisi bir sosyal medya platformudur?", "Instagram", "Excel", "Word", "Photoshop"),
    ("Bir gün kaç saattir?", "24", "12", "48", "36"),
    ("İngilizcede 'Kırmızı' ne anlama gelir?", "Red", "Blue", "Green", "Yellow"),
    ("Yaz mevsiminden sonra hangi mevsim gelir?", "Sonbahar", "İlkbahar", "Kış", "Yaz"),
    ("Türkiye'nin en kalabalık şehri hangisidir?", "İstanbul", "Ankara", "İzmir", "Antalya")
]

orta_sorular = [
    ("Mona Lisa tablosu hangi ünlü ressama aittir?", "Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"),
    ("Hangi kıta hem Kuzey hem de Güney yarımkürede yer alır?", "Afrika", "Avrupa", "Kuzey Amerika", "Avustralya"),
    ("Mustafa Kemal Atatürk'ün doğum yeri olan Selanik, günümüzde hangi ülkededir?", "Yunanistan", "Bulgaristan", "Makedonya", "Arnavutluk"),
    ("Periyodik cetvelde O simgesiyle gösterilen element hangisidir?", "Oksijen", "Osmiyum", "Altın", "Karbon"),
    ("Nobel ödülleri hangi ülkede dağıtılmaktadır?", "İsveç", "Norveç", "İsviçre", "Danimarka"),
    ("İstiklal Marşı'mızın şairi kimdir?", "Mehmet Akif Ersoy", "Necip Fazıl Kısakürek", "Cemal Süreya", "Nazım Hikmet"),
    ("Dünyanın en yüksek dağı hangisidir?", "Everest", "K2", "Ağrı Dağı", "Alpler"),
    ("Telefonu icat eden kişi kimdir?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Guglielmo Marconi"),
    ("Türkiye hangi kıtalarda toprak sahibidir?", "Avrupa - Asya", "Asya - Afrika", "Avrupa - Afrika", "Asya - Avustralya"),
    ("Japonya'nın başkenti neresidir?", "Tokyo", "Pekin", "Seul", "Kyoto"),
    ("Eiffel Kulesi hangi şehirdedir?", "Paris", "Londra", "Berlin", "Roma"),
    ("Osmanlı İmparatorluğu'nun kurucusu kimdir?", "Osman Gazi", "Orhan Gazi", "Fatih Sultan Mehmet", "Yavuz Sultan Selim"),
    ("Işık hızı saniyede yaklaşık kaç kilometredir?", "300.000", "150.000", "1.000.000", "3.000"),
    ("Harry Potter serisinin yazarı kimdir?", "J.K. Rowling", "Stephen King", "J.R.R. Tolkien", "George R.R. Martin"),
    ("Hangi gezegen 'Kızıl Gezegen' olarak bilinir?", "Mars", "Jüpiter", "Venüs", "Satürn")
]

zor_sorular = [
    ("Kıbrıs Barış Harekatı hangi yıl gerçekleşmiştir?", "1974", "1960", "1983", "1954"),
    ("Dünyanın en uzun akarsuyu hangisidir?", "Nil", "Amazon", "Yangtze", "Mississippi"),
    ("Tarihte bilinen ilk yazılı antlaşma olan Kadeş Antlaşması hangi devletler arasındadır?", "Mısırlılar - Hititler", "Sümerler - Akadlar", "Romalılar - Kartacalılar", "Persler - Yunanlar"),
    ("Romen rakamlarında 'L' harfi hangi sayıyı ifade eder?", "50", "100", "500", "1000"),
    ("Nobel Edebiyat Ödülü alan ilk Türk yazar kimdir?", "Orhan Pamuk", "Yaşar Kemal", "Sabahattin Ali", "Aziz Nesin"),
    ("Göbeklitepe hangi şehrimizde bulunmaktadır?", "Şanlıurfa", "Gaziantep", "Mardin", "Diyarbakır"),
    ("Fatih Sultan Mehmet İstanbul'u fethettiğinde kaç yaşındaydı?", "21", "19", "25", "23"),
    ("Satranç tahtasında toplam kaç kare vardır?", "64", "32", "128", "100"),
    ("Birleşmiş Milletler'in merkezi nerededir?", "New York", "Cenevre", "Brüksel", "Washington"),
    ("İnsan vücudundaki en küçük kemik nerededir?", "Kulak", "Burun", "Ayak parmağı", "Serçe parmağı"),
    ("DNA molekülünün yapısını çözen bilim insanları kimlerdir?", "Watson - Crick", "Newton - Einstein", "Curie - Bohr", "Edison - Tesla"),
    ("Picasso'nun İspanya İç Savaşı'nı anlattığı meşhur tablosunun adı nedir?", "Guernica", "Çığlık", "Yıldızlı Gece", "Belleğin Azmi"),
    ("Güneş sistemindeki en büyük gezegen hangisidir?", "Jüpiter", "Satürn", "Uranüs", "Neptün"),
    ("Kutup ayılarının derisi ne renktir?", "Siyah", "Beyaz", "Pembe", "Mavi"),
    ("İlk bilgisayar programcısı olarak kabul edilen kişi kimdir?", "Ada Lovelace", "Alan Turing", "Charles Babbage", "Bill Gates"),
    ("Osmanlı Devleti'nde ilk matbaayı kim kurmuştur?", "İbrahim Müteferrika", "Katip Çelebi", "Evliya Çelebi", "Hezarfen Ahmet Çelebi"),
    ("Periyodik tablonun mucidi kimdir?", "Dmitri Mendeleyev", "Marie Curie", "Albert Einstein", "Niels Bohr"),
    ("Dünyanın en büyük çölü hangisidir?", "Antarktika", "Sahra", "Gobi", "Kalahari"),
    ("Mimar Sinan'ın 'Ustalık eserim' dediği cami hangisidir?", "Selimiye", "Süleymaniye", "Şehzade", "Sultanahmet"),
    ("Bir zürafanın boynunda kaç adet kemik vardır?", "7", "12", "20", "3"),
    ("Dünyada en çok konuşulan ana dil hangisidir?", "Mandarin Çincesi", "İngilizce", "İspanyolca", "Hintçe"),
    ("Modern olimpiyatların ilki hangi yıl düzenlenmiştir?", "1896", "1900", "1924", "1888"),
    ("Machu Picchu antik şehri hangi ülkededir?", "Peru", "Brezilya", "Meksika", "Şili"),
    ("Uzaya çıkan ilk insan kimdir?", "Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "Laika"),
    ("Bir üçgenin iç açıları toplamı kaç derecedir?", "180", "360", "90", "270"),
    ("İzafiyet Teorisi'ni kim ortaya atmıştır?", "Albert Einstein", "Isaac Newton", "Stephen Hawking", "Galileo Galilei"),
    ("Aspirinin etken maddesi nedir?", "Asetilsalisilik asit", "Parasetamol", "İbuprofen", "Penisilin"),
    ("Türk edebiyatında ilk yerli roman hangisidir?", "Taaşşuk-ı Talat ve Fitnat", "İntibah", "Araba Sevdası", "Mai ve Siyah"),
    ("Hangi elementin simgesi 'Au'dur?", "Altın", "Gümüş", "Bakır", "Alüminyum"),
    ("Kuduz aşısını kim bulmuştur?", "Louis Pasteur", "Alexander Fleming", "Edward Jenner", "Jonas Salk")
]

def insert_pool(soru_listesi, zorluk):
    for q in soru_listesi:
        soru_metni = q[0]
        secenekler = [q[1], q[2], q[3], q[4]]
        dogru_cevap = q[1]
        random.shuffle(secenekler)
        dogru_harf = "A" if secenekler[0] == dogru_cevap else "B" if secenekler[1] == dogru_cevap else "C" if secenekler[2] == dogru_cevap else "D"
        cur.execute('''
            INSERT INTO hangisi_soru (oyun_id, soru_metni, secenek_a, secenek_b, secenek_c, secenek_d, dogru_cevap, zorluk_derecesi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (oyun_id, soru_metni, secenekler[0], secenekler[1], secenekler[2], secenekler[3], dogru_harf, zorluk))

insert_pool(kolay_sorular, "Kolay")
insert_pool(orta_sorular, "Orta")
insert_pool(zor_sorular, "Zor")

conn.commit()
cur.close()
conn.close()
print("Soru havuzu başarıyla yüklendi: Toplam 60 soru (15 Kolay, 15 Orta, 30 Zor)")
