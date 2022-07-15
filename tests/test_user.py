import pytest

from sqlalchemy.exc import IntegrityError

from application.models import User


def test__create_user(database):
    # Case for creation query
    email = "some.email@server.com"
    user = User(email=email)
    database.session.add(user)
    database.session.commit()

    user = User.query.first()

    assert user.email == email

    users_count = User.query.count()

    assert users_count == 1

    # Case for unique email field
    another_user = User(email=email)
    with pytest.raises(IntegrityError):
        database.session.add(another_user)
        database.session.commit()
    database.session.rollback()

    # Case for nullable email field
    another_user = User()
    with pytest.raises(IntegrityError):
        database.session.add(another_user)
        database.session.commit()
    database.session.rollback()


def test__users_count(database):
    # Cases for user count function
    first_email = "some.email@server.com"
    second_email = "another.email@server.com"
    first_user = User(email=first_email)
    second_user = User(email=second_email)

    database.session.add(first_user)
    users_count = User.query.count()

    assert users_count == 1

    database.session.add(second_user)
    database.session.commit()

    users_count = User.query.count()

    assert users_count == 2


def test__users_count_endpoint(client, database):
    # Case for success status of endpoint
    response = client.get('/users')
    assert response.status_code == 200

    # Case for correct empty output
    assert response.get_json() == {'Number of users': 0}

    # Case for correct output after user creation
    email = "some.email@server.com"
    user = User(email=email)
    database.session.add(user)
    database.session.commit()

    response = client.get('/users')
    assert response.get_json() == {'Number of users': 1}
