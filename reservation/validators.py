from data_handler import DataHandler
import datetime
from filters import search_current_week


class ReservationValidators:
    def __init__(self, name, booking_time):
        self.data_handler = DataHandler("23.03-30.03.json")
        self.data_handler.load_data()
        self.schedule = self.data_handler.schedule
        self.booking_time = booking_time
        self.name = name

    def validate_number_of_reservation_per_week(self):
        """Validate that user is not making reservation more than two time per week"""
        user_reservation_current_week = 0
        current_week = search_current_week(self.booking_time)
        for day in current_week:
            for date, users_reservation in self.schedule.items():
                date_obj = datetime.datetime.strptime(
                    f"{date}.{self.booking_time.year}", "%d.%m.%Y"
                ).date()
                for user_data in users_reservation:
                    if day == date_obj and user_data["name"] == self.name:
                        user_reservation_current_week += 1
        if user_reservation_current_week >= 2:
            print("You are not allowed to book court more then two times per week")
            return False

    def validate_hour_is_bookable(self):
        for date, users_reservation in self.schedule.items():

            # iter through user value for each day
            for user_time_reservation in users_reservation:

                # check if  any date with any time is similar to user choose
                if (
                    user_time_reservation["start_time"]
                    >= self.booking_time.strftime("%H:%M:%S")
                    == user_time_reservation["end_time"]
                ):

                    return False

    def validate_hour_is_less_now(self):
        # check if booking time is not less than now+1 hour
        if self.booking_time < datetime.datetime.now() + datetime.timedelta(hours=1):
            print("Reservation time must be at least one hour ahead from now")
            return False

    def validate_hour_is_available_for_chosen_day(self, booking):
        for date, user_reservation in self.schedule.items():

            # convert date to datetime object, add year
            date_obj = datetime.datetime.strptime(
                f"{date}.{booking.year}", "%d.%m.%Y"
            ).date()

            # if any data object from database have same date, check hour reservation
            if date_obj == booking.date():
                for user_time_reservation in user_reservation:
                    if user_time_reservation["start_time"] == booking.strftime("%H:%M"):
                        suggest_other_reservation = input(
                            f"The time you choose is unavailable,"
                            f" would you like to make a reservation for"
                            f" {user_time_reservation['end_time']} instead (yes/no)"
                        )
                        if suggest_other_reservation == "yes":
                            print(user_time_reservation["end_time"])
                            return user_time_reservation["end_time"]
                        elif suggest_other_reservation == "no":
                            print(False)
                            return False
                        else:
                            print("Your answer was uncorrect, let's start again")
