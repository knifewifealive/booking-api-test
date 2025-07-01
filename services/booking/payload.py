import requests
from requests import auth
import os
from dotenv import load_dotenv

load_dotenv()
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")


class PayloadBookings:

    @staticmethod
    def auth_data(login: str = LOGIN, password: str = PASSWORD) -> tuple:
        """
        Static method to keep auth data
        :param login: string login to get token or basic auth
        :param password: string password to get token or basic auth
        :return: tuple login, password
        """

        return login, password

    @staticmethod
    def basic_auth(login = LOGIN, password = PASSWORD):
        """
        Static method to auth with Basic Auth
        :param login: string login to get token or basic auth
        :param password: string password to get token or basic auth
        :return:
        """
        return requests.auth.HTTPBasicAuth(login, password)

    @staticmethod
    def post_booking_data(
            firstname: str,
            lastname: str,
            totalprice: float,
            depositpaid: bool,
            checkin: str,
            checkout: str,
            additionalneeds: str
    ) -> dict:
        """
        Can be used w Create and Update requests
        :param firstname:
Firstname for the guest who made the booking
        :param lastname: Lastname for the guest who made the booking
        :param totalprice: The total price for the booking
        :param depositpaid: Whether the deposit has been paid or not
        :param checkin: str, YYYY-MM-DD, Date the guest is checking in
        :param checkout: str, YYYY-MM-DD, Date the guest is checking out
        :param additionalneeds: Any other needs the guest has
        :return: dictionary with params above
        """
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": totalprice,
            "depositpaid": depositpaid,
            "bookingdates": {
                "checkin": checkin,
                "checkout": checkout
            },
            "additionalneeds": additionalneeds
        }

        return data

    @staticmethod
    def patch_booking_data(
            firstname: str = None,
            lastname: str = None,
            totalprice: float = None,
            depositpaid: bool = None,
            checkin: str = None,  # формат YYYY-MM-DD
            checkout: str = None,  # формат YYYY-MM-DD
            additionalneeds: str = None
    ) -> dict:
        """
        Can be used w PATCH requests
        :param firstname:
Firstname for the guest who made the booking
        :param lastname: Lastname for the guest who made the booking
        :param totalprice: The total price for the booking
        :param depositpaid: Whether the deposit has been paid or not
        :param checkin: str, YYYY-MM-DD, Date the guest is checking in
        :param checkout: str, YYYY-MM-DD, Date the guest is checking out
        :param additionalneeds: Any other needs the guest has
        :return: dictionary with not None params above
        """

        data = {}

        if firstname is not None:
            data["firstname"] = firstname
        if lastname is not None:
            data["lastname"] = lastname
        if totalprice is not None:
            data["totalprice"] = totalprice
        if depositpaid is not None:
            data["depositpaid"] = depositpaid
        if checkin or checkout:
            data["bookingdates"] = {}
            if checkin:
                data["bookingdates"]["checkin"] = checkin
            if checkout:
                data["bookingdates"]["checkout"] = checkout
        if additionalneeds is not None:
            data["additionalneeds"] = additionalneeds

        return data
