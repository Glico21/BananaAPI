import json

from datetime import datetime

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


def test__palm_getting_endpoint(database, client):
    # Palms attributes
    first_location = "New Guinea"
    first_created_at = "2011-01-01 00:00:00"
    first_max_banana_in_bundle = 2
    second_location = "Brazil"
    second_created_at = "2015-01-01 00:00:00"
    second_max_banana_in_bundle = 3

    first_palm = Palm(location=first_location,
                      created_at=first_created_at,
                      max_banana_in_bundle=first_max_banana_in_bundle)
    second_palm = Palm(location=second_location,
                       created_at=second_created_at,
                       max_banana_in_bundle=second_max_banana_in_bundle)

    # Case for getting non-existent palm by id
    response = client.get('/palms/1')

    assert response.status_code == 404
    assert response.get_json() is None

    # Cases for success getting a specific palm
    database.session.add(first_palm)
    database.session.add(second_palm)
    database.session.commit()

    response = client.get('/palms/1')

    assert response.status_code == 200

    first_expected_response = {"id": 1, "location": "New Guinea",
                               "created_at": "2011-01-01T00:00:00", "max_banana_in_bundle": 2}
    second_expected_response = {"id": 2, "location": "Brazil",
                                "created_at": "2015-01-01T00:00:00", "max_banana_in_bundle": 3}

    assert response.get_json() == first_expected_response

    response = client.get('/palms/2')

    assert response.get_json() == second_expected_response


def test__palm_delete_endpoint(client, database):
    # Palms attributes
    location = "New Guinea"
    created_at = "2011-01-01 00:00:00"
    max_banana_in_bundle = 2
    palm = Palm(location=location, created_at=created_at, max_banana_in_bundle=max_banana_in_bundle)
    database.session.add(palm)
    database.session.commit()

    # Case for removing existing palm
    response = client.delete('/palms/1')

    assert response.status_code == 204

    palm_count = Palm.query.count()
    assert palm_count == 0

    # Case for removing non-existing palm

    response = client.delete('/palms/1')
    expected_output = {"Message": "Not found palm with id: 1"}

    assert response.status_code == 404
    assert response.get_json() == expected_output


