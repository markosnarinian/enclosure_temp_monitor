from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/exchange")
def exchange():
    x = datetime.now()
    return x.strftime("%a %d %b %H:%M")


app.run(
    host="192.168.1.11",
    port=50110,
    debug=True
    )