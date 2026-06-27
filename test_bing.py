import urllib.request
import re
import urllib.parse

def get_image(query):
    url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    # Find murl":"..."
    match = re.search(r'murl":"([^"]+)"', html)
    if match:
        return match.group(1)
    return None

print(get_image("Arthur Morgan character RDR2"))
