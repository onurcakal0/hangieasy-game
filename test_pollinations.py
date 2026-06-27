import urllib.request

url = "https://image.pollinations.ai/prompt/The%20Godfather%201972%20movie%20scene%20Vito%20Corleone%20in%20his%20dark%20office%20cinematic%20realistic?width=800&height=450&nologo=1"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    print("OK:", res.status)
except Exception as e:
    print("ERROR:", e)
