import json

import pytest
from sqlalchemy.exc import IntegrityError

from application.models import Palm, Banana


def test__create_palm(database):
    # Case for palm creation
    location = "New Guinea"
    created_at = "2011-01-01 00:00:00"
    max_banana_in_bundle = 2
    palm = Palm(location=location, created_at=created_at, max_banana_in_bundle=max_banana_in_bundle)

    database.session.add(palm)
    database.session.commit()

    palm = Palm.query.first()

    assert palm.location == location
    assert str(palm.created_at) == created_at
    assert palm.max_banana_in_bundle == max_banana_in_bundle

    # Case for palm creation count function
    another_palm = Palm(location=location, created_at=created_at, max_banana_in_bundle=max_banana_in_bundle)
    database.session.add(another_palm)
    database.session.commit()

    palm_count = Palm.query.count()

    assert palm_count == 2


def test__banana_with_empty_fields(database):
    location = "New Guinea"
    created_at = "2011-01-01 00:00:00"
    max_banana_in_bundle = 2

    # Case of palm creation with empty created_at field
    palm = Palm(location=location, max_banana_in_bundle=max_banana_in_bundle)
    database.session.add(palm)
    database.session.commit()

    palm = palm.query.first()

    assert palm.created_at is None

    # Case of palm creation with empty location field
    second_palm = Palm(created_at=created_at, max_banana_in_bundle=max_banana_in_bundle)
    with pytest.raises(IntegrityError):
        database.session.add(second_palm)
        database.session.commit()
    database.session.rollback()

    # Case of palm creation with empty max_banana_in_bundle field
    third_palm = Palm(created_at=created_at, location=location)
    with pytest.raises(IntegrityError):
        database.session.add(third_palm)
        database.session.commit()
    database.session.rollback()


def test__palm_with_banana(database):
    # Palm attributes
    location = "New Guinea"
    created_at = "2011-01-01 00:00:00"
    max_banana_in_bundle = 2

    # Banana attributes
    color = "Yellow"
    palm_id = 1

    # Case of creation palm tree and a banana and the connections between them
    palm = Palm(location=location, created_at=created_at, max_banana_in_bundle=max_banana_in_bundle)

    database.session.add(palm)
    database.session.commit()

    banana = Banana(color=color, palm=palm_id)

    database.session.add(banana)
    database.session.commit()

    assert banana.palm == palm.id
    assert banana.id == palm.bananas.first().id
