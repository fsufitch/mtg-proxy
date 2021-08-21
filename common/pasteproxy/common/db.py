import sqlite3

class ScryfallDB:
    def __init__(self, path):
        self._db = sqlite3.connect(path)

    def num_cards(self):
        dbc = self._db.cursor()

        dbc.execute('SELECT COUNT(1) FROM cards');
        (count,) = dbc.fetchone()
        return count
