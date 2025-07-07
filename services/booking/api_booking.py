import allure
import requests
from services.booking.payload import PayloadBookings, LOGIN, PASSWORD
from services.booking.endpoints import EndpointsBooking
from requests import Response


class Bookings:

    def __init__(self):
        self.payload = PayloadBookings
        self.endpoints = EndpointsBooking

    @allure.step('Get request for all available bookings')
    def get_all_bookings(self) -> Response:
        response = requests.get(
            url=self.endpoints.get_all_bookings()
        )
        return response

    @allure.step('Get request for booking by id')
    def get_booking_by_id(self, booking_id: int) -> Response:
        response = requests.get(
            url=self.endpoints.get_booking_by_id(booking_id)
        )

        return response

    @allure.step('Auth request to get token')
    def get_auth_token(self, login = LOGIN, password = PASSWORD) -> Response:
        data = {
            'login': login,
            'password': password
        }
        response = requests.post(
            self.endpoints.create_token(), json=data
        )

        return response

    @allure.step('Post request to create booking')
    def post_create_booking(self, **data) -> Response:
        response = requests.post(
            url=self.endpoints.post_create_booking(),
            json=self.payload.post_booking_data(**data)
        )
        return response

    @allure.step('Put request to update booking')
    def post_update_booking(self, booking_id: int, **data):
        response = requests.post(
            url=self.endpoints.update_booking(booking_id),
            json=self.payload.post_booking_data(**data),
            auth=self.payload.basic_auth()
        )
        return response

    @allure.step('Patch request to partial update booking')
    def partial_update_booking(self, booking_id: int, **data):
        data = self.payload.patch_booking_data(**data)
        response = requests.patch(
            url = self.endpoints.update_booking(booking_id),
            json = self.payload.patch_booking_data(**data),
            auth = self.payload.basic_auth()
        )

        return response

    @allure.step('Delete booking request')
    def delete_booking(self, booking_id: int) -> Response:
        response = requests.delete(
            url=self.endpoints.delete_booking(booking_id),
            auth=self.payload.basic_auth()
        )
        return response



