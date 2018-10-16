import attr
from tinydb import TinyDB, Query


db = TinyDB('data.json')


@attr.s
class Review(object):
    title: str = attr.ib()
    text: str = attr.ib()
    sentiment: int = attr.ib()
    link: str = attr.ib()


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
