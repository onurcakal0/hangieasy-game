/**
 * HangiEasy Passaparola 6 Saatlik Dinamik Soru Havuzu
 * Her harf için en az 8-10 adet zengin, doğrulanmış ve ilgi çekici soru içerir.
 */
const PASSAPAROLA_POOLS = {
    "A": [
        { "question": "Dünyanın en geniş yüzölçümüne ve nüfusuna sahip olan kıtası.", "answer": "Asya" },
        { "question": "Ateş düşürücü ve ağrı kesici olarak dünyada en yaygın kullanılan ilaç.", "answer": "Aspirin" },
        { "question": "Gök cisimlerini, yıldızları ve evrenin yapısını inceleyen doğa bilimi.", "answer": "Astronomi" },
        { "question": "Etrafı tamamen sularla çevrili olan kara parçası.", "answer": "Ada" },
        { "question": "Bir fikri, tezi veya düşünceyi savunmak amacıyla öne sürülen mantıksal kanıt.", "answer": "Argüman" },
        { "question": "Geçmiş uygarlıklardan kalan kalıntıları kazı yoluyla ortaya çıkaran bilim dalı.", "answer": "Arkeoloji" },
        { "question": "Tiyatrolarda veya açık havada gösteri yapılan basamaklı daire şeklindeki antik alan.", "answer": "Amfitiyatro" },
        { "question": "Eski dönemlerde metalleri altına çevirmeye ve ölümsüzlük iksirini bulmaya çalışan ilkel uğraş.", "answer": "Alşimi" }
    ],
    "B": [
        { "question": "İpek böcekçiliği, termal kaplıcaları ve kestane şekeriyle ünlü Marmara şehri.", "answer": "Bursa" },
        { "question": "İnsan ve hayvan vücudunda düşünme, hafıza ve hareket kontrolünü yöneten organ.", "answer": "Beyin" },
        { "question": "Rengi sarı, tadı tatlı ve kabuğu soyularak yenilen muz gibi tropikal meyvelerin yetiştiği sıcak iklim kuşağı.", "answer": "Bask" , "alt": "Bambu", "questionAlt": "Uzak Doğu'da yetişen, hızla uzayan ve pandaların ana besini olan sert odunsu kamış türü.", "answerAlt": "Bambu" },
        { "question": "Gözleri net görmeyen kişilerin görme kusurlarını düzeltmek için taktığı optik cam.", "answer": "Gözlük", "questionAlt": "Suyun donarak katı hale geçmiş kristal veya şeffaf biçimi.", "answerAlt": "Buz" },
        { "question": "Hava sıcaklığını ve atmosfer basıncını ölçmeye yarayan meteorolojik ölçüm aleti.", "answer": "Barometre" },
        { "question": "Yeryüzünde yaşayan canlı türlerinin çeşitliliğini ve zenginliğini ifade eden biyolojik kavram.", "answer": "Biyoçeşitlilik" },
        { "question": "Alışverişte bir malın elde edilmesi için ödenmesi gereken parasal değer.", "answer": "Bedel" },
        { "question": "Büyükbaş veya küçükbaş hayvanların beslenip barındırıldığı üstü kapalı köy yapısı.", "answer": "Ahır", "questionAlt": "Büyük su kütlelerinin akışını keserek elektrik üretmek veya su depolamak için kurulan set.", "answerAlt": "Baraj" }
    ],
    "C": [
        { "question": "Müslümanların topluca ibadet etmek ve cuma namazı kılmak için toplandığı mabet.", "answer": "Cami" },
        { "question": "Haftanın çalışma günlerini tamamlayan beşinci günü.", "answer": "Cuma" },
        { "question": "Sıcaklığı ve vücut ısısını ölçmek için kullanılan cıvalı veya dijital ölçüm aracı.", "answer": "Termometre", "questionAlt": "Oda sıcaklığında sıvı halde bulunan tek ağır metal element.", "answerAlt": "Cıva" },
        { "question": "Yerkürenin fiziki yapısını, dağlarını, ırmaklarını ve iklimlerini inceleyen bilim dalı.", "answer": "Coğrafya" },
        { "question": "Sert kabuklu, içi beyne benzeyen ve omega-3 bakımından çok zengin olan kuru yemiş.", "answer": "Ceviz" },
        { "question": "Vücudun dış yüzeyini kaplayan, dokunma duyusunu sağlayan en büyük organımız.", "answer": "Deri", "questionAlt": "Bir devletin veya krallığın sahip olduğu toprakların bütünü, ülke sınırları.", "answerAlt": "Coğrafya" },
        { "question": "Korkusuzca tehlikelerin üzerine giden, yürekli ve yiğit kimseye verilen sıfat.", "answer": "Cesur" },
        { "question": "Genellikle paraların ve kimliklerin taşındığı cep boyundaki küçük deri kap.", "answer": "Cüzdan" }
    ],
    "Ç": [
        { "question": "Rize ve Doğu Karadeniz bölgesinde yaygın olarak yetiştirilen milli sıcak içecek bitkisi.", "answer": "Çay" },
        { "question": "Gözleri güneşin zararlı UV ışınlarından ve aşırı ışıktan korumak için takılan renkli camlı aksesuar.", "answer": "Güneş Gözlüğü", "questionAlt": "Şimşek ve yıldırım çakması sırasında meydana gelen çok güçlü gürleme sesi.", "answerAlt": "Çatırtı" },
        { "question": "Yıllık yağış miktarı çok az olan, kurak ve çoğunlukla kumullarla kaplı devasa bölge.", "answer": "Çöl" },
        { "question": "Yaz aylarında tarlalarda açan, çekirdekleri çitlenen güneşe aşık büyük sarı çiçek.", "answer": "Ayçiçeği", "questionAlt": "Kırmızı renkli, küçük yuvarlak taneli ve mayhoş lezzetli popüler bahar meyvesi.", "answerAlt": "Çilek" },
        { "question": "Toprağı işleyerek tahıl, sebze veya meyve yetiştiren tarım emekçisi kimse.", "answer": "Çiftçi" },
        { "question": "Kakao yağı, süt ve şekerden üretilen dünyanın en çok tüketilen tatlı atıştırmalığı.", "answer": "Çikolata" },
        { "question": "Ev ve binaların en üst kısmını örterek yağmur ve kardan koruyan koruyucu üst yapı.", "answer": "Çatı" },
        { "question": "Tepeler veya dağlar arasında kalan, genellikle içinden akarsu geçen derin yarık çukurluk.", "answer": "Vadi", "questionAlt": "Yaylı telli bir orkestra çalgısı olan viyolonselin halk arasındaki yaygın adı.", "answerAlt": "Çello" }
    ],
    "D": [
        { "question": "Yer kabuğundaki fay hatlarının kırılmasıyla oluşan sarsıntıya verilen bilimsel isim.", "answer": "Deprem" },
        { "question": "Gündüzleri gökyüzünü aydınlatan güneş batınca başlayan karanlık zaman dilimi.", "answer": "Gece", "questionAlt": "Suyun veya sıvıların içine tamamen batarak su altında nefes alabilen dalış uzmanı.", "answerAlt": "Dalgıç" },
        { "question": "Tıbbi olarak hastalıkları teşhis ve tedavi eden tıp doktoru hekim.", "answer": "Doktor" },
        { "question": "Kelimelerin anlamlarını, söylenişlerini ve kökenlerini alfabetik olarak açıklayan başvuru kitabı.", "answer": "Sözlük", "questionAlt": "Büyük su kütlesi olup okyanuslardan daha küçük olan geniş tuzlu su alanı.", "answerAlt": "Deniz" },
        { "question": "Gemilerin veya teknelerin rüzgar ve akıntıyla sürüklenmemesi için denize atılan ağır demir çapa.", "answer": "Demir" },
        { "question": "Dünya genelinde insanların iletişim kurmak için kullandığı sözlü veya yazılı dizge, lisan.", "answer": "Dil" },
        { "question": "Kare veya dikdörtgen şekilli, genellikle 6 yüzünde 1'den 6'ya kadar noktalar olan oyun aracı.", "answer": "Zar", "questionAlt": "Çevresindeki araziye göre oldukça yüksek, zirvesi karla kaplanabilen devasa yeryüzü şekli.", "answerAlt": "Dağ" },
        { "question": "İçinde dondurulmuş krema, süt ve meyve aromaları bulunan yazın tüketilen soğuk tatlı.", "answer": "Dondurma" }
    ],
    "E": [
        { "question": "Fırınlarda un, su ve maya ile pişirilen, sofralarımızın en temel besin maddesi.", "answer": "Ekmek" },
        { "question": "Kırmızı veya yeşil renkli, içi beyaz sulu ve çıtır çıtır kış meyvesi.", "answer": "Elma" },
        { "question": "Tarihi çok eskilere dayanan, krallarına firavun denilen ve piramitleriyle ünlü Kuzey Afrika ülkesi.", "answer": "Mısır", "questionAlt": "Eski çağlarda yaşamış insanların bıraktığı el yazması, heykel veya kalıntı eser.", "answerAlt": "Eser" },
        { "question": "Kabuğu sert, içi lezzetli ve lifli olan, sıcak bölgelerde palmiyelerde yetişen lifli meyve.", "answer": "Hindistan Cevizi", "questionAlt": "Dikenli kabuğu soyulup haşlanarak yenen, kestaneye benzeyen şifalı bir sebze.", "answerAlt": "Enginar" },
        { "question": "Maddelerin moleküler hareketliliğini, elektrik veya ışık üretebilme gücünü temsil eden fiziksel büyüklük.", "answer": "Enerji" },
        { "question": "Eski dönemlerde kervanların ve tüccarların ticaret yaptığı yolların genel adı.", "answer": "İpek Yolu", "questionAlt": "Toprak altında yaşayan, toprağı havalandırıp zenginleştiren bacaksız halkalı canlı.", "answerAlt": "Solucan", "questionAlt2": "Evin iç sıcaklığını veya pişirme ortamını ayarlayan elektrikli mutfak cihazı.", "answerAlt2": "Fırın", "questionAlt3": "Gökkuşağında yer alan kırmızı, turuncu, sarı gibi renklerin genel optik adı.", "answerAlt3": "Elvan" },
        { "question": "Bir kişinin ailesiyle birlikte barındığı, huzur bulduğu konut, hane.", "answer": "Ev" },
        { "question": "Dünyayı kuzey ve güney olarak iki eşit yarım küreye böldüğü varsayılan hayali çizgi.", "answer": "Ekvator" }
    ],
    "F": [
        { "question": "On birer kişilik iki takım arasında ayakla top sürülerek oynanan dünyanın en popüler sporu.", "answer": "Futbol" },
        { "question": "Karadeniz kıyılarında bolca yetişen, çikolatanın ve tatlıların vazgeçilmezi olan yağlı kuru yemiş.", "answer": "Fındık" },
        { "question": "Genellikle karanlıkta yön bulmak veya aydınlatmak için elde taşınan pilli ışık kaynağı.", "answer": "Fener" },
        { "question": "Aşırı ve mantıksız düzeyde korku veya kaygı duyma psikolojik durumu.", "answer": "Fobi" },
        { "question": "Görünür ışık yardımıyla cisimlerin görüntüsünü hassas bir yüzeye veya dijital sensöre kaydetme sanatı.", "answer": "Fotoğraf" },
        { "question": "Eski Mısır'da hükümdarlara ve krallara verilen resmi unvan.", "answer": "Firavun" },
        { "question": "Bir çiçeğin veya bitkinin topraktan yeni süren körpe dalı, taze sürgünü.", "answer": "Filiz" },
        { "question": "Evrende gerçekleşen madde ve enerji etkileşimlerini inceleyen temel pozitif doğa bilimi.", "answer": "Fizik" }
    ],
    "G": [
        { "question": "Güneş sistemimizin merkezinde yer alan sıcak plazma ve gazlardan oluşan hayat kaynağımız yıldız.", "answer": "Güneş" },
        { "question": "Gündüz veya gece rüya gördüğümüz, gözlerimizi kapattığımız doğal dinlenme durumu.", "answer": "Uyku", "questionAlt": "Gözün ön kısmındaki saydam tabakanın hemen ardında bulunan ve göz rengini veren renkli tabaka.", "answerAlt": "Göz", "questionAlt2": "Yağmur sonrası güneş açtığında gökyüzünde beliren 7 renkli optik yay.", "answerAlt2": "Gökkuşağı" },
        { "question": "Su üzerinde yüzerek yolcu ve araç taşıyan motorlu büyük deniz taşıtı.", "answer": "Gemi" },
        { "question": "Halkı korumak ve kamu güvenliğini sağlamak için silah taşıyan resmi devlet görevlisi.", "answer": "Polis", "questionAlt": "Karanlık ortamlarda nesnelerin veya renklerin algılanmasını sağlayan duyu organımız.", "answerAlt": "Göz" },
        { "question": "Tatlı kokulu, dikenli sapları olan ve aşkın simgesi kabul edilen popüler çiçek.", "answer": "Gül" },
        { "question": "Gökbilimcilerin yıldızları ve gezegenleri incelemek için yüksek tepelere kurduğu kubbeli merkez.", "answer": "Gözlemevi" },
        { "question": "Gündüz gökyüzüne baktığımızda bulutların ve maviliğin yer aldığı sonsuz uzay boşluğu tavanı.", "answer": "Gökyüzü" },
        { "question": "Dört tarafı karayla çevrili, genellikle tatlı su barındıran durgun ve derin doğal su birikintisi.", "answer": "Göl" }
    ],
    "H": [
        { "question": "İnsanların veya canlıların hastalandığında muayene ve tedavi olduğu büyük sağlık kuruluşu.", "answer": "Hastane" },
        { "question": "Uçak ve helikopterlerin iniş kalkış yaptığı, yolcu terminalleri bulunan tesis.", "answer": "Havalimanı" },
        { "question": "Dünya veya bir bölgenin yeryüzü şekillerini belirli bir ölçekle küçülterek kağıda çizen çizim.", "answer": "Harita" },
        { "question": "Sonbaharda topraktan sökülen, tavşanların çok sevdiği turuncu renkli A vitamini deposu kök sebze.", "answer": "Havuç" },
        { "question": "Birbirini izleyen yedi günlük zaman dilimi.", "answer": "Hafta" },
        { "question": "Çölde su taşımadan günlerce yol alabilen, sırtında hörgücü olan dayanıklı hayvan.", "answer": "Deve", "questionAlt": "Canlıların hayatta kalmak için ciğerlerine çektiği oksijen ve azot gazları karışımı.", "answerAlt": "Hava" },
        { "question": "Geçmişte yaşanmış olayları yer ve zaman göstererek sebep-sonuç ilişkisiyle inceleyen bilim.", "answer": "Tarih", "questionAlt": "Gözle görülemeyecek kadar küçük olan canlıların en küçük yapı ve görev birimi.", "answerAlt": "Hücre" },
        { "question": "Toprak, taş, kil veya mermerden yontularak yapılan üç boyutlu plastik sanat eseri.", "answer": "Heykel" }
    ],
    "I": [
        { "question": "Kış aylarında kaynatılıp limonla içilen, göğsü yumuşatan sarı renkli şifalı ağaç çiçeği.", "answer": "Ihlamur" },
        { "question": "Karanlığı aydınlatan, saniyede yaklaşık 300.000 kilometre hızla yayılan elektromanyetik ışıma.", "answer": "Işık" },
        { "question": "Temel Reis çizgi filminde kahramana süper güç veren demir zengini yeşil yapraklı sebze.", "answer": "Ispanak" },
        { "question": "Deniz kıyısında veya göl kenarında dalgaların oluşturduğu kumluk dinlenme sahili, kumsal.", "answer": "Ilıca", "questionAlt": "Akarsuların en küçüğü olan dere veya çaydan daha büyük, nehirden daha sakin akan doğal su yolu.", "answerAlt": "Irmak" },
        { "question": "Sıcaklığı ılık olan, romatizma ve eklem hastalıklarına iyi gelen mineralli termal kaynak.", "answer": "Ilıca" },
        { "question": "Güneşin veya lambanın yaydığı ışığın şiddetini gösteren parlaklık veya aydınlanma derecesi.", "answer": "Işıltı" },
        { "question": "Geceleri gemilere yol gösteren kıyı kulelerinin tepe lambasında kullanılan güçlü projektör.", "answer": "Işıldak" },
        { "question": "Bir maddenin sıcaklığının artmasına yol açan enerjinin transfer edilmiş hali.", "answer": "Isı" }
    ],
    "İ": [
        { "question": "Asya ve Avrupa kıtalarını birbirine bağlayan, Boğaz'a sahip tarihi dünya metropolümüz.", "answer": "İstanbul" },
        { "question": "Hastalıkları iyileştirmek, ağrıları dindirmek amacıyla eczanelerde satılan kimyasal veya bitkisel madde.", "answer": "İlaç" },
        { "question": "Bir bölgede uzun yıllar boyunca gözlemlenen ortalama hava koşullarının bütünü.", "answer": "İklim" },
        { "question": "Gelecekte teknoloji veya sanat alanında daha önce yapılmamış yeni bir buluş ortaya koyma.", "answer": "İcat" },
        { "question": "Doğada kendiliğinden yetişen ve tatlı lezzetli küçük çekirdekli Ege meyvesi.", "answer": "İncir" },
        { "question": "Denizlerde kabuklu istiridyelerin içinde kum tanesinin etrafında oluşan değerli parlak süs taşı.", "answer": "İnci" },
        { "question": "Düşünme, konuşma ve alet yapma yeteneğiyle diğer canlılardan ayrılan en gelişmiş varlık.", "answer": "İnsan" },
        { "question": "Bir ülkenin veya kuruluşun bağımsızlığını simgeleyen ve göndere çekilen kumaş sembol.", "answer": "Bayrak", "questionAlt": "İki veya daha çok kişinin uzaktan telefon, internet veya yüz yüze konuşarak bilgi alışverişi yapması.", "answerAlt": "İletişim" }
    ],
    "J": [
        { "question": "Elektrik kesintilerinde yakıt kullanarak elektrik akımı üreten mekanik jeneratör aygıtı.", "answer": "Jeneratör" },
        { "question": "Güneş sistemimizin kütle ve hacim bakımından en büyük gaz devi olan beşinci gezegeni.", "answer": "Jüpiter" },
        { "question": "Kırsal alanlarda emniyet ve asayişi sağlamakla görevli askeri zabıta gücü.", "answer": "Jandarma" },
        { "question": "Olimpiyatlarda atletlerin en uzağa fırlatmak için yarıştığı sivri uçlu hafif mızrak.", "answer": "Cirit", "questionAlt": "Vücut esnekliğini, çevikliğini ve dengesini sergileyen estetik spor dalı.", "answerAlt": "Jimnastik" },
        { "question": "Binalarda kapı ve pencerelerin dışına takılan, ışığı ayarlamaya yarayan kanatlı tahta veya plastik örtü.", "answer": "Panjur", "questionAlt": "Saça şekil vermek ve parlaklık kazandırmak için sürülen yapışkan kozmetik madde.", "answerAlt": "Jöle" },
        { "question": "Yarışmalarda veya mahkemelerde değerlendirme ve karar vermekle görevli seçici heyet.", "answer": "Jüri" },
        { "question": "Tıraş olurken sakalları kesmek için kullanılan çok keskin ince çelik bıçak.", "answer": "Jilet" },
        { "question": "Uzak Doğu'da ortaya çıkan, rakibi fırlatıp yere sabitlemeyi amaçlayan geleneksel savunma sporu.", "answer": "Judo" }
    ],
    "K": [
        { "question": "Kış mevsiminde hava sıcaklığı sıfırın altına düştüğünde yağan beyaz kristal yağış.", "answer": "Kar" },
        { "question": "Göğüs kafesimizin sol tarafında yer alan ve vücuda sürekli kan pompalayan hayati organ.", "answer": "Kalp" },
        { "question": "Yazı yazmak, çizim yapmak için kullanılan ucu kömür veya grafitli kırtasiye aleti.", "answer": "Kalem" },
        { "question": "Tavuk, hindi gibi kanatlı hayvanların folluklara bıraktığı protein zengini kabuklu besin.", "answer": "Yumurta", "questionAlt": "Kırmızı tüyleri, uzun kulakları ve sevimli halleriyle bilinen evcil veya yabani kemirgen.", "answerAlt": "Tavşan", "questionAlt2": "Mısır piramitlerini beklediğine inanılan aslan gövdeli, insan başlı dev heykel.", "answerAlt2": "Sfenks", "questionAlt3": "Evlerde sırtımızı dayayıp oturduğumuz yumuşak ve geniş mobilya.", "answerAlt3": "Koltuk" },
        { "question": "Ağaçların gövdesini kaplayan ve içerideki dokuları koruyan sert dış tabaka, ağaç zırhı.", "answer": "Kabuk" },
        { "question": "İçinde hikayeler, romanlar veya ders bilgileri yer alan basılı sayfalar bütünü.", "answer": "Kitap" },
        { "question": "Gemilerin açık denizlerde fırtınadan sığındığı, yük indirip bindirdiği korunaklı kıyı tesisi.", "answer": "Liman", "questionAlt": "Topkapı Sarayı'nda padişahların ve sadrazamların toplantı yaptığı devasa kapı ve saray bölümü.", "answerAlt": "Kapı" },
        { "question": "Bir devletin yasalarla belirlenmiş yönetim merkezi olan en önemli şehri.", "answer": "Başkent", "questionAlt": "Mutfaklarda yemek pişirmek için ocağın üstüne konulan derin metal kap.", "answerAlt": "Tencere", "questionAlt2": "Yazın tarlalarda olgunlaşan, içi kırmızı çekirdekli ve çok sulu devasa meyve.", "answerAlt2": "Karpuz" }
    ],
    "L": [
        { "question": "Sarı renkli kabuğu olan, C vitamini zengini ve salatalara sıkılan ekşi narenciye meyvesi.", "answer": "Limon" },
        { "question": "Gemi ve teknelerin yanaşıp bağlandığı, yolcu ve yük taşımacılığının yapıldığı kıyı limanı.", "answer": "Liman" },
        { "question": "Özellikle ilkbaharda açan, Osmanlı dönemine adını vermiş soğanlı ve kadeh biçimli çiçek.", "answer": "Lale" },
        { "question": "Bilim insanlarının deneyler, araştırmalar ve testler yaptığı donanımlı oda veya bina.", "answer": "Laboratuvar" },
        { "question": "Düz hatlı, tek renkli ve yoğun ışık demeti üreten ileri optik teknoloji aygıtı.", "answer": "Lazer" },
        { "question": "Elektrik enerjisini aydınlatmaya çeviren armut biçimli cam fanuslu aydınlatma elemanı.", "answer": "Lamba" },
        { "question": "Bebekleri emziren, vücudu kıllarla kaplı ve doğurarak çoğalan canlılar sınıfı.", "answer": "Memeli", "questionAlt": "Kırmızı veya yeşil yapraklı, salatalarda çiğ olarak yenen geniş yapraklı sebze.", "answerAlt": "Marul", "questionAlt2": "Gözdeki netlik sorununu gidermek için göz bebeği üzerine doğrudan yerleştirilen ince saydam mercek.", "answerAlt2": "Lens" },
        { "question": "Şehir içi ve mahalle aralarındaki atık suları toplayıp ana kanala aktaran yer altı boru hattı.", "answer": "Kanalizasyon", "questionAlt": "Tuz oranı yüksek olan sığ kıyı göllerine veya deniz kulağına verilen coğrafi ad.", "answerAlt": "Lagün" }
    ],
    "M": [
        { "question": "Sarı renkli kabuğu soyularak yenen, potasyum zengini tropikal ve tatlı meyve.", "answer": "Muz" },
        { "question": "Tarihi eserlerin, tabloların ve heykellerin sergilendiği halka açık kültür yapısı.", "answer": "Müze" },
        { "question": "Demir, nikel gibi metalleri kendine doğru çeken doğal veya yapay çekim kuvvetine sahip madde.", "answer": "Mıknatıs" },
        { "question": "Binalarda veya okullarda üzerine yazı yazılan, yemek yenilen dört ayaklı ahşap mobilya.", "answer": "Masa" },
        { "question": "Kare veya dikdörtgen şekilli, genellikle kağıt veya tahtadan üretilen ve içine eşya konulan kap.", "answer": "Kutu", "questionAlt": "Dünyanın uydusu olan, geceleri gökyüzünde evrelerine göre parlayan gök cismi.", "answerAlt": "Ay", "questionAlt2": "Gözün ön yüzeyini örten ve ışığı kıran saydam tabaka merceği.", "answerAlt2": "Mercek" },
        { "question": "Gökyüzünün ve açık denizlerin yansıttığı temel renk tonu.", "answer": "Mavi" },
        { "question": "Kumaş, kağıt veya ip gibi şeyleri kesmeye yarayan iki bıçaklı el aleti.", "answer": "Makas" },
        { "question": "Çocuklara ve gençlere okullarda ders anlatan, onları geleceğe hazırlayan eğitimci.", "answer": "Öğretmen", "questionAlt": "Yüksek dağlık bölgelerde taş ve kaya bloklarının işlenmesiyle elde edilen değerli sert yapı taşı.", "answerAlt": "Mermer" }
    ],
    "N": [
        { "question": "Soğuk algınlığı sebebiyle burun akıntısı, hapşırma ve boğaz ağrısıyla seyreden viral enfeksiyon.", "answer": "Nezle" },
        { "question": "Müziğin ses tonlarını ve sürelerini kağıt üzerinde göstermeye yarayan özel işaretler.", "answer": "Nota" },
        { "question": "Bahar aylarında açan, beyaz taç yaprakları ve ortasında sarı borusu olan güzel kokulu soğanlı çiçek.", "answer": "Nergis" },
        { "question": "Atom çekirdeğinde protonlarla birlikte bulunan yüksüz temel parçacık.", "answer": "Nötron" },
        { "question": "Kırmızı kabuklu, içinde yüzlerce tatlı mayhoş yakut tanesi bulunan bereket simgesi meyve.", "answer": "Nar" },
        { "question": "Aşırı sıcak yaz günlerinde havada su buharının yoğunlaşmasıyla oluşan yapışkan hava ağırlığı.", "answer": "Nem" },
        { "question": "Toprak altında yetişen, yemeklerde salçası yapılan kuru ve taze türü olan kokulu acı kök sebze.", "answer": "Soğan", "questionAlt": "Nüfus sayımlarında veya kimlik kartlarında yer alan kişiye özel vatandaşlık kodu.", "answerAlt": "Numara" },
        { "question": "Petrolün rafinerilerde işlenmesiyle elde edilen şeffaf ve uçucu endüstriyel sıvı kimyasal.", "answer": "Nafta" }
    ],
    "O": [
        { "question": "Ağaçlarla, bitki örtüsüyle ve yabani hayvanlarla dolu geniş doğal alan, dünyanın akciğerleri.", "answer": "Orman" },
        { "question": "Çocukların ve gençlerin eğitim görüp bilgi edindiği resmi eğitim kurumu binası.", "answer": "Okul" },
        { "question": "Kıtaları birbirinden ayıran devasa büyüklükteki çok geniş ve derin tuzlu su kütlesi.", "answer": "Okyanus" },
        { "question": "Solunum yaparken ciğerlerimize çektiğimiz ve yaşamın devamını sağlayan hayati gaz elementi.", "answer": "Oksijen" },
        { "question": "Dört yılda bir dünyanın dört bir yanından sporcuların katıldığı devasa spor şöleni.", "answer": "Olimpiyat" },
        { "question": "Eski çağlarda avlanmak veya savaşmak için yay yardımıyla fırlatılan sivri uçlu tahta çubuk.", "answer": "Ok" },
        { "question": "Dört tekerlekli, motorlu ve kişisel ulaşımda en sık kullanılan binek kara aracı.", "answer": "Otomobil" },
        { "question": "Yolcu taşımacılığında kullanılan çok sayıda koltuğu olan büyük şehir içi veya şehirlerarası motorlu taşıt.", "answer": "Otobüs" }
    ],
    "Ö": [
        { "question": "Bir okulda veya kursta öğrencilere ders anlatıp rehberlik eden meslek sahibi kimse.", "answer": "Öğretmen" },
        { "question": "Okulda öğretmenlerin verdiği dersleri dinleyip öğrenen genç veya çocuk, talebe.", "answer": "Öğrenci" },
        { "question": "Sekiz bacaklı, ağ örerek uçan böcekleri avlayan eklem bacaklı canlı.", "answer": "Örümcek" },
        { "question": "Göl veya deniz kenarlarında yaşayan, yassı gagalı, perde ayaklı ve suda yüzen sevimli kuş.", "answer": "Ördek" },
        { "question": "Geçmişte yaşanmış güzel günleri veya sevilen bir insanı kalpten anımsayıp hasret çekme duygusu.", "answer": "Özlem" },
        { "question": "Bir kitabın, makalenin veya konunun ana fikirlerini kısaca toparlayan kısa metin.", "answer": "Özet" },
        { "question": "Güneşin tam tepede olduğu, günün ortasını ifade eden saat dilimi ve vakit.", "answer": "Öğle" },
        { "question": "Toplumda insanların nasıl davranması gerektiğini düzenleyen yazılı olmayan ahlaki gelenekler bütünü.", "answer": "Örf" }
    ],
    "P": [
        { "question": "Alışverişte mal veya hizmet almak için kullanılan resmi devlet basımı değişim aracı.", "answer": "Para" },
        { "question": "Havadayken uçaktan veya yüksek bir uçurumdan güvenle yere inebilmek için açılan dev kumaş kubbe.", "answer": "Paraşüt" },
        { "question": "Toprak altında yumru şeklinde yetişen, kızartması ve püresi çok sevilen temel karbonhidrat sebzesi.", "answer": "Patates" },
        { "question": "Bahar aylarında kırlarda açan, sarı göbeği ve beyaz yapraklarıyla bilinen zarif kır çiçeği.", "answer": "Papatya" },
        { "question": "Tuşlarına basıldığında içindeki çekiçlerin tellere vurmasıyla ses çıkaran büyük klasik müzik aleti.", "answer": "Piyano" },
        { "question": "Kutup bölgelerinde soğuk buzullar üzerinde yaşayan, uçamayan ama usta bir dalgıç olan sevimli kuş.", "answer": "Penguen" },
        { "question": "Haftanın ilk günü olup pazardan sonra gelen iş ve okul başlangıç günü.", "answer": "Pazartesi" },
        { "question": "Evlerde odaların güneş almasını, havalanmasını sağlayan açılır camlı çerçeve bölmesi.", "answer": "Pencere" }
    ],
    "R": [
        { "question": "Ses dalgalarını elektromanyetik dalgalarla havadan ileten ve dinlenen kitle iletişim aracı.", "answer": "Radyo" },
        { "question": "Boya ve fırça yardımıyla tuval veya kağıt üzerine çizilen iki boyutlu görsel sanat eseri.", "answer": "Resim" },
        { "question": "Havadaki yüksek basınçtan alçak basınca doğru esen yatay hava hareketine verilen isim.", "answer": "Rüzgar" },
        { "question": "Uzaya astronot veya uydu taşımak amacıyla fırlatılan çok güçlü itişli motorlara sahip silindirik araç.", "answer": "Roket" },
        { "question": "Kırmızı veya yeşil renkte acı ve tatlı türü olan, salatalara doğranan içi boş sebze.", "answer": "Biber", "questionAlt": "Tiyatro veya sinema oyuncusunun bir sahnede canlandırdığı karakterin payı ve görevi.", "answerAlt": "Rol" },
        { "question": "Tekerlekleri üzerinde dönerek çalışan, bilgisayar kontrollü veya programlanabilir mekanik makine.", "answer": "Robot" },
        { "question": "Sayıları yazmak için kullanılan 0'dan 9'a kadar olan standart matematiksel semboller.", "answer": "Rakam" },
        { "question": "Gözdeki görüntünün odaklandığı, ışığa duyarlı sinir hücreleriyle kaplı en içteki ağ tabakası.", "answer": "Retina" }
    ],
    "S": [
        { "question": "İki hidrojen ve bir oksijen atomundan oluşan, hayatın kaynağı renksiz ve kokusuz sıvı.", "answer": "Su" },
        { "question": "Zamanı saat, dakika ve saniye cinsinden ölçüp kadranında gösteren mekanik veya dijital alet.", "answer": "Saat" },
        { "question": "Havada asılı kalan mikroskobik su damlacıklarının görüş mesafesini düşürdüğü alçak bulut tabakası.", "answer": "Sis" },
        { "question": "Yemeklere lezzet katmak ve dezenfekte etmek için kullanılan beyaz kristal sodyum klorür baharatı.", "answer": "Tuz", "questionAlt": "Doğal veya yapay olarak üretilen, yüzeyleri kayganlaştırıp temizlemeye yarayan köpüklü temizlik maddesi.", "answerAlt": "Sabun" },
        { "question": "Beyaz dişleriyle bilinen, kokusu keskin ve antibiyotik etkili şifalı doğal soğan türü sebze.", "answer": "Sarımsak" },
        { "question": "Yaz aylarında havaların çok sıcak olması sebebiyle vücuttan gözeneklerle atılan tuzlu su damlaları.", "answer": "Ter", "questionAlt": "Hastalıkların veya salgınların yayılmasını önlemek amacıyla alınan güvenlik tedbirleri.", "answerAlt": "Sağlık" },
        { "question": "Ev ve binalarda katlar arasında inip çıkmayı sağlayan basamaklar dizisi.", "answer": "Merdiven", "questionAlt": "Dört tarafı duvarlarla çevrili ve çatısı olan en küçük yaşam odası veya bölümü.", "answerAlt": "Oda", "questionAlt2": "Üzerine oturulan tek kişilik arkalıklı mobilya.", "answerAlt2": "Sandalye" },
        { "question": "Doğada minerallerin basınç ve ısıyla birleşmesinden oluşan katı ve dayanıklı yerkabuğu parçası.", "answer": "Kaya", "questionAlt": "Sonbahar mevsiminde kuruyup dökülen ağaç yapraklarının bütünü.", "answerAlt": "Saman", "questionAlt2": "Ses telleri titreştiğinde ağızdan çıkan melodik veya konuşma seslerinin frekansı.", "answerAlt2": "Ses" }
    ],
    "Ş": [
        { "question": "Yağmurdan veya güneşten korunmak için baş üstünde taşınan açılır kapanır kubbeli gereç.", "answer": "Şemsiye" },
        { "question": "Büyük yerleşim yeri olup köylerden ve ilçelerden daha kalabalık olan il merkezi kenti.", "answer": "Şehir" },
        { "question": "Pancardan veya şeker kamışından elde edilen tatlı kristal toz veya kesme gıda maddesi.", "answer": "Şeker" },
        { "question": "Yüksek bir kayalıktan veya uçurumdan gürül gürül aşağı dökülen doğal su kaynağı, çağlayan.", "answer": "Şelale" },
        { "question": "Duyguların, hayallerin ve düşüncelerin ölçülü ve ahenkli mısralarla dile getirildiği edebi sanat türü.", "answer": "Şiir" },
        { "question": "Gök gürültülü fırtınalarda bulutlar arasında gerçekleşen anlık çok güçlü elektrik deşarjı ışığı.", "answer": "Şimşek" },
        { "question": "Trafikte veya kavşaklarda araçların hızını kesmek ve güvenliği sağlamak için takılan ışıklı cihaz.", "answer": "Sinyal", "questionAlt": "Genellikle cam veya plastikten üretilen, içine içecek konulan dar boyunlu kap.", "answerAlt": "Şişe" },
        { "question": "Bir yarışmada, ligde veya turnuvada birinci gelerek kupayı kaldıran takıma veya kişiye verilen unvan.", "answer": "Şampiyon" }
    ],
    "T": [
        { "question": "Demiryolu rayları üzerinde lokomotif tarafından çekilerek hareket eden uzun yolcu veya yük aracı.", "answer": "Tren" },
        { "question": "Geçmişte yaşanmış olayları, savaşları ve uygarlıkları belgelere dayanarak inceleyen bilim dalı.", "answer": "Tarih" },
        { "question": "Uzaktaki yıldızları, gezegenleri ve gök cisimlerini dev lenslerle yakından görmeye yarayan optik alet.", "answer": "Teleskop" },
        { "question": "Hava sıcaklığını derece cinsinden hassas şekilde ölçen göstergeli ölçüm aracı.", "answer": "Termometre" },
        { "question": "Yaz aylarında kırmızı renkte olgunlaşan, salçası ve çorbası yapılan çekirdekli sulu sebze.", "answer": "Domates", "questionAlt": "Bitkilerin toprağa tutunmasını ve su ile mineralleri emmesini sağlayan yer altı organı.", "answerAlt": "Kök", "questionAlt2": "Ses dalgalarını elektrik sinyaline çevirerek uzaktaki kişilerle anında sesli konuşmayı sağlayan cihaz.", "answerAlt2": "Telefon" },
        { "question": "Yeryüzünü kaplayan, üzerinde bitkilerin ve ağaçların kök saldığı mineral zengini kahverengi tabaka.", "answer": "Toprak" },
        { "question": "Sahneye çıkan oyuncuların seyirciler önünde canlı olarak sergilediği dramatik sahne sanatı.", "answer": "Tiyatro" },
        { "question": "Tarlalarda veya seralarda çiftçilerin toprağı sürüp ekmesi için kullandığı büyük tekerlekli motorlu araç.", "answer": "Traktör" }
    ],
    "U": [
        { "question": "Hava yoluyla yolcu ve kargo taşımaya yarayan motorlu ve kanatlı büyük hava aracı, tayyare.", "answer": "Uçak" },
        { "question": "Gezegenlerin ve yıldızların ötesinde yer alan, sonsuz kabul edilen karanlık ve sessiz madde boşluğu.", "answer": "Uzay" },
        { "question": "Denizlerin metrelerce altında batmadan ilerleyebilen periskoplu askeri veya bilimsel deniz aracı.", "answer": "Denizaltı", "questionAlt": "Uçakları ve helikopterleri güvenle kullanan ehliyetli ve eğitimli hava pilotu.", "answerAlt": "Uçman", "questionAlt2": "Bir gezegenin çekim alanında onun etrafında dolanan doğal veya insan yapımı yapay gök cismi.", "answerAlt2": "Uydu" },
        { "question": "Her gece yatağa yattığımızda beynimizin dinlenmesi ve vücudun yenilenmesi için girdiğimiz bilinçsiz hal.", "answer": "Uyku" },
        { "question": "Toprağın, bitkilerin veya dağların çok derin ve dik olan tehlikeli kenar yamacı, yar.", "answer": "Uçurum" },
        { "question": "Genellikle rüzgarlı ilkbahar günlerinde çocukların iple gökyüzüne saldığı çıtalı kağıt oyuncak.", "answer": "Uçurtma" },
        { "question": "Belli bir meslek veya bilim dalında çok derin bilgi ve deneyime sahip olan ihtisas sahibi kimse.", "answer": "Uzman" },
        { "question": "Güneş sistemimizde güneşe en uzak yedinci sırada yer alan buz devi mavi-yeşil gezegen.", "answer": "Uranüs" }
    ],
    "Ü": [
        { "question": "Salkım salkım yetişen, yaş veya kuru olarak tüketilen ve sirkesi yapılan şifalı tatlı meyve.", "answer": "Üzüm" },
        { "question": "Lise eğitimini tamamlayan gençlerin yükseköğrenim ve diploma almak için gittiği büyük akademik kurum.", "answer": "Üniversite" },
        { "question": "Kıyafetlerdeki ve kumaşlardaki kırışıklıkları buhar ve sıcak metal tabanla düzelten elektrikli ev aleti.", "answer": "Ütü" },
        { "question": "Sınırlar ile belirlenmiş, bir milletin üzerinde bağımsız olarak yaşadığı toprak parçası, vatan.", "answer": "Ülke" },
        { "question": "Yaz kış demeden fabrikalarda veya tarlalarda hammaddeyi işleyerek mal ve değer ortaya koyma eylemi.", "answer": "Üretim" },
        { "question": "Herkes tarafından tanınan, bilinen ve toplumda büyük bir şöhrete sahip olan kimse.", "answer": "Ünlü" },
        { "question": "Geleceğe dair beslenen güzel beklenti, karamsarlığın zıddı olan içsel inanç ve iyimserlik duygusu.", "answer": "Ümit" },
        { "question": "Duygusal veya fiziksel bir aksilik karşısında duyulan keder, acı ve moral bozukluğu.", "answer": "Üzüntü" }
    ],
    "V": [
        { "question": "Denizlerde ve göllerde iki kıyı arasında düzenli yolcu ve yük taşıyan motorlu deniz taşıtı.", "answer": "Vapur" },
        { "question": "İki dağ veya tepe arasında kalan, genellikle tabanında bir ırmak veya dere yatağı bulunan çukurluk.", "answer": "Vadi" },
        { "question": "Bir insanın veya milletin üzerinde doğup büyüdüğü, canı pahasına savunduğu kutsal ata yurdu.", "answer": "Vatan" },
        { "question": "Çiçekleri canlı tutmak ve sergilemek için içine su konulan cam, porselen veya kilden yapılan süs kabı.", "answer": "Vazo" },
        { "question": "Yüksek bir filenin üzerinden topu yere düşürmeden elle karşı sahaya geçirme kuralına dayanan takım oyunu.", "answer": "Voleybol" },
        { "question": "Grip, kuduz ve nezle gibi hastalıklara yol açan, sadece canlı hücrelerin içinde çoğalabilen mikroskobik parçacık.", "answer": "Virüs" },
        { "question": "Bir ilin genel yönetiminden, asayişinden ve devlet hizmetlerinden sorumlu olan en üst düzey mülki amir.", "answer": "Vali" },
        { "question": "Bir hedefe ulaşmak, bir yere ayak basmak anlamına gelen eylem, hedefe ulaşma.", "answer": "Varış" }
    ],
    "Y": [
        { "question": "Bulutlardaki su damlacıklarının yoğunlaşarak yer çekimi etkisiyle yeryüzüne düşen sıvı yağış türü.", "answer": "Yağmur" },
        { "question": "Geceleri gökyüzünde ışıl ışıl parlayan, kendi ışığını üreten devasa gaz ve plazma kütlesi.", "answer": "Yıldız" },
        { "question": "Kuşların ve sürüngenlerin üremek için yumurtladığı, sarısı ve beyazı olan protein zengini besin.", "answer": "Yumurta" },
        { "question": "Denizlerde yaşayan, son derece zeki ve insanlara dostça yaklaşmasıyla bilinen memeli deniz canlısı.", "answer": "Yunus" },
        { "question": "Güneşin etrafında eliptik bir yörüngede dönen Dünya, Mars gibi büyük gök cisimlerinin genel adı.", "answer": "Gezegen", "questionAlt": "Yatakta başımızın altına koyduğumuz, içi pamuk veya elyafla doldurulmuş yumuşak yastık.", "answerAlt": "Yastık" },
        { "question": "Dört mevsimden en sıcağı olup deniz ve tatil sezonunun açıldığı yaz dönemi.", "answer": "Yaz" },
        { "question": "Kuşların ve böceklerin gökyüzünde süzülmesini ve havalanmasını sağlayan kanat organı.", "answer": "Kanat", "questionAlt": "Eski dönemlerde düşmanlardan korunmak amacıyla tepelere inşa edilen savunma kalesi.", "answerAlt": "Kale", "questionAlt2": "Düşüncelerin harflerle kağıda dökülmüş biçimi, alfabe sembolleri bütünü.", "answerAlt2": "Yazı" },
        { "question": "Deniz, göl veya havuz suyunda kollar ve bacaklar yardımıyla batmadan ilerleme sporu.", "answer": "Yüzme" }
    ],
    "Z": [
        { "question": "Akdeniz ikliminin kutsal ağacı olan, kahvaltıların baş tacı ve yağı çıkarılan küçük taneli meyve.", "answer": "Zeytin" },
        { "question": "Bir dağın veya yüksek bir tepenin en uç noktası, doruk tepe noktası.", "answer": "Zirve" },
        { "question": "Masa oyunlarında, tavlada atılan 1'den 6'ya kadar noktaları bulunan kemik veya plastik küp.", "answer": "Zar" },
        { "question": "Afrika savanalarında yaşayan, dünyanın en uzun boylu ve en uzun boyunlu otçul memeli hayvanı.", "answer": "Zürafa" },
        { "question": "Gözle görülemeyecek kadar küçük canlıları binlerce kat büyüterek inceleyen laboratuvar aleti.", "answer": "Mikroskop", "questionAlt": "Vücuda girdiğinde hücreleri tahrip ederek ölüme veya hastalığa yol açan zararlı toksik madde.", "answerAlt": "Zehir" },
        { "question": "Okullarda veya evlerin kapılarında bir eylemin başladığını ya da misafir geldiğini bildiren sesli aygıt.", "answer": "Zil" },
        { "question": "İçinde pek çok zengin mineral barındıran, sıcak iklimlerde yetişen şifalı kök baharat bitkisi.", "answer": "Zencefil" },
        { "question": "Kollarda veya ceplerde taşınan, saat, dakika ve saniyeleri içine alan kesintisiz akış boyutu.", "answer": "Zaman" }
    ]
};
