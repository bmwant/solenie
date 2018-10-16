import attr
from tinydb import TinyDB, Query


db = TinyDB('data.json')


@attr.s
class Review(object):
    title: str = attr.ib()
    text: str = attr.ib()
    sentiment: int = attr.ib()
    link: str = attr.ib()


def insert_review(review: Review, *, dry_run=False):
    if dry_run:
        print(f'Inserting {review}...')
        return

    db.insert(attr.asdict(review))
