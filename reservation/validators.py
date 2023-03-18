from data_handler import DataHandler
import datetime
from filters import search_current_week


class ReservationValidators:
    def __init__(self):
        self.data_handler = DataHandler("23.03-30.03.json")
        self.data_handler.load_data()
        # self.schedule = self.data_handler.schedule

    def validate_number_of_reservation_per_week(self, booking_time, name, schedule):
        """Validate that user is not making reservation more than two time per week"""
        user_reservation_current_week = 0
        current_week = search_current_week(booking_time)
        for day in current_week:
            for date, users_reservation in schedule.items():
                date_obj = datetime.datetime.strptime(
                    f"{date}.{booking_time.year}", "%d.%m.%Y"
                ).date()
                for user_data in users_reservation:
                    if day == date_obj and user_data["name"] == name:
                        user_reservation_current_week += 1
        if user_reservation_current_week >= 2:
            print("You are not allowed to book court more then two times per week")
            return False

    def validate_hour_is_not_less_now(self, booking_time):
        # check if booking time is not less than now+1 hour
        if booking_time < datetime.datetime.now() + datetime.timedelta(hours=1):
            print("Reservation time must be at least one hour ahead from now")
            return False

    def validate_hour_is_bookable_for_chosen_day(self, booking_time, schedule):
        for date, user_reservation in schedule.items():

            # convert date to datetime object, add year
            date_obj = datetime.datetime.strptime(
                f"{date}.{booking_time.year}", "%d.%m.%Y"
            ).date()

            # if any data object have same date, check hour reservation
            if date_obj == booking_time.date():
                for user_time_reservation in user_reservation:
                    start_time = datetime.datetime.strptime(
                        user_time_reservation["start_time"], "%H:%M"
                    ).time()
                    end_time = datetime.datetime.strptime(
                        user_time_reservation["end_time"], "%H:%M"
                    ).time()
                    if start_time <= booking_time.time() < end_time:
                        print(
                            "time you trying to book is already reserved, please try another"
                        )

                        suggest_other_reservation = input(
                            f"The time you choose is unavailable,"
                            f" would you like to make a reservation for"
                            f" {user_time_reservation['end_time']} instead (yes/no)"
                        )
                        if suggest_other_reservation == "yes":
                            print(user_time_reservation["end_time"])
                            return user_time_reservation["end_time"]
                        elif suggest_other_reservation == "no":
                            return False
                        else:
                            print("Your answer was incorrect, let's start again")
                            self.validate_hour_is_bookable_for_chosen_day(booking_time, schedule)

        else:
            return True
