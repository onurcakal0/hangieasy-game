import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'hangieasy@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('HangiEasy Merkez', 'hangieasy@gmail.com')

mail = Mail(app)

import threading

def send_in_thread(flask_app, message):
    with flask_app.app_context():
        try:
            mail.send(message)
            print("Thread içi mail gönderildi!")
        except Exception as e:
            print("Thread hatası:", str(e))

with app.app_context():
    msg = Message('Test Mail Thread', recipients=['test@example.com'])
    msg.body = "This is a test in thread."
    threading.Thread(target=send_in_thread, args=(app, msg), daemon=False).start()

