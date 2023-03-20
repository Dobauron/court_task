import datetime
from validators import ReservationValidators
from date_time_converter import DateTimeConverter


class Reservation:
    def __init__(self, data_handler):
        self.name = None
        self.booking_date_time = None
        self.booking_period = None
        self.validated_booking_time = None
        self.cancel_reservation_date = None
        self.cancel_reservation_time = None
        self.schedule = data_handler.load_schedule()
        self.data_handler = data_handler

    def setup_reservation(self):
        self.set_name()
        self.set_booking_date_time()
        self.set_than_save_reservation()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_date_time(self):
        booking_date_time_str = input("When would you like to book? {DD.MM.YYYY HH:MM}")
        try:
            booking_date_time = DateTimeConverter.convert_string_to_date_time(
                booking_date_time_str
            )
            validation = self.validate(booking_date_time)
            if validation is not False:
                self.validated_booking_time = validation
                self.booking_date_time = booking_date_time
        except ValueError:
            print("Invalid date format, Please try again")
            self.set_booking_date_time()

    def validate(self, booking_date_time):
        if (
            ReservationValidators.validate_booking_time_is_not_forbidden(
                booking_date_time
            )
            is False
        ):
            self.set_book_reservation_period()
            validated_booking_time = (
                ReservationValidators.validate_hour_is_bookable_for_chosen_day(
                    booking_date_time, self.schedule, self.booking_period
                )
            )
            if (
                ReservationValidators.validate_number_of_reservation_per_week(
                    booking_date_time, self.name, self.schedule
                )
                is False
                or ReservationValidators.validate_hour_is_not_less_now(
                    booking_date_time
                )
                is False
            ):
                return validated_booking_time

        else:
            return False

    def set_book_reservation_period(self):
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
            self.set_book_reservation_period()

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

    def cancel_reservation(self):
        self.set_name()
        self.set_cancel_reservation_date_time()
        self.delete_reservation()

    def set_cancel_reservation_date_time(self):
        cancel_reservation = input(
            "Please provide date and time for cancel your reservation {DD.MM.YYYY HH:MM}"
        )
        try:
            cancel_reservation_date_time = (
                DateTimeConverter.convert_string_to_date_time(cancel_reservation)
            )
            cancel_reservation_time = DateTimeConverter.get_time(
                cancel_reservation_date_time
            )
            cancel_reservation_date = DateTimeConverter.get_date(
                cancel_reservation_date_time
            )
            self.cancel_reservation_date = cancel_reservation_date
            self.cancel_reservation_time = cancel_reservation_time
        except ValueError:
            print("Invalid date format, Please try again")
            self.set_cancel_reservation_date_time()

    def delete_reservation(self):
        reservation_to_cancel_index = ReservationValidators.validate_reservation_exist(
            self.name,
            self.schedule,
            self.cancel_reservation_date,
            self.cancel_reservation_time,
        )
        if reservation_to_cancel_index is not False:
            print(self.schedule[self.cancel_reservation_date][reservation_to_cancel_index])
            del self.schedule[self.cancel_reservation_date][reservation_to_cancel_index]
        else:
            print('There is no reservation with specified data')
            self.cancel_reservation()

        print(self.schedule)

    def show_schedule(self):
        print("this is schedule", self.schedule)
