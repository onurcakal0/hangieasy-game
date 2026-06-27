import urllib.request

urls = [
    "https://icon.horse/icon/apple.com",
    "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://apple.com&size=128"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        print(f"OK: {u}")
    except Exception as e:
        print(f"FAIL: {u} - {e}")
