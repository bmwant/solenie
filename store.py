import attr
from tinydb import TinyDB, Query

from buttworld.logger import get_logger

logger = get_logger(__name__)


class DB(TinyDB):
    @property
    def name(self) -> str:
        return self._storage._handle.name


@attr.s
class Review(object):
    title: str = attr.ib()
    text: str = attr.ib()
    sentiment: int = attr.ib()
    link: str = attr.ib()


def _get_default_db():
    default_db = DB('data.json')
    return default_db


def insert_review(
    review: Review, *,
    dry_run=False,
    allow_duplicates=False,
    db: TinyDB=None,
):
    db = db or _get_default_db()
    if not allow_duplicates:
        query = Query()
        queryset = db.search(query.link == review.link)
        if queryset:
            raise ValueError(f'Duplicate record found {queryset}')

    if dry_run:
        logger.info(f'Inserting {review}...')
        return

    db.insert(attr.asdict(review))


def get_reviews(*, db: TinyDB=None) -> list:
    db = db or _get_default_db()
    query = Query()
    result = db.search(query.text.exists())
    logger.info('Loaded %s reviews', len(result))
    return result


def get_reviews_by_sentiment(sentiment, *, db: TinyDB=None):
    db = db or _get_default_db()
    logger.debug('Using %s database', db.name)
    query = Query()
    result = db.search(query.sentiment == sentiment)
    logger.info('Loaded %s records for %s sentiment', len(result), sentiment)
    return result
