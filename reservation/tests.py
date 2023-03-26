import unittest
import datetime
from court_reservation import Reservation
from data_handler import DataHandler
from unittest.mock import patch
from converters import DateTimeConverter
from validators import ReservationValidators


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
            self.reservation.set_booking_date_time()
        self.assertEqual(self.reservation.booking_date_time, expected_booking_date_time)


    def test_validate_reservation_hour_is_not_less_now(self):
        booking_date_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.assertEqual(self.reservation.validate_reservation(booking_date_time), None)


class TestReservationValidators(unittest.TestCase):
    def test_validate_number_of_reservation_per_week_with_valid_input(self):
        # Set up test data
        booking_date_time = datetime.datetime(2023, 4, 1, 10, 0, 0)
        name = "Mariusz Najman"
        schedule = {
            "29.03.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "31.03.2023": [{"name": "Mariusz Najman"}],
            "01.04.2023": [{"name": "Mariusz Najman"}],
            "02.04.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "03.04.2023": [{"name": "Marcin Pudzianowski"}],
            "04.04.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "06.03.2023": [{"name": "Mariusz Najman"}],
        }

        # Call the method and check the output
        self.assertFalse(
            ReservationValidators.validate_number_of_reservation_per_week(booking_date_time, name, schedule))

    def test_validate_number_of_reservation_per_week_with_invalid_input(self):
        booking_date_time = datetime.datetime(2023, 4, 1, 10, 0, 0)
        name = "Mariusz Najman"
        schedule = {
            "29.03.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "31.03.2023": [{"name": "Mariusz Najman"}],
            "01.04.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "02.04.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "03.04.2023": [{"name": "Marcin Pudzianowski"}],
            "04.04.2023": [{"name": "Mariusz Najman"}, {"name": "Marcin Pudzianowski"}],
            "06.03.2023": [{"name": "Mariusz Najman"}],
        }

        self.assertIsNone(
            ReservationValidators.validate_number_of_reservation_per_week(booking_date_time, name, schedule))

    def test_validate_hour_is_not_less_now_with_valid_input(self):
        booking_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        self.assertFalse(ReservationValidators.validate_hour_is_not_less_now(booking_time))

    def test_validate_hour_is_not_less_now_with_invalid_input(self):
        booking_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        self.assertIsNone(ReservationValidators.validate_hour_is_not_less_now(booking_time))


if __name__ == "__main__":
    unittest.main()
