from services.booking.payload import PayloadBookings as PLB
from services.booking.endpoints import EndpointsBooking as EPB
import allure
import pytest
import random
import requests
from basetest import BaseTest



class TestBookingApi(BaseTest):

    @pytest.fixture(scope="function")
    def create_and_delete_booking(self):
        data = PLB.post_booking_data(
            firstname='mark',
            lastname='bybin',
            totalprice=150,
            depositpaid=True,
            bookingdates={
                'checkin': '2025-07-25',
                'checkout': '2025-07-30'
            },
            additionalneeds='Nothing'
        )
        response = requests.post(EPB.post_create_booking(), json=data).json()
        yield response['bookingid']
        requests.delete(f'{EPB.delete_booking(response['bookingid'])}')
        print(f'Удалено бронирование с Id: {response['bookingid']}')

    def test_get_bookings(self):
        response = self.booking.get_all_bookings()
        assert response.status_code == 200, response.json()

    @pytest.mark.api_positive
    @pytest.mark.parametrize('booking_id', [x for x in range(1, 4)])
    def test_get_booking_positive(self, booking_id):
        response = self.booking.get_booking_by_id(booking_id)
        assert response.status_code == 200, response.json()

    @pytest.mark.api_negative
    @pytest.mark.parametrize('case, data',
                             (
                                     ("Negative number", [random.randint(-1000, -1) for _ in range(2)]),
                                     ("Number more than 10 000", [random.randint(10000, 100000) for _ in range(2)])
                             ))
    def test_get_booking_negative(self, case, data):
        allure.dynamic.title(case)
        response = self.booking.get_booking_by_id(data)
        assert response.status_code == 404, response.json()

    @pytest.mark.api_positive
    def test_get_auth_token_positive(self):
        response = self.booking.get_auth_token()
        assert response.status_code == 200, response.json()

    @pytest.mark.api_negative
    @pytest.mark.parametrize(
        'login, password',
        [
            ('wrong_login', 'password123'),
            ('admin', 'wrong_password'),
            ('wrong_login', 'wrong_password'),
        ]
    )
    def test_get_auth_token_negative(self, login, password):
        response = self.booking.get_auth_token(login=login, password=password)
        assert response.status_code == 200, response.json()['reason'] == 'Bad credentials'

    @pytest.mark.api_positive
    @pytest.mark.parametrize('data', [

        {
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

    ])
    def test_post_create_booking_positive(self, data):
        response = self.booking.post_create_booking(**data)
        assert response.status_code == 200, response.json()

    @pytest.mark.api_negative
    @pytest.mark.parametrize('case,data', [

        ("String totalprice",{
            "firstname": "Mark",
            "lastname": "Bybin",
            "totalprice": 'asdffdsafdsa',
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-06-27",
                "checkout": "2025-06-29"
            },
            "additionalneeds": "Sleeping Bag"
        }),
        ("String depositpaid", {
            "firstname": "Mark",
            "lastname": "Bybin",
            "totalprice": 150,
            "depositpaid": 'String depositpaid',
            "bookingdates": {
                "checkin": "2025-06-27",
                "checkout": "2025-06-29"
            },
            "additionalneeds": "Sleeping Bag"
        })
    ])
    def test_post_create_booking_negative(self, case,data):
        allure.dynamic.title(case)
        response = self.booking.post_create_booking(**data)
        assert response.status_code == 200, response.json()

    @pytest.mark.api_positive
    @pytest.mark.parametrize(
        'case,data',
        [
            ('Positive case',PLB.post_booking_data(
            firstname='mark',
            lastname='bybin',
            totalprice=200,
            depositpaid=True,
            bookingdates={'checkin': '2025-07-08', 'checkout': '2025-07-10'},
            additionalneeds='Nothing'
        ))
        ]
    )
    def test_update_booking_positive(self, create_and_delete_booking, case, data):
        allure.dynamic.title(case)
        response = self.booking.put_update_booking(create_and_delete_booking,**data)
        assert response.status_code == 200, response.json()

    @pytest.mark.api_negative
    @pytest.mark.parametrize(
        'case,data',
        [
            ('Negative case w string total_price', PLB.post_booking_data(
                firstname='mark',
                lastname='bybin',
                totalprice='hellototal',
                depositpaid=True,
                bookingdates={'checkin': '2025-07-08', 'checkout': '2025-07-10'},
                additionalneeds='Nothing'
            )),
            ('Negative case w string total_price', PLB.post_booking_data(
                firstname='mark',
                lastname='bybin',
                totalprice=200,
                depositpaid='hellodeposit',
                bookingdates={'checkin': '2025-07-08', 'checkout': '2025-07-10'},
                additionalneeds='Nothing'
            ))
        ]
    )
    def test_update_booking_negative(self, create_and_delete_booking, case, data):
        allure.dynamic.title(case)
        response = self.booking.put_update_booking(create_and_delete_booking, **data)
        assert response.status_code == 200, response.json()


    @pytest.mark.api_positive
    @pytest.mark.parametrize(
        'case, data',
        [
            ('Positive case w 3 fields', PLB.patch_booking_data(
                firstname='mark',
                bookingdates={'checkin': '2025-07-26', 'checkout': '2025-07-30'},
                additionalneeds='Nothing'
            )),
            ('Positive case w 4 fields', PLB.patch_booking_data(
                lastname='watson',
                depositpaid=False,
                bookingdates={'checkin': '2028-07-26', 'checkout': '2028-07-30'},
                additionalneeds='WiFi, Coke and laptop'
            ))
        ]
    )
    def test_patch_booking_positive(self, create_and_delete_booking, case, data):
        allure.dynamic.title(case)
        response = self.booking.partial_update_booking(create_and_delete_booking, **data)
        assert response.status_code == 200, response.json()

    @pytest.mark.wip
    @pytest.mark.parametrize(
        'case, data',
        [
            ('Negative case w wrong dates', PLB.patch_booking_data(
                firstname='mark',
                bookingdates={'checkin': '2023-07-26', 'checkout': '2021-07-30'},
                additionalneeds='Nothing'
            )),
            ('Negative case w incorrect last and firstname', PLB.patch_booking_data(
                firstname='fjds;aljsdklfaskdhfsdjkfhas;413212412fdsakhjfads;klhfds;akhlgajskd;',
                lastname='fsda;lkghdsapoaisdhgsadopsgdsagd[dfsan;fdslkjfsda',
                depositpaid=False,
                bookingdates={'checkin': '2028-07-26', 'checkout': '2028-07-30'},
                additionalneeds='WiFi, Coke and laptop'
            ))
        ]
    )
    def test_patch_booking_negative(self, create_and_delete_booking, case, data):
        allure.dynamic.title(case)
        response = self.booking.partial_update_booking(create_and_delete_booking, **data)
        assert response.status_code == 200, response.json()
