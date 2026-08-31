import os
import threading
from flask import Flask

app = Flask("")

@app.route("/")
def home():
    return "Hello, World! Bot is running."

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()