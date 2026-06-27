import re

old_html = """                <div class="social-icons">
                    <a href="#"><i class="fa-brands fa-instagram"></i></a>
                    <a href="#"><i class="fa-brands fa-twitter"></i></a>
                    <a href="#"><i class="fa-brands fa-youtube"></i></a>
                    <a href="#"><i class="fa-brands fa-tiktok"></i></a>
                </div>"""

new_html = """                <div class="social-icons">
                    <a href="https://www.instagram.com/hangieasy?igsh=eGZpNjF6NWUyY3h5&utm_source=qr" target="_blank"><i class="fa-brands fa-instagram"></i> HangiEasy</a>
                    <a href="https://www.instagram.com/komplikefutbol?igsh=MTJwd2xjajl4dGZ1Nw%3D%3D&utm_source=qr" target="_blank"><i class="fa-brands fa-instagram"></i> Komplike Futbol</a>
                </div>"""

old_css = """        .social-icons a {
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
        }"""

new_css = """        .social-icons a {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0 12px;
            height: 35px;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: #fff;
            margin-right: 10px;
            margin-bottom: 10px;
            text-decoration: none;
            font-size: 13px;
            transition: 0.3s;
        }"""

for filename in ['templates/dashboard.html', 'templates/world_cup_2026.html']:
    with open(filename, 'r') as f:
        content = f.read()
    
    content = content.replace(old_html, new_html)
    content = content.replace(old_css, new_css)
    
    with open(filename, 'w') as f:
        f.write(content)
        
print("Updated social icons and CSS in both files!")
