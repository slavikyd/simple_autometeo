"""Api testing module."""
import datetime

import pytest
import requests

today = datetime.datetime.today()

ID = 'id'
TEMP = 'temperature'
HUM = 'humidity'
PRES = 'pressure'
CREATED = 'created'
TOUT = 120

test_create = (
    (
        {
            ID: '6860be52-9d32-4fe5-9c17-f843835657cc',
            TEMP: 25,
            HUM: 60,
            PRES: 760,
            CREATED: datetime.datetime.today().__str__(),
        },
        [
            {
                CREATED: datetime.datetime.today().strftime(
                    '%a, %d %b %Y %H:%M:%S GMT',
                ),
                ID: 'Any',
                TEMP: 25.0,
                HUM: 60.0,
                PRES: 760.0,
            },
        ],
    ),
)

test_delete = (204,)


@pytest.mark.parametrize('json_create, valid_json', test_create)
def test_create_func(json_create: dict, valid_json: tuple) -> None:
    """REST create and get test.

    Args:
        json_create (dict): create sample
        valid_json (tuple): get sample
    """
    requests.post(
        'http://localhost:5000/inner/meteodata/create', json=json_create, timeout=TOUT,
    )
    response = requests.get('http://localhost:5000/inner/meteodata/get', timeout=TOUT).json()
    response = {key: value for key, value in response[0].items() if key != 'id'}
    valid_json[0] = {key: value for key, value in valid_json[0].items() if key != 'id'}
    assert response == valid_json[0]


@pytest.mark.parametrize('status_code', test_delete)
def test_delete_func(status_code: int) -> None:
    """REST delete test.

    Args:
        status_code (int): awaited response code
    """
    response = requests.get('http://localhost:5000/inner/meteodata/get', timeout=TOUT).json()
    response_id = response[0]['id']
    response_code = requests.delete(
        'http://127.0.0.1:5000/inner/meteodata/delete',
        json={'id': response_id},
        timeout=TOUT,
        ).status_code
    assert response_code == status_code
