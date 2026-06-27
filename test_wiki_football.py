import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Aston_Villa_F.C."
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

match = re.search(r'meta property="og:image" content="(.*?)"', html)
if match:
    print("Found:", match.group(1))
else:
    print("Not found")
