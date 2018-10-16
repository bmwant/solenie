import attr
from tinydb import TinyDB, Query

from buttworld.logger import get_logger


db = TinyDB('data.json')
logger = get_logger(__name__)


@attr.s
class Review(object):
    title: str = attr.ib()
    text: str = attr.ib()
    sentiment: int = attr.ib()
    link: str = attr.ib()


def insert_review(review: Review, *, dry_run=False, allow_duplicates=False):
    if not allow_duplicates:
        query = Query()
        queryset = db.search(query.link == review.link)
        if queryset:
            raise ValueError(f'Duplicate record found {queryset}')

    if dry_run:
        logger.info(f'Inserting {review}...')
        return

    db.insert(attr.asdict(review))
