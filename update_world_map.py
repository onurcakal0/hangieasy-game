import re

with open('templates/guess_world.html', 'r') as f:
    content = f.read()

old_html = """    <div id="bitis-ekrani">
        <div class="bitis-icerik">
            <div id="bitis-baslik">Oyun Bitti!</div>
            <div style="color:var(--muted); font-size:18px; margin-bottom:10px;">Bulduğun Ülke Sayısı</div>
            <div id="bitis-skor">0 / 0</div>
            <a href="/guess-world" class="btn-anasayfa">🔄 Tekrar Oyna</a>
        </div>
    </div>"""

new_html = """    <div id="bitis-ekrani">
        <div class="bitis-icerik" style="max-width: 600px; width: 90%;">
            <div id="bitis-baslik">Oyun Bitti!</div>
            <div style="color:var(--muted); font-size:18px; margin-bottom:10px;">Bulduğun Ülke Sayısı</div>
            <div id="bitis-skor">0 / 0</div>
            
            <div id="skor-kayit-alani" style="margin-bottom: 20px; background: rgba(0,0,0,0.4); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="color: #aaa; font-size: 14px; margin-bottom: 10px;">Global sıralamaya katılmak için adını gir:</p>
                <div style="display: flex; gap: 10px; max-width: 400px; margin: 0 auto;">
                    <input type="text" id="oyuncu-ismi" value="{% if session.get('kullanici_adi') and not session['kullanici_adi'].startswith('Misafir') %}{{ session['kullanici_adi'] }}{% endif %}" placeholder="Adın veya Rumuzun" style="flex: 1; padding: 12px; border-radius: 8px; border: none; background: rgba(255,255,255,0.1); color: white; outline: none;">
                    <button onclick="skoruKaydet()" id="btn-skor-kaydet" style="padding: 12px 25px; border-radius: 8px; border: none; background: var(--primary); color: black; font-weight: bold; cursor: pointer; transition: 0.3s;">Kaydet</button>
                </div>
            </div>

            <div id="liderlik-tablosu" style="display: none; background: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px; margin-bottom: 20px; max-height: 250px; overflow-y: auto;">
                <h3 style="color: var(--primary); margin-bottom: 15px; font-size: 20px;">🏆 GÜNÜN LİDERLERİ (DÜNYA)</h3>
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

            <a href="/guess-world" class="btn-anasayfa">🔄 Tekrar Oyna</a>
            <a href="/" class="btn-anasayfa" style="background: transparent; border: 1px solid rgba(255,255,255,0.2); margin-left: 10px;">🏠 Stüdyoya Dön</a>
        </div>
    </div>"""

content = content.replace(old_html, new_html)

js_to_insert = """
        async function skoruKaydet() {
            const isim = document.getElementById('oyuncu-ismi').value.trim() || 'Gizemli Oyuncu';
            const gecenSure = (sureDakika * 60) - kalanSaniye;
            const btn = document.getElementById('btn-skor-kaydet');
            btn.innerText = 'Kaydediliyor...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/harita_skor_kaydet', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        oyun_turu: 'world_map',
                        kullanici_adi: isim,
                        bulunan_sehir_sayisi: bulunanUlkeler.size,
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
                const res = await fetch('/api/harita_liderlik_tablosu/world_map');
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
                        <td style="padding: 10px; color: #2ecc71;">${skor.bulunan_sehir_sayisi} Ülke</td>
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
    # Insert JS before </script> at the end
    content = content.replace("            setTimeout(() => {", js_to_insert + "\n            setTimeout(() => {")
    content = content.replace("document.getElementById('bitis-ekrani').style.display = 'flex';", "document.getElementById('bitis-ekrani').style.display = 'flex';\n                liderlikTablosunuYukle();")
    with open('templates/guess_world.html', 'w') as f:
        f.write(content)
    print("world_map updated")
else:
    print("Already updated")
