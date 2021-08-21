import os
from flask import Flask
from pasteproxy.common.db import ScryfallDB

app = Flask(__name__)

db_path = os.getenv('CARDS_DB')


@app.route("/")
def hello_world():
    db = ScryfallDB(db_path)
    return f"<p>Hello, World! There are {db.num_cards()} cards in the Scryfall database. </p>"
