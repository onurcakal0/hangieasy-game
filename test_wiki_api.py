import urllib.request
import json
import urllib.parse

wiki_title = "Bayer_04_Leverkusen"
url = f"https://en.wikipedia.org/w/api.php?action=query&titles={wiki_title}&prop=pageimages&format=json&pithumbsize=500"
req = urllib.request.Request(url, headers={'User-Agent': 'HangiEasyBot/1.0 (contact@hangieasy.com)'})
response = urllib.request.urlopen(req).read().decode('utf-8')
data = json.loads(response)

pages = data['query']['pages']
for page_id in pages:
    if 'thumbnail' in pages[page_id]:
        print("Image:", pages[page_id]['thumbnail']['source'])
    else:
        print("No thumbnail found.")
