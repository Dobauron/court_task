import datetime
from validators import ReservationValidators
from date_time_converter import DateTimeConverter


class Reservation:
    def __init__(self, data_handler):
        self.name = None
        self.booking_date_time = None
        self.booking_period = None
        self.validated_booking_time = None
        self.schedule = data_handler.load_schedule()
        self.data_handler = data_handler

    def setup_reservation(self):
        self.set_name()
        self.set_booking_time_and_validate()
        self.set_than_save_reservation()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_time_and_validate(self):
        booking_date_time_str = input("When would you like to book? {DD.MM.YYYY HH:MM}")
        try:
            self.booking_date_time = DateTimeConverter.convert_string_to_date_time(
                booking_date_time_str
            )
            if (
                ReservationValidators.validate_booking_time_is_not_forbidden(
                    self.booking_date_time
                )
                is False
            ):
                print(1)
                self.set_booking_time_and_validate()


            self.book_reservation_period()

            validated_booking_time = (
                ReservationValidators.validate_hour_is_bookable_for_chosen_day(
                    self.booking_date_time, self.schedule, self.booking_period
                )
            )
            # if booking_time is available for chosen date and time
            if (
                validated_booking_time is not None
                and validated_booking_time is not False
            ):

                # validate quantity reservation for user per week
                # validate time is not less than now+1 hour
                # if any validation fail reinvoke set booking time
                if (
                    ReservationValidators.validate_number_of_reservation_per_week(
                        self.booking_date_time, self.name, self.schedule
                    )
                    is False
                    or ReservationValidators.validate_hour_is_not_less_now(
                        self.booking_date_time
                    )
                    is False
                ):
                    self.validated_booking_time = validated_booking_time

            # if user not said 'no'
            elif validated_booking_time is True:
                print(3)
                self.set_booking_time_and_validate()

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

    def set_than_save_reservation(self):
        validated_new_booking_start_time = self.validated_booking_time[0]
        validated_new_booking_end_time = self.validated_booking_time[1]
        data = {
            "name": self.name,
            "start_time": DateTimeConverter.get_time(validated_new_booking_start_time),
            "end_time": DateTimeConverter.get_time(validated_new_booking_end_time),
        }

        date_key = self.booking_date_time.strftime("%d.%m")
        if date_key in self.schedule:
            self.schedule[date_key].append(data)
        else:
            self.schedule[date_key] = [data]
        self.data_handler.save_reservation_in_json(date_key, data)

    def show_schedule(self):
        print("this is schedule", self.schedule)
