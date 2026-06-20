from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "Konoha System is ONLINE!"

def run():
    # Render requires the app to bind to the port specified in the PORT env var.
    # If PORT is not found (e.g. running locally), it falls back to port 8080.
    port = int(os.environ.get("PORT", 8080))
    try:
        app.run(host='0.0.0.0', port=port)
    except OSError:
        # Fallback for local Windows testing if 8080 is blocked
        print(f"Port {port} is busy. Binding to random port for local test...")
        app.run(host='0.0.0.0', port=0)

def keep_alive():
    t = Thread(target=run)
    t.start()
