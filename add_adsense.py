import os
import glob

adsense_script = '    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4362078981934571" crossorigin="anonymous"></script>\n'

for file in glob.glob('templates/*.html'):
    with open(file, 'r') as f:
        content = f.read()
    
    if 'pagead2.googlesyndication.com' in content:
        continue
        
    if '</head>' in content:
        content = content.replace('</head>', adsense_script + '</head>')
        with open(file, 'w') as f:
            f.write(content)
        print(f"Added AdSense to {file}")

