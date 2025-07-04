from http.client import responses
from services.booking.payload import PayloadBookings
from services.booking.endpoints import EndpointsBooking
from requests import Response
import requests
import allure


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
    def get_booking_by_id(self, id: int) -> Response:
        response = requests.get(
            url=self.endpoints.get_booking_by_id(id)
        )

        return response

    @allure.step('Auth request to get token')
    def get_auth_token(self) -> Response:
        data = {
            'username': self.payload.auth_data()[0],
            'password': self.payload.auth_data()[1]
        }
        response = requests.post(
            self.endpoints.create_token(), json=data
        )

        return response

    @allure.step('Post request to create booking')
    def create_booking(self, booking_id: int, **kwargs) -> Response:
        response = requests.post(
            url=self.endpoints.post_create_booking(booking_id),
            json=self.payload.post_booking_data(**kwargs)
        )
        return response

    @allure.step('Put request to update booking')
    def update_booking(self, booking_id: int, **kwargs):
        response = requests.post(
            url=self.endpoints.update_booking(booking_id),
            json=self.payload.post_booking_data(**kwargs)
        )
        return response

    @allure.step('Patch request to partial update booking')
    def partial_update_booking(self, booking_id: int, **kwargs):
        data = self.payload.patch_booking_data(**kwargs)
        response = requests.patch(
            url = self.endpoints.update_booking(booking_id),
            json = self.payload.patch_booking_data(**kwargs),
            auth = self.payload.basic_auth()
        )

    @allure.step('Delete booking request')
    def delete_booking(self, booking_id: int) -> Response:
        response = requests.delete(
            url=self.endpoints.delete_booking(booking_id)
        )
        return response
