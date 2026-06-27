import urllib.request
import urllib.parse
import re

movies = [
    "The Godfather movie scene",
    "Titanic jack and rose bow scene",
    "Avatar 2009 movie scene pandora",
    "The Dark Knight joker interrogation scene",
    "Forrest Gump bench scene",
    "The Matrix neo dodging bullets scene",
    "Inception hallway fight scene",
    "Lord of the Rings return of the king charge scene",
    "Interstellar gargantua scene",
    "Harry potter sorcerers stone floating candles scene",
    "The Avengers 2012 circle scene",
    "Jurassic Park t-rex roar scene",
    "Star Wars Episode IV binary sunset scene",
    "Spider-Man 2002 upside down kiss scene",
    "Joker 2019 stairs dance scene",
    "The Lion King 1994 pride rock scene",
    "Gladiator are you not entertained scene",
    "Back to the future clock tower scene",
    "Pulp fiction dance scene",
    "Fight club rules scene"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

results = []
for m in movies:
    query = urllib.parse.quote(m)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Duckduckgo HTML might not have images directly. Let's try bing.
    except Exception as e:
        pass

# Actually let's use TMDB backdrops by ID directly from TMDB's public site!
