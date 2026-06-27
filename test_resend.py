import os
import urllib.request
import json
import urllib.error
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('RESEND_API_KEY')
print("API Key:", "VAR" if api_key else "YOK")
