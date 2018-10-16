import pytest
from tinydb import Query

from store import db
from store import Review, insert_review


def test_inserting_duplicates():
    review = Review(
        title='t1',
        text='text1',
        sentiment=1,
        link='http://example.com/review1',
    )

    insert_review(review)
    with pytest.raises(ValueError):
        insert_review(review, allow_duplicates=False)


def test_search():
    ReviewQ = Query()
    r = db.search(ReviewQ.title == 't1')
    # r = db.get(doc_id=1)
    print(r)
