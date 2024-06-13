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

test_update_data = (
    (
        {
            TEMP: 26,
            HUM: 66,
            PRES: 762,
            CREATED: 'Thu, 13 Jun 2024 13:44:55 GMT',
        },
        204,
    ),
    (
        {
            HUM: 66,
            PRES: 762,
            CREATED: 'Thu, 13 Jun 2024 13:44:55 GMT',
        },
        500,
    ),
)


@pytest.mark.parametrize('json_create, valid_json', test_create)
def test_create_func(json_create: dict, valid_json: tuple) -> None:
    """REST create and get test.

    Args:
        json_create (dict): create sample
        valid_json (tuple): get sample
    """
    requests.post(
        'http://localhost:5000/meteodata/create', json=json_create, timeout=TOUT,
    )
    response = requests.get('http://localhost:5000/meteodata/get', timeout=TOUT)
    response = {key: value for key, value in response.json()[0].items() if key != 'id'}
    valid_json = {key: value for key, value in valid_json[0].items() if key != 'id'}
    assert response == valid_json


@pytest.mark.parametrize('sample, code', test_update_data)
def test_update(sample: dict, code: int) -> None:
    """REST update test.

    Args:
        sample (dict): put json example
        code (int): awatied response code
    """
    response = requests.get('http://localhost:5000/meteodata/get', timeout=TOUT).json()
    response_id = response[0]['id']
    response_code = requests.put(
        'http://127.0.0.1:5000/meteodata/update',
        json={'id': response_id} | sample,
        timeout=TOUT,
        ).status_code
    assert response_code == code


@pytest.mark.parametrize('status_code', test_delete)
def test_delete_func(status_code: int) -> None:
    """REST delete test.

    Args:
        status_code (int): awaited response code
    """
    response = requests.get('http://localhost:5000/meteodata/get', timeout=TOUT).json()
    response_id = response[0]['id']
    response_code = requests.delete(
        'http://127.0.0.1:5000/meteodata/delete',
        json={'id': response_id},
        timeout=TOUT,
        ).status_code
    assert response_code == status_code
