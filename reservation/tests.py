import unittest
import datetime
import io
from court_reservation import Reservation
from data_handler import DataHandler
from unittest.mock import patch
from converters import DateTimeConverter


class TestDateTimeConverter(unittest.TestCase):
    def test_convert_string_to_date(self):
        string_date = "23.03.2023"
        expected_date = datetime.date(2023, 3, 23)
        actual_date = DateTimeConverter.convert_string_to_date(string_date)
        self.assertEqual(actual_date, expected_date)

    def test_convert_string_to_time(self):
        string_time = "12:30"
        expected_time = datetime.time(12, 30)
        actual_time = DateTimeConverter.convert_string_to_time(string_time)
        self.assertEqual(actual_time, expected_time)

    def test_convert_string_to_date_time(self):
        string_date_time = "23.03.2023 12:30"
        expected_date_time = datetime.datetime(2023, 3, 23, 12, 30)
        actual_date_time = DateTimeConverter.convert_string_to_date_time(
            string_date_time
        )
        self.assertEqual(actual_date_time, expected_date_time)

    def test_get_string_time(self):
        date_time = datetime.datetime(2023, 3, 23, 12, 30)
        expected_time_string = "12:30"
        actual_time_string = DateTimeConverter.get_string_time(date_time)
        self.assertEqual(actual_time_string, expected_time_string)

    def test_get_string_date(self):
        date_time = datetime.datetime(2023, 3, 23, 12, 30)
        expected_date_string = "23.03.2023"
        actual_date_string = DateTimeConverter.get_string_date(date_time)
        self.assertEqual(actual_date_string, expected_date_string)

    def test_convert_time_to_datetime(self):
        date = datetime.datetime(2023, 3, 23)
        time_to_convert = datetime.time(12, 30)
        expected_date_time = datetime.datetime(2023, 3, 23, 12, 30)
        actual_date_time = DateTimeConverter.convert_time_to_datetime(
            date, time_to_convert
        )
        self.assertEqual(actual_date_time, expected_date_time)

    def test_get_day_name(self):
        date = datetime.datetime(2023, 3, 23)
        expected_day_name = "Thursday"
        actual_day_name = DateTimeConverter.get_day_name(date)
        self.assertEqual(actual_day_name, expected_day_name)


class TestCourtReservation(unittest.TestCase):
    def setUp(self):
        self.data_handler = DataHandler()
        self.reservation = Reservation(self.data_handler)

    def test_set_name(self):
        self.reservation.set_name()
        self.assertIsNotNone(self.reservation.name)

    def test_set_booking_date_time(self):
        expected_booking_date_time_str = "25.03.2023 14:00"
        expected_booking_date_time = datetime.datetime(2023, 3, 25, 14, 0)
        self.reservation.validate_reservation = lambda x: (x, x)

        with patch("builtins.input", return_value=expected_booking_date_time_str):
            # Call the method to be tested
            self.reservation.set_booking_date_time()
        self.assertEqual(self.reservation.booking_date_time, expected_booking_date_time)

    def test_validate_reservation_booking_time_is_not_forbidden(self):
        booking_date_time = datetime.datetime.now() + datetime.timedelta(days=1)
        self.assertEqual(self.reservation.validate_reservation(booking_date_time), None)

    def test_validate_reservation_number_of_reservation_per_week(self):
        booking_date_time = datetime.datetime.now() + datetime.timedelta(days=7)
        self.assertEqual(self.reservation.validate_reservation(booking_date_time), None)

    def test_validate_reservation_hour_is_bookable_for_chosen_day(self):
        booking_date_time = datetime.datetime.now() + datetime.timedelta(days=2)
        self.assertEqual(self.reservation.validate_reservation(booking_date_time), None)

    def test_validate_reservation_hour_is_not_less_now(self):
        booking_date_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.assertEqual(self.reservation.validate_reservation(booking_date_time), None)

    def test_validate_reservation_valid_booking(self):
        expected_booking_date_time = datetime.datetime(2023, 3, 25, 14, 0)
        for hours_delta in [0.5, 1, 1.5]:
            booking_end_time = expected_booking_date_time + datetime.timedelta(
                hours=hours_delta
            )
            validated_booking_time = self.reservation.validate_reservation(
                expected_booking_date_time
            )
            expected_validated_booking_time = (
                expected_booking_date_time,
                booking_end_time,
            )
            self.assertEqual(validated_booking_time, expected_validated_booking_time)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["2"])
    def test_set_book_reservation_period(self, mock_input, mock_output):
        expected_output = "1)30 Minutes\n2)60 Minutes\n3)90 Minutes\n"
        expected_booking_period = datetime.timedelta(hours=1)
        self.reservation.set_book_reservation_period()
        self.assertEqual(mock_output.getvalue(), expected_output)
        self.assertEqual(self.reservation.booking_period, expected_booking_period)


if __name__ == "__main__":
    unittest.main()
