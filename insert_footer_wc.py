import re

with open('insert_footer.py', 'r') as f:
    content = f.read()

# Extract the footer_html variable
match = re.search(r'footer_html = """(.*?)"""', content, re.DOTALL)
if match:
    footer_html = match.group(1)
    
    with open('templates/world_cup_2026.html', 'r') as f:
        wc_content = f.read()

    # world_cup_2026.html might not have a <script> block at the end, let's replace </body>
    if "<!-- YENİ GELİŞMİŞ FOOTER" not in wc_content:
        wc_content = wc_content.replace("</body>", footer_html + "\n</body>")
        with open('templates/world_cup_2026.html', 'w') as f:
            f.write(wc_content)
        print("Footer added to world_cup_2026.html")
    else:
        print("Footer already exists in world_cup_2026.html")
