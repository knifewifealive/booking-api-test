BASE_URL = 'https://restful-booker.herokuapp.com/'
BOOKING_URL = BASE_URL + 'booking/'
AUTH_URL = BASE_URL + 'auth'


class EndpointsBooking:

    @staticmethod
    def get_all_bookings() -> str:
        """

        :return: get url string for all bookings
        """
        return f'{BOOKING_URL}'

    @staticmethod
    def get_booking_by_id(booking_id: int) -> str:
        """

        :param booking_id: int, booking id
        :return: GET url-string for api request
        """
        return f'{BOOKING_URL}{booking_id}'

    @staticmethod
    def create_token() -> str:
        """

        :return: POST url-string for api request
        """
        return f'{AUTH_URL}'

    @staticmethod
    def post_create_booking() -> str:
        """

        :param booking_id: int, booking id
        :return: POST url-string for api request
        """
        return f'{BOOKING_URL}'

    @staticmethod
    def update_booking(booking_id: int) -> str:
        """
        Can be used for PATCH request
        :param booking_id: int, booking id
        :return: PUT url-string for api request
        """
        return f'{BOOKING_URL}{booking_id}'

    @staticmethod
    def delete_booking(booking_id: int) -> str:
        """
        Can be used for Delete request
        :param booking_id: int, booking id
        :return: DELETE url-string for api request
        """
        return f'{BOOKING_URL}{booking_id}'