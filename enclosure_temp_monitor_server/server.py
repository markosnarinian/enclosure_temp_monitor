from flask import Flask, request
from datetime import datetime
import sqlite3

conn = sqlite3.connect("enclosure_temp.sqlite")
cur = conn.cursor()

app = Flask(__name__)

@app.route("/exchange")
def exchange():
    x = datetime.now()

    cur.execute(f"INSERT INTO temperature (temp, temp_type, timestamp) VALUES ('{request.args['temp']}', 'enclosure_temp', '{datetime.timestamp(x)}')")
    conn.commit()

    return x.strftime("%a %d %b %H:%M")


app.run(
    host="192.168.1.12",
    port=50110,
    debug=True
    )

conn.close()
