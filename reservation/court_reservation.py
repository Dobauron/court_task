from data_handler import DataHandler
import datetime
from validators import ReservationValidators


class MakeReservation:
    def __init__(self):
        self.name = None
        self.booking_time = None
        self.booking_period = None
        self.validator = None
        self.data_handler = DataHandler("23.03-30.03.json")
        self.setup_reservation()

    def setup_reservation(self):
        self.set_name()
        self.set_booking_time()
        self.book_reservation_period()
        self.validate_and_set_reservation()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_time(self):
        booking_date_time_str = input("When would you like to book? {DD.MM.YYYY HH:MM}")
        try:
            self.booking_time = datetime.datetime.strptime(
                booking_date_time_str, "%d.%m.%Y %H:%M"
            )
            print("booking time", self.booking_time)

            # Create validators object when booking_time  and user name is seted
            self.validator = ReservationValidators(self.name, self.booking_time)

            # validate day and hour is available for user choice and save answer as new_booking_time
            new_booking_time = self.validator.validate_hour_is_available_for_chosen_day(
                self.booking_time
            )
            if new_booking_time is False:
                self.set_booking_time()
            elif new_booking_time is None:
                self.setup_reservation()
            else:
                # get suggested time and set it in new booking_time if user said 'yes'
                hour, minute = map(int, new_booking_time.split(":"))
                self.booking_time = datetime.datetime.combine(
                    self.booking_time, datetime.time(hour, minute)
                )
        except ValueError:
            print("Invalid date format, Please try again")

    def book_reservation_period(self):
        print("1)30 Minutes\n2)60 Minutes\n3)90 Minutes")
        chosen_period = int(input("How long would you like to book court?"))
        if chosen_period == 1:
            self.booking_period = datetime.timedelta(minutes=30)
        elif chosen_period == 2:
            self.booking_period = datetime.timedelta(hours=1)
        elif chosen_period == 3:
            self.booking_period = datetime.timedelta(minutes=90)
        else:
            print("Invalid choice. Please try again.")
            self.book_reservation_period()

    def validate_and_set_reservation(self):

        if (
            self.validator.validate_number_of_reservation_per_week() is False
            or self.validator.validate_hour_is_bookable() is False
            or self.validator.validate_hour_is_less_now() is False
        ):
            self.setup_reservation()
        else:
            end_time = self.booking_time + self.booking_period
            data = {
                "name": self.name,
                "start_time": self.booking_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
            }

            date_key = self.booking_time.strftime("%d.%m")
            self.data_handler.save_reservation_json(date_key, data)


R = MakeReservation()
