import os
import sys
import json
import sqlite3
import time
from yaspin import yaspin

db = sqlite3.connect(os.getenv('DB_PATH'))
dbc = db.cursor()

dbc.executescript('''
    CREATE TABLE IF NOT EXISTS cards (
        id text not null,
        lang text not null,
        oracle_id text not null,
        uri text not null,
        rulings_uri text not null,
        scryfall_uri text not null,
        has_faces integer not null,

        name text not null,
        oracle_text text not null,
        type_line text not null,

        collector_number text not null,
        set_ text not null,
        image_large_url text not null,
        image_normal_url text not null,
        image_small_url text not null,

        printed_name text,
        printed_text text,
        printed_type_line text,   

        released_at text not null
    );

    CREATE UNIQUE INDEX idx_cards_id ON cards(id);

    CREATE INDEX idx_cards_lang ON cards(lang);
    CREATE INDEX idx_cards_oracle_id ON cards(oracle_id);
    CREATE INDEX idx_cards_name ON cards(name);
    CREATE INDEX idx_cards_oracle_text ON cards(oracle_text);
    CREATE INDEX idx_cards_type_line ON cards(type_line);
    CREATE INDEX idx_cards_collector_number ON cards(collector_number);
    CREATE INDEX idx_cards_set ON cards(set_);
    CREATE INDEX idx_cards_released_at ON cards(released_at);
''')

class Progress:
    def __init__(self):
        self.cards = 0
        self.start = time.time()
    def __str__(self):
        return 'Indexed {} cards; Elapsed: {:.2f} seconds'.format(self.cards, time.time()-self.start)

progress = Progress()
spinner = yaspin(text=progress)
spinner.start()

for line in sys.stdin:
    data = json.loads(line)

    image_large_url = ''
    image_normal_url = ''
    image_small_url = ''
    if 'image_uris' in data:
        image_small_url = data.get('image_uris', {}).get('small', '')
        image_normal_url = data.get('image_uris', {}).get('normal', '') or image_small_url
        image_large_url = data.get('image_uris', {}).get('large', '') or image_normal_url

    dbc.execute(f'''
        INSERT INTO cards (id, lang, oracle_id, uri, rulings_uri, scryfall_uri, 
            has_faces, name, oracle_text, type_line, collector_number, set_, 
            image_large_url, image_normal_url, image_small_url, printed_name,
            printed_text, printed_type_line, released_at)
            VALUES ({', '.join(["?"]*19)})
            ON CONFLICT DO NOTHING;
    ''', (
    
        data['id'],
        data['lang'],
        data['oracle_id'],
        data['uri'],
        data['rulings_uri'],
        data['scryfall_uri'],
        len(data.get('card_faces', [])) > 1,
        data.get('name', ''),
        data.get('oracle_text', ''),
        data.get('type_line', ''),
        data['collector_number'],
        data['set'],
        image_large_url,
        image_normal_url,
        image_small_url,
        data.get('printed_name', ''),
        data.get('printed_text', ''),
        data.get('printed_type_line', ''),
        data['released_at'],
        )
    )

    progress.cards += 1

spinner.text = f'Committing {progress.cards} cards to DB...'
db.commit()
db.close()
spinner.stop()

print('Wrote {} cards to DB in {:.2f} seconds.'.format(progress.cards, time.time()-progress.start))