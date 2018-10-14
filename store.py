from tinydb import TinyDB, Query


db = TinyDB('data.json')


def insert_review(title, text, sentiment, link, *, dry_run=False):
    if dry_run:
        print(f'Inserting {title}({link}) {sentiment} review...')
        return

    db.insert({
        'title': title,
        'text': text,
        'sentiment': sentiment,
        'link': link,
    })
