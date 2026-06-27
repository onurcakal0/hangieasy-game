import urllib.request
import json

def get_twitch_pfp(username):
    url = "https://gql.twitch.tv/gql"
    headers = {
        'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'Content-Type': 'application/json'
    }
    body = [{
        "operationName": "ChannelShell",
        "variables": {"login": username},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "580ab410bcd0c1ad194224957ae2241e5d252b2c5173d8e0cce9d32d5bb14efe"
            }
        }
    }]
    
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    res = urllib.request.urlopen(req).read().decode()
    data = json.loads(res)
    
    try:
        user = data[0]['data']['userOrError']
        if 'profileImageURL' in user:
            return user['profileImageURL']
    except Exception as e:
        pass
    return None

print("Elraenn:", get_twitch_pfp('elraenn'))
print("wtcN:", get_twitch_pfp('wtcn'))
print("Jahrein:", get_twitch_pfp('jahrein'))
