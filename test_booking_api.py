from http.client import responses

from basetest import BaseTest
from services.booking.payload import PayloadBookings, LOGIN, PASSWORD

class TestBookingApi(BaseTest):

    def test_get_bookings_id(self, load_dv):

        response = self.booking.get_all_bookings()
        assert response.status_code == 200, response.json()