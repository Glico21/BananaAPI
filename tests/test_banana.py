import pytest
from sqlalchemy.exc import IntegrityError

from application.models import Banana


def test__create_banana(database):
    # Case for banana creation
    color = "Yellow"
    origins = "New Guinea"
    banana = Banana(color=color, origins=origins)
    database.session.add(banana)
    database.session.commit()

    banana = Banana.query.first()

    assert banana.color == color
    assert banana.origins == origins

    # Case for banana creation count function
    another_banana = Banana(color=color, origins=origins)
    database.session.add(another_banana)
    database.session.commit()

    banana_count = Banana.query.count()

    assert banana_count == 2


def test__banana_with_empty_fields(database):
    color = "Yellow"
    origins = "New Guinea"

    # Case of banana creation with empty origin field
    banana = Banana(color=color)
    database.session.add(banana)
    database.session.commit()

    banana = Banana.query.first()

    assert banana.origins is None

    # Case of banana creation with empty color field
    another_banana = Banana(origins=origins)
    with pytest.raises(IntegrityError):
        database.session.add(another_banana)
        database.session.commit()
    database.session.rollback()


def test__all_banana_getting_endpoint(client, database):
    color = "Yellow"
    origins = "New Guinea"
    banana = Banana(color=color, origins=origins)

    # Case for success status of endpoint
    response = client.get('/banana/all')
    assert response.status_code == 200

    # Case for empty bananas list output
    assert response.get_json() == []

    # Case for correct banana list output
    database.session.add(banana)
    database.session.commit()

    response = client.get('/banana/all')
    expected_response = [{"id": 1, "color": "Yellow", "origins": "New Guinea"}]
    assert response.get_json() == expected_response
