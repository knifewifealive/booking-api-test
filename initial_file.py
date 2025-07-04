from requests import auth
import requests
import pytest

BASE_URL = 'https://restful-booker.herokuapp.com/'
BOOKING_URL = BASE_URL + 'booking/'
AUTH_URL = BASE_URL + 'auth'

client_auth = requests.auth.HTTPBasicAuth("admin", "password123")

@pytest.fixture()
def booking_id():
    data = {
      "firstname": "Mark",
      "lastname": "Bybin",
      "totalprice": 100,
      "depositpaid": True,
      "bookingdates": {
        "checkin": "2025-06-27",
        "checkout": "2025-06-29"
      },
      "additionalneeds": "Sleeping Bag"
    }
    response = requests.post(BOOKING_URL, json=data).json()
    yield response['bookingid']
    requests.delete(f'{BOOKING_URL}{response['bookingid']}')


def test_get_booking(booking_id):
    response = requests.get(BOOKING_URL + str(booking_id))
    assert response.status_code == 200

def test_create_booking():
    data = {
      "firstname": "Mark",
      "lastname": "Bybin",
      "totalprice": 100,
      "depositpaid": True,
      "bookingdates": {
        "checkin": "2025-06-27",
        "checkout": "2025-06-29"
      },
      "additionalneeds": "Sleeping Bag"
    }
    response = requests.post(BOOKING_URL, json=data).json()
    assert (response['booking']['firstname'] == data['firstname']) and (response['booking']['lastname'] == data['lastname'])

def test_create_token():
    data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(AUTH_URL, json=data)
    if response.status_code != 200:
        raise Exception(f"Auth failed: {response.status_code}, {response.text}")
    assert response.status_code == 200

def test_update_booking(booking_id):
    data = {
        "firstname": "Natalia",
        "lastname": "Sholudkova",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-27",
            "checkout": "2025-06-30"
        },
        "additionalneeds": "Iqos"
    }

    response = requests.put(BOOKING_URL + str(booking_id), json=data, auth=client_auth).json()
    assert (response['firstname'] == data['firstname']) and (response['lastname'] == data['lastname'])

def test_delete_booking(booking_id):
    response = requests.delete(f'{BOOKING_URL}{booking_id}', auth=client_auth)
    response = requests.get(f'{BOOKING_URL}{booking_id}')
    assert response.status_code == 404


