import json

import pytest


def test__hello_world_endpoint(client):
    # Case hello-world endpoint
    response = client.get('/')

    assert response.status_code == 200
    assert response.get_json() == "Hello, World!"
