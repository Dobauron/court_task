from data_handler import DataHandler
import datetime
from validators import ReservationValidators
from date_time_converter import DateTimeConverter


class Reservation:
    def __init__(self):
        self.name = None
        self.booking_data = None
        self.booking_period = None
        self.validator = None
        self.schedule = {}
        self.data_handler = DataHandler("23.03-30.03.json")

    def setup_reservation(self):
        self.set_name()
        self.set_booking_time_and_validate()
        self.book_reservation_period()
        self.set_reservation()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_time_and_validate(self):
        booking_date_time_str = input("When would you like to book? {DD.MM.YYYY HH:MM}")
        try:
            self.booking_data = DateTimeConverter.convert_string_date_time(
                booking_date_time_str
            )

            # validate day and hour is available for user choice and save answer as new_booking_time
            new_booking_time = (
                ReservationValidators.validate_hour_is_bookable_for_chosen_day(
                    self.booking_data, self.schedule
                )
            )
            # if booking_time is available for chosen date and time
            if new_booking_time is True:

                # validate quantity reservation for user per week
                # validate time is not less than now+1 hour
                # if any validation fail reinvoke set booking time
                if (
                    ReservationValidators.validate_number_of_reservation_per_week(
                        self.booking_data, self.name, self.schedule
                    )
                    is False
                    or ReservationValidators.validate_hour_is_not_less_now(
                        self.booking_data
                    )
                    is False
                ):
                    self.set_booking_time_and_validate()

            # if user not said 'no'
            elif new_booking_time is False:
                self.set_booking_time_and_validate()

            # validation pass
            else:
                # get suggested time and set it in new booking_time if user said 'yes'
                hour, minute = map(int, new_booking_time.split(":"))
                self.booking_data = datetime.datetime.combine(
                    self.booking_data, datetime.time(hour, minute)
                )

        except ValueError:
            # reinvoke method if error appear and send message
            print("Invalid date format, Please try again")
            self.set_booking_time_and_validate()

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

    def set_reservation(self):
        end_time = self.booking_data + self.booking_period
        data = {
            "name": self.name,
            "start_time": DateTimeConverter.get_time(self.booking_data),
            "end_time": DateTimeConverter.get_time(end_time),
        }

        date_key = self.booking_data.strftime("%d.%m")
        if date_key in self.schedule:
            self.schedule[date_key].append(data)
        else:
            self.schedule[date_key] = [data]
        # self.data_handler.save_reservation_json(date_key, data)

    def show_schedule(self):
        print("this is schedule", self.schedule)
