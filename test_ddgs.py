from duckduckgo_search import DDGS
import json

ddgs = DDGS()
results = list(ddgs.images("Bayer Leverkusen logo png", max_results=1))
print(json.dumps(results))
