import re

with open('templates/harita_tr.html', 'r') as f:
    content = f.read()

old_html = """        <div id="bitis-ekrani">
            <h2 style="color: #00f2fe; font-size: 36px; margin-bottom: 20px; font-weight: 900; text-transform: uppercase;" id="bitis-baslik">Süre Doldu!</h2>
            <div style="font-size: 60px; font-weight: 900; color: #facc15; margin-bottom: 20px; text-shadow: 0 0 30px rgba(250,204,21,0.5);" id="bitis-skor">
                0 / 81
            </div>
            <p style="color: #aaa; font-size: 16px; margin-bottom: 30px;">Türkiye coğrafyasına ne kadar hakimsin gördük!</p>
            <a href="/" class="btn-anasayfa">🏠 Stüdyoya Dön</a>
        </div>"""

new_html = """        <div id="bitis-ekrani">
            <h2 style="color: #00f2fe; font-size: 36px; margin-bottom: 20px; font-weight: 900; text-transform: uppercase;" id="bitis-baslik">Süre Doldu!</h2>
            <div style="font-size: 60px; font-weight: 900; color: #facc15; margin-bottom: 20px; text-shadow: 0 0 30px rgba(250,204,21,0.5);" id="bitis-skor">
                0 / 81
            </div>
            
            <div id="skor-kayit-alani" style="margin-bottom: 30px; background: rgba(0,0,0,0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="color: #aaa; font-size: 14px; margin-bottom: 10px;">Global sıralamaya katılmak için adını gir:</p>
                <div style="display: flex; gap: 10px; max-width: 400px; margin: 0 auto;">
                    <input type="text" id="oyuncu-ismi" value="{% if session.get('kullanici_adi') and not session['kullanici_adi'].startswith('Misafir') %}{{ session['kullanici_adi'] }}{% endif %}" placeholder="Adın veya Rumuzun" style="flex: 1; padding: 12px; border-radius: 8px; border: none; background: rgba(255,255,255,0.1); color: white; outline: none;">
                    <button onclick="skoruKaydet()" id="btn-skor-kaydet" style="padding: 12px 25px; border-radius: 8px; border: none; background: #00f2fe; color: black; font-weight: bold; cursor: pointer; transition: 0.3s;">Kaydet</button>
                </div>
            </div>

            <div id="liderlik-tablosu" style="display: none; background: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px; margin-bottom: 30px; max-height: 250px; overflow-y: auto;">
                <h3 style="color: #facc15; margin-bottom: 15px; font-size: 20px;">🏆 GÜNÜN LİDERLERİ (TR)</h3>
                <table style="width: 100%; text-align: left; color: white; border-collapse: collapse;">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.2); color: #00f2fe;">
                            <th style="padding: 10px;">Sıra</th>
                            <th style="padding: 10px;">Kullanıcı</th>
                            <th style="padding: 10px;">Skor</th>
                            <th style="padding: 10px;">Süre</th>
                        </tr>
                    </thead>
                    <tbody id="liderlik-listesi">
                    </tbody>
                </table>
            </div>

            <a href="/" class="btn-anasayfa">🏠 Stüdyoya Dön</a>
        </div>"""

content = content.replace(old_html, new_html)

js_to_insert = """
        async function skoruKaydet() {
            const isim = document.getElementById('oyuncu-ismi').value.trim() || 'Gizemli Oyuncu';
            const gecenSure = 600 - sure;
            const btn = document.getElementById('btn-skor-kaydet');
            btn.innerText = 'Kaydediliyor...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/harita_skor_kaydet', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        oyun_turu: 'tr_map',
                        kullanici_adi: isim,
                        bulunan_sehir_sayisi: bulunanlar.size,
                        gecen_sure_saniye: gecenSure
                    })
                });
                
                if(res.ok) {
                    document.getElementById('skor-kayit-alani').style.display = 'none';
                    await liderlikTablosunuYukle();
                }
            } catch (error) {
                console.error(error);
                btn.innerText = 'Hata! Tekrar dene';
                btn.disabled = false;
            }
        }

        async function liderlikTablosunuYukle() {
            document.getElementById('liderlik-tablosu').style.display = 'block';
            const tbody = document.getElementById('liderlik-listesi');
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 10px;">Yükleniyor...</td></tr>';
            
            try {
                const res = await fetch('/api/harita_liderlik_tablosu/tr_map');
                const data = await res.json();
                
                tbody.innerHTML = '';
                if(data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 10px; color:#aaa;">Henüz kimse skor kaydetmedi. İlk sen ol!</td></tr>';
                    return;
                }
                
                data.forEach((skor, index) => {
                    let siraRenk = index === 0 ? '#facc15' : index === 1 ? '#e2e8f0' : index === 2 ? '#cd7f32' : 'white';
                    let tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                    tr.innerHTML = `
                        <td style="padding: 10px; color: ${siraRenk}; font-weight: bold;">#${index + 1}</td>
                        <td style="padding: 10px; font-weight: bold;">${skor.kullanici_adi}</td>
                        <td style="padding: 10px; color: #2ecc71;">${skor.bulunan_sehir_sayisi} Şehir</td>
                        <td style="padding: 10px; color: #aaa;">${Math.floor(skor.gecen_sure_saniye / 60)}:${(skor.gecen_sure_saniye % 60).toString().padStart(2, '0')}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (error) {
                console.error(error);
                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 10px; color:red;">Tablo yüklenemedi.</td></tr>';
            }
        }
"""

if "function skoruKaydet" not in content:
    content = content.replace("function oyunuBitir", js_to_insert + "\n        function oyunuBitir")
    content = content.replace("document.getElementById('bitis-ekrani').style.display = 'block';", "document.getElementById('bitis-ekrani').style.display = 'block';\n            liderlikTablosunuYukle();")
    with open('templates/harita_tr.html', 'w') as f:
        f.write(content)
    print("tr_map updated")
