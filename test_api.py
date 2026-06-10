from app import app
with app.test_client() as client:
    resp = client.get('/api/sorular/13')
    print("STATUS:", resp.status_code)
    try:
        print("JSON LENGTH:", len(resp.json))
    except Exception as e:
        print("JSON ERROR:", e)
        print("RAW DATA:", resp.data)
