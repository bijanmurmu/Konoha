from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive and running!"

def run():
    # Render assigns a dynamic port, so we listen to 0.0.0.0
    app.run(host='0.0.0.0', port=0)

def keep_alive():
    t = Thread(target=run)
    t.start()
