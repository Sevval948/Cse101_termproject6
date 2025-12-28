import unittest
import os
import json
import seating
import bookings


class TestCinemaSystem(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_data/'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        self.showtimes = [{
            "showtime_id": "ST_001",
            "movie_id": "M_001",
            "pricing_tier": "Standard"
        }]

        self.seat_maps = {
            "ST_001": {
                "A1": {"status": "available", "price": 100.0},
                "A2": {"status": "sold", "price": 100.0}
            }
        }

        self.bookings = [
            {
                "booking_id": "B_001",
                "showtime_id": "ST_001",
                "seats": ["A2"],
                "total_price": 100.0
            }
        ]

    def test_seat_availability(self):
        self.assertTrue(seating.is_seat_available(self.seat_maps["ST_001"], "A1"))
        self.assertFalse(seating.is_seat_available(self.seat_maps["ST_001"], "A2"))
        self.assertFalse(seating.is_seat_available(self.seat_maps["ST_001"], "Z99"))

    def test_booking_total_calculation(self):
        selected_seats = ["A1"]
        total = sum(self.seat_maps["ST_001"][s]["price"] for s in selected_seats)
        self.assertEqual(total, 100.0)

    def test_cancellation_path(self):
        booking_id = "B_001"
        success = bookings.cancel_booking(self.bookings, booking_id, self.seat_maps)

        self.assertTrue(success)
        self.assertEqual(len(self.bookings), 0)
        self.assertEqual(self.seat_maps["ST_001"]["A2"]["status"], "available")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)


if __name__ == '__main__':
    unittest.main()