def test__palm_creation_endpoint(client, database):
    location = "New Guinea"
    age = 7
    max_banana_in_bundle = 2
    empty_body = {}
    body = {
        "location": location,
        "age": age,
        "max_banana_in_bundle": max_banana_in_bundle
    }

    # Case for adding empty body
    response = client.post('/palms',
                           data=json.dumps(empty_body),
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 400
    assert response.get_json() == {'Message': 'No input data provided'}

    # Cases for adding wrong body
    first_wrong_body = {
        "location": location,
        "age": age
    }
    second_wrong_body = {
        "age": age
    }
    third_wrong_body = {
        "origins": "New Guinea",
        "max_banana_in_bundle": max_banana_in_bundle
    }

    response = client.post('/palms',
                           data=json.dumps(first_wrong_body),
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 422
    assert response.get_json() == {'max_banana_in_bundle': ['Missing data for required field.']}

    response = client.post('/palms',
                           data=json.dumps(second_wrong_body),
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 422
    assert response.get_json() == {'location': ['Missing data for required field.']}

    response = client.post('/palms',
                           data=json.dumps(third_wrong_body),
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 422
    assert response.get_json() == {'location': ['Missing data for required field.']}

    # Case for success creation and age to datetime converting
    now = datetime.now()

    response = client.post('/palms',
                           data=json.dumps(body),
                           headers={"Content-Type": "application/json"})

    output = response.get_json()

    assert response.status_code == 201
    assert output['location'] == "New Guinea"
    assert output['max_banana_in_bundle'] == 2

    created_data = datetime.strptime(output['created_at'], '%Y-%m-%dT%H:%M:%S')
    assert created_data.year == now.year - age


def test__palm_update_endpoint(client, database):
    location = "New Guinea"
    created_at = "2011-01-01 00:00:00"
    max_banana_in_bundle = 2
    palm = Palm(location=location, created_at=created_at, max_banana_in_bundle=max_banana_in_bundle)
    database.session.add(palm)
    database.session.commit()

    response = client.get('/palms/1')

    assert response.status_code == 200

    # Case for patch location field
    update_body = {
        "location": "Brazil"
    }

    response = client.patch('/palms/1',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    expected_output = {"id": 1, "location": "Brazil", "created_at": "2011-01-01T00:00:00", "max_banana_in_bundle": 2}

    assert response.status_code == 200
    assert response.get_json() == expected_output

    # Case for patch max_banana_in_bundle field
    update_body = {
        "max_banana_in_bundle": 3
    }

    response = client.patch('/palms/1',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    expected_output = {"id": 1, "location": "Brazil", "created_at": "2011-01-01T00:00:00", "max_banana_in_bundle": 3}

    assert response.status_code == 200
    assert response.get_json() == expected_output

    # Case for update created_at field
    age = 10
    update_body = {
        "age": age
    }

    response = client.patch('/palms/1',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    output = response.get_json()

    assert response.status_code == 200
    assert output['location'] == "Brazil"
    assert output['max_banana_in_bundle'] == 3

    now = datetime.now()
    created_data = datetime.strptime(output['created_at'], '%Y-%m-%dT%H:%M:%S')
    assert created_data.year == now.year - age

    # Case for wrong palm id
    response = client.patch('/palms/2',
                            data=json.dumps(update_body),
                            headers={"Content-Type": "application/json"})
    expected_output = {"Message": "Not found palm with id: 2"}

    assert response.status_code == 404
    assert response.get_json() == expected_output

    # Case for patch empty data

    response = client.patch('/palms/1',
                            data=json.dumps({}),
                            headers={"Content-Type": "application/json"})

    assert response.status_code == 400
    assert response.get_json() == {"Message": "No input data provided"}

    # Case for irrelevant data

    irrelevant_body = {
        "max_banana_in_bundle": 'wrong'
    }
    response = client.patch('/palms/1',
                            data=json.dumps(irrelevant_body),
                            headers={"Content-Type": "application/json"})

    assert response.status_code == 422
    assert response.get_json() == {'max_banana_in_bundle': ['Not a valid integer.']}


def test__all_banana_getting_endpoint(client, database):
    first_location = "New Guinea"
    second_location = "Brazil"
    first_created_at = "2011-01-01 00:00:00"
    second_created_at = "2021-01-01 00:00:00"
    first_max_banana_in_bundle = 2
    second_max_banana_in_bundle = 42
    first_palm = Palm(location=first_location,
                      created_at=first_created_at,
                      max_banana_in_bundle=first_max_banana_in_bundle)
    second_palm = Palm(location=second_location,
                      created_at=second_created_at,
                      max_banana_in_bundle=second_max_banana_in_bundle)

    # Case for success status of endpoint
    response = client.get('/palms')

    assert response.status_code == 200

    # Case for empty palms list output
    assert response.get_json() == []

    # Cases for correct palms list output
    database.session.add(first_palm)
    database.session.commit()

    response = client.get('/palms')
    expected_response = [{"id": 1,
                          "location": "New Guinea",
                          "created_at": "2011-01-01T00:00:00",
                          "max_banana_in_bundle": 2}]

    assert response.get_json() == expected_response

    database.session.add(second_palm)
    database.session.commit()

    response = client.get('/palms')
    expected_response = [
        {"id": 1, "location": "New Guinea", "created_at": "2011-01-01T00:00:00", "max_banana_in_bundle": 2},
        {"id": 2, "location": "Brazil", "created_at": "2021-01-01T00:00:00", "max_banana_in_bundle": 42}
    ]

    assert response.get_json() == expected_response
