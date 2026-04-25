let mevcutSkor = 0;
let mevcutSoruIndex = 0;
let sorular = [];

window.onload = function() {
    apiDanSorulariCek();
};

function apiDanSorulariCek() {
    // DİKKAT: Burada ters tırnak kullanıyoruz ki OYUN_ID dinamik olarak URL'ye eklensin
    fetch(`/api/sorular/${OYUN_ID}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("API'den yanıt alınamadı patron!");
            }
            return response.json();
        })
        .then(data => {
            sorular = data;
            // Kategori boşsa uyar
            if(sorular.length === 0) {
                document.querySelector('.oyun-kutusu').innerHTML = "<h2 style='color:#e74c3c;'>Patron bu kategoriye henüz soru girmedin!</h2>";
                return;
            }
            soruyuEkranaBas();
        })
        .catch(error => console.error("Veri çekme hatası:", error));
}

function soruyuEkranaBas() {
    if (mevcutSoruIndex >= sorular.length) {
        oyunuBitir();
        return;
    }

    let aktifSoru = sorular[mevcutSoruIndex];
    let resimElementi = document.getElementById('soru-resmi');
    resimElementi.src = aktifSoru.resim;
    resimElementi.style.display = "block";

    let butonKutusu = document.getElementById('buton-kutusu');
    butonKutusu.innerHTML = '';

    aktifSoru.secenekler.forEach(secenek => {
        let btn = document.createElement('button');
        btn.className = 'secenek-btn';
        btn.innerText = secenek;
        btn.onclick = function() { cevapKontrol(this, aktifSoru.dogru_cevap); };
        butonKutusu.appendChild(btn);
    });
}

function cevapKontrol(secilenButon, dogruCevap) {
    let secilenMetin = secilenButon.innerText;
    let tumButonlar = document.querySelectorAll('.secenek-btn');

    tumButonlar.forEach(btn => btn.onclick = null);

    if (secilenMetin === dogruCevap) {
        secilenButon.classList.add('dogru');
        mevcutSkor += 10;
        document.getElementById('skor').innerText = mevcutSkor;
    } else {
        secilenButon.classList.add('yanlis');
        tumButonlar.forEach(btn => {
            if (btn.innerText === dogruCevap) {
                btn.classList.add('dogru');
            }
        });
    }

    setTimeout(() => {
        mevcutSoruIndex++;
        soruyuEkranaBas();
    }, 1500);
}

function oyunuBitir() {
    let oyunKutusu = document.querySelector('.oyun-kutusu');
    oyunKutusu.innerHTML = `
        <div class="baslik">
            <h2 style="color: #27ae60;">Oyun Bitti!</h2>
            <h1 style="margin: 20px 0;">Skorun: ${mevcutSkor}</h1>
            <input type="text" id="oyuncu-ismi" placeholder="Adını yaz kral..." style="padding:12px; width:80%; margin-bottom:15px; border-radius:8px; border:none; text-align:center; font-size:16px; font-weight:bold; color:#333;">
            <br>
            <button class="secenek-btn" style="background-color: #f39c12;" onclick="skoruKaydet()">Sıralamaya Katıl</button>
        </div>
        <div id="liderlik-alani" style="margin-top:20px; text-align:left;"></div>
    `;
}

function skoruKaydet() {
    let isim = document.getElementById('oyuncu-ismi').value;
    if (isim === "") {
        alert("Sahaya isimsiz çıkılmaz patron, adını gir!");
        return;
    }
    fetch('/api/skor_kaydet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ isim: isim, skor: mevcutSkor })
    })
    .then(response => response.json())
    .then(data => {
        let liderlikHTML = "<h3 style='color:#f39c12; text-align:center; margin-bottom:10px;'>🏆 Top 5 Sıralama 🏆</h3><ul style='list-style:none; padding:0;'>";
        data.forEach((kisi, index) => {
            liderlikHTML += `<li style="background:#2c3e50; margin:8px 0; padding:12px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;"><span><b>${index + 1}.</b> ${kisi.isim}</span> <span style="color:#f1c40f; font-weight:bold;">${kisi.skor} Puan</span></li>`;
        });
        liderlikHTML += "</ul><button class='secenek-btn' style='margin-top:15px; width:100%; background-color: #34495e;' onclick='location.href=\"/\"'>Ana Sayfaya Dön</button>";
        document.querySelector('.baslik').style.display = 'none';
        document.getElementById('liderlik-alani').innerHTML = liderlikHTML;
    });
}