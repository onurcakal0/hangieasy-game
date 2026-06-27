import urllib.request
import re
import urllib.parse

def get_image(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query + " image")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'img class="zcm__images__img" src="([^"]+)"', html)
        if match:
            return match.group(1)
    except Exception as e:
        pass
    return None

print(get_image("Arthur Morgan character RDR2"))
