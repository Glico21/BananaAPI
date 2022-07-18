import json

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
    first_color = "Yellow"
    second_color = "Black"
    origins = "New Guinea"
    first_banana = Banana(color=first_color, origins=origins)
    second_banana = Banana(color=second_color, origins=origins)

    # Case for success status of endpoint
    response = client.get('/banana')

    assert response.status_code == 200

    # Case for empty bananas list output
    assert response.get_json() == []

    # Cases for correct banana list output
    database.session.add(first_banana)
    database.session.commit()

    response = client.get('/banana')
    expected_response = [{"id": 1, "color": "Yellow", "origins": "New Guinea"}]

    assert response.get_json() == expected_response

    database.session.add(second_banana)
    database.session.commit()

    response = client.get('/banana')
    expected_response = [
        {"id": 1, "color": "Yellow", "origins": "New Guinea"},
        {"id": 2, "color": "Black", "origins": "New Guinea"}
    ]

    assert response.get_json() == expected_response


def test__banana_getting_endpoint(client, database):
    first_color = "Yellow"
    second_color = "Black"
    origins = "New Guinea"
    first_banana = Banana(color=first_color, origins=origins)
    second_banana = Banana(color=second_color, origins=origins)

    # Case for getting non-existent banana by id
    response = client.get('/banana/1')

    assert response.status_code == 404
    assert response.get_json() is None

    # Cases for success getting a specific banana
    database.session.add(first_banana)
    database.session.add(second_banana)
    database.session.commit()

    response = client.get('/banana/1')

    assert response.status_code == 200

    first_expected_response = {"id": 1, "color": "Yellow", "origins": "New Guinea"}

    assert response.get_json() == first_expected_response

    response = client.get('/banana/2')
    expected_response = {"id": 2, "color": "Black", "origins": "New Guinea"}

    assert response.get_json() == expected_response


def test__banana_creation_endpoint(client, database):
    color = "Yellow"
    origins = "New Guinea"
    empty_body = {}
    body = {
        "color": color,
        "origins": origins
    }

    # Case for adding empty body
    response = client.post('/banana',
                           data=json.dumps(empty_body),
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 400
    assert response.get_json() == {'Message': 'No input data provided'}

    # Case for adding wrong body
    wrong_body = {
        "origins": "New Guinea"
    }

    response = client.post('/banana',
                           data=json.dumps(wrong_body),
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 422
    assert response.get_json() == {'color': ['Missing data for required field.']}

    # Case for successfully creation of new banana
    response = client.post('/banana',
                           data=json.dumps(body),
                           headers={"Content-Type": "application/json"})

    expected_output = {"id": 1, "color": "Yellow", "origins": "New Guinea"}

    assert response.status_code == 201
    assert response.get_json() == expected_output


def test__banana_update_endpoint(client, database):
    color = "Yellow"
    origins = "New Guinea"
    banana = Banana(color=color, origins=origins)
    database.session.add(banana)
    database.session.commit()

    # Case for patch origins field
    update_body = {
        "origins": "Brazil"
    }

    response = client.patch('/banana/1',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    expected_output = {"id": 1, "color": "Yellow", "origins": "Brazil"}

    assert response.status_code == 200
    assert response.get_json() == expected_output

    # Case for patch color field
    update_body = {
        "color": "Black"
    }

    response = client.patch('/banana/1',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    expected_output = {"id": 1, "color": "Black", "origins": "Brazil"}

    assert response.status_code == 200
    assert response.get_json() == expected_output

    # Case for wrong banana id
    response = client.patch('/banana/2',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    expected_output = {"Message": "Not found banana with id: 2"}

    assert response.status_code == 404
    assert response.get_json() == expected_output

    # Case for patch empty data

    response = client.patch('/banana/1',
                            data=json.dumps({}),
                            headers={"Content-Type": "application/json"})

    assert response.status_code == 400
    assert response.get_json() == {"Message": "No input data provided"}

    # Case for irrelevant data

    irrelevant_body = {
        "origins": 123
    }
    response = client.patch('/banana/1',
                            data=json.dumps(irrelevant_body),
                            headers={"Content-Type": "application/json"})

    assert response.status_code == 422
    assert response.get_json() == {'origins': ['Not a valid string.']}


def test__banana_delete_endpoint(client, database):
    color = "Yellow"
    origins = "New Guinea"
    banana = Banana(color=color, origins=origins)
    database.session.add(banana)
    database.session.commit()

    # Case for removing existing banana
    response = client.delete('/banana/1')

    assert response.status_code == 204

    banana_count = Banana.query.count()
    assert banana_count == 0

    # Case for removing non-existing banana

    response = client.delete('/banana/1')
    expected_output = {"Message": "Not found banana with id: 1"}

    assert response.status_code == 404
    assert response.get_json() == expected_output
