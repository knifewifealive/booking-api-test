from services.booking.api_booking import Bookings


class BaseTest:

    def setup_method(self):

        self.booking = Bookings()