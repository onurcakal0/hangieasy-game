import re

footer_html = """
    <!-- YENİ GELİŞMİŞ FOOTER (QUIZEI TARZI) -->
    <footer class="site-footer">
        <div class="footer-top-border"></div>
        <div class="footer-container">
            <div class="footer-col brand-col">
                <a href="/" class="footer-logo">Hangi<span>Easy</span></a>
                <p class="footer-desc">HangiEasy, eğlenceli ve etkileşimli quizlerin dünyasıdır. Bilgi, seçim ve eğlence bir arada! Burada herkes için bir test var!</p>
                <div class="social-icons">
                    <a href="#"><i class="fa-brands fa-instagram"></i></a>
                    <a href="#"><i class="fa-brands fa-twitter"></i></a>
                    <a href="#"><i class="fa-brands fa-youtube"></i></a>
                    <a href="#"><i class="fa-brands fa-tiktok"></i></a>
                </div>
                <div class="lang-selector">
                    <span>A/文 TR (Türkçe)</span>
                </div>
            </div>
            
            <div class="footer-col links-col">
                <h3 class="footer-heading"><i class="fa-solid fa-trophy"></i> TURNUVA</h3>
                <ul>
                    <li><a href="/world-cup-2026">Turnuva Ağacı</a></li>
                    <li><a href="/">O mu, Bu mu?</a></li>
                    <li><a href="/">Kör Sıralama</a></li>
                    <li><a href="/">Klasik Testler</a></li>
                </ul>
            </div>

            <div class="footer-col links-col">
                <h3 class="footer-heading"><i class="fa-solid fa-futbol"></i> WORLD CUP 2026</h3>
                <ul>
                    <li><a href="/world-cup-2026">Şampiyon Kim Olur?</a></li>
                    <li><a href="/world-cup-2026">Bulanık Bayrak Avı</a></li>
                    <li><a href="/world-cup-2026">En Şık Forma Seçimi</a></li>
                    <li><a href="/world-cup-2026">Futbolun Yeni Kuralları</a></li>
                </ul>
            </div>

            <div class="footer-col links-col">
                <h3 class="footer-heading"><i class="fa-solid fa-info-circle"></i> BİLGİ</h3>
                <ul>
                    <li><a href="/aydinlatma_metni">Gizlilik Politikası</a></li>
                    <li><a href="/kullanici_sozlesmesi">Kullanım Koşulları</a></li>
                    <li><a href="/veri_gizlilik">Veri Gizliliği</a></li>
                    <li><a href="#">İletişim</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2026 - HangiEasy & Komplike Futbol - All rights reserved</p>
            <button class="scroll-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})"><i class="fa-solid fa-chevron-up"></i></button>
        </div>
    </footer>

    <style>
        .site-footer {
            background-color: #0b0c10;
            color: #c5c6c7;
            font-family: 'Poppins', sans-serif;
            position: relative;
            margin-top: 80px;
            padding-bottom: 20px;
        }
        .footer-top-border {
            height: 10px;
            width: 100%;
            background: repeating-linear-gradient(45deg, #111, #111 15px, #f1c40f 15px, #f1c40f 30px);
            border-bottom: 2px solid #d4af37;
        }
        .footer-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 40px;
            padding: 60px 20px 40px;
        }
        .footer-logo {
            font-size: 28px;
            font-weight: 900;
            color: #fff;
            text-decoration: none;
            display: block;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        .footer-logo span { color: #f1c40f; }
        .footer-desc {
            font-size: 13px;
            line-height: 1.6;
            color: #888;
            margin-bottom: 20px;
            max-width: 300px;
        }
        .social-icons a {
            display: inline-block;
            width: 35px;
            height: 35px;
            line-height: 35px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: #fff;
            margin-right: 10px;
            transition: 0.3s;
        }
        .social-icons a:hover {
            background: #f1c40f;
            color: #000;
            border-color: #f1c40f;
            transform: translateY(-3px);
        }
        .lang-selector {
            margin-top: 20px;
            display: inline-block;
            padding: 8px 15px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            font-size: 12px;
            cursor: pointer;
            transition: 0.3s;
        }
        .lang-selector:hover { border-color: #f1c40f; color: #f1c40f; }
        
        .footer-heading {
            font-size: 16px;
            font-weight: 700;
            color: #f1c40f;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .links-col ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .links-col ul li { margin-bottom: 12px; }
        .links-col ul li a {
            color: #888;
            text-decoration: none;
            font-size: 14px;
            transition: 0.3s;
        }
        .links-col ul li a:hover { color: #fff; padding-left: 5px; }
        
        .footer-bottom {
            max-width: 1200px;
            margin: 0 auto;
            border-top: 1px solid rgba(255,255,255,0.05);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #666;
        }
        .scroll-top {
            background: rgba(255,255,255,0.1);
            border: none;
            color: #fff;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            transition: 0.3s;
        }
        .scroll-top:hover {
            background: #f1c40f;
            color: #000;
        }

        @media (max-width: 900px) {
            .footer-container {
                grid-template-columns: 1fr 1fr;
            }
        }
        @media (max-width: 600px) {
            .footer-container {
                grid-template-columns: 1fr;
            }
            .footer-bottom {
                flex-direction: column;
                gap: 15px;
                text-align: center;
            }
        }
    </style>
"""

with open('templates/dashboard.html', 'r') as f:
    content = f.read()

# Replace <script> with footer + <script> (inserting just above scripts at the bottom)
if "<!-- YENİ GELİŞMİŞ FOOTER" not in content:
    content = content.replace("    <script>", footer_html + "\n    <script>")
    with open('templates/dashboard.html', 'w') as f:
        f.write(content)
    print("Footer added to dashboard.html")
else:
    print("Footer already exists in dashboard.html")

