import os
import glob

favicon_tag = '    <link rel="icon" type="image/png" href="{{ url_for(\'static\', filename=\'img/favicon.png\') }}">\n'

for file in glob.glob('templates/*.html'):
    with open(file, 'r') as f:
        content = f.read()
    
    if 'img/favicon.png' in content:
        continue
        
    if '</head>' in content:
        content = content.replace('</head>', favicon_tag + '</head>')
        with open(file, 'w') as f:
            f.write(content)
        print(f"Added favicon to {file}")

