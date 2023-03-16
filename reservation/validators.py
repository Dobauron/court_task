from data_handler import DataHandler
import datetime
from filters import search_current_week


class ReservationValidators:
    def __init__(self, name, booking_time):
        self.data_handler = DataHandler("23.03-30.03.json")
        self.booking_time = booking_time
        self.name = name

    def validate_number_of_reservation_per_week(self):
        """Validate that user is not making reservation more than two time per week"""
        user_reservation_current_week = 0
        current_week = search_current_week(self.booking_time)
        self.data_handler.load_data()
        for day in current_week:
            for date, user_reservation in self.data_handler.schedule.items():
                date_obj = datetime.datetime.strptime(
                    f"{date}.{self.booking_time.year}", "%d.%m.%Y"
                ).date()
                for user_data in user_reservation:
                    if day == date_obj and user_data["name"] == self.name:
                        user_reservation_current_week += 1
        if user_reservation_current_week <= 2:
            return False

    def validate_hour_is_bookable(self):
        self.data_handler.load_data()
        for date, user_reservation in self.data_handler.schedule.items():
            for user_time_reservation in user_reservation:
                if (
                    user_time_reservation["start_time"]
                    >= self.booking_time.strftime("%H:%M:%S")
                    <= user_time_reservation["end_time"]
                ):
                    return False
