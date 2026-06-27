import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Replace Pixabay URLs with reliable Wikimedia Commons URLs
pele_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Pel%C3%A9_1966.jpg/500px-Pel%C3%A9_1966.jpg"
rossi_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Paolo_Rossi_in_1982.jpg/500px-Paolo_Rossi_in_1982.jpg"

maradona_img = "https://r2.thesportsdb.com/images/media/player/thumb/z4v3ox1515072958.jpg"
baggio_img = "https://r2.thesportsdb.com/images/media/player/thumb/46dpqf1496579845.jpg"

cur.execute("""
    UPDATE soru 
    SET resim_url = %s 
    WHERE oyun_id = 26 AND secenekler = 'Pele,Diego Maradona';
""", (f"{pele_img},{maradona_img}",))

cur.execute("""
    UPDATE soru 
    SET resim_url = %s 
    WHERE oyun_id = 26 AND secenekler = 'Roberto Baggio,Paolo Rossi';
""", (f"{baggio_img},{rossi_img}",))

conn.commit()
cur.close()
conn.close()

print("Fixed Pele and Rossi images!")
