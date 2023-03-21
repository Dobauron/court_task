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
        self.cancel_reservation_date_time = None
        self.schedule = data_handler.load_schedule()
        self.data_handler = data_handler

    def setup_reservation(self):
        self.set_name()
        self.set_booking_date_time()
        self.set_than_save_reservation()

    def cancel_reservation(self):
        self.set_name()
        self.set_cancel_reservation_date_time()
        self.delete_reservation()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_date_time(self):
        booking_date_time_str = input("When would you like to book? {DD.MM.YYYY HH:MM}")
        try:
            booking_date_time = DateTimeConverter.convert_string_to_date_time(
                booking_date_time_str
            )
            validation = self.validate_reservation(booking_date_time)
            if validation is not False:
                self.validated_booking_time = validation
                self.booking_date_time = booking_date_time
        except ValueError:
            print("Invalid date format, Please try again")
            self.set_booking_date_time()

    def validate_reservation(self, booking_date_time):
        if (
            ReservationValidators.validate_booking_time_is_not_forbidden(
                booking_date_time
            )
            is False
        ):
            if (
                ReservationValidators.validate_number_of_reservation_per_week(
                    booking_date_time, self.name, self.schedule
                )
                is False
            ):
                self.set_book_reservation_period()
                validated_booking_time = (
                    ReservationValidators.validate_hour_is_bookable_for_chosen_day(
                        booking_date_time, self.schedule, self.booking_period
                    )
                )
                if validated_booking_time is False:
                    self.set_booking_date_time()
                else:

                    if (
                        ReservationValidators.validate_hour_is_not_less_now(
                            booking_date_time
                        )
                        is False
                    ):

                        if (
                            ReservationValidators.validate_booking_time_is_not_forbidden(
                                booking_date_time, validated_booking_time
                            )
                            is None
                        ):
                            self.set_booking_date_time()
                        else:
                            return validated_booking_time

        else:
            self.set_booking_date_time()

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
            "start_time": DateTimeConverter.get_string_time(
                validated_new_booking_start_time
            ),
            "end_time": DateTimeConverter.get_string_time(
                validated_new_booking_end_time
            ),
        }
        date_key = DateTimeConverter.get_string_date(self.booking_date_time)
        if date_key in self.schedule:
            self.schedule[date_key].append(data)
        else:
            self.schedule[date_key] = [data]
        self.save_to_file()

    def set_cancel_reservation_date_time(self):
        cancel_reservation = input(
            "Please provide date and time for cancel your reservation {DD.MM.YYYY HH:MM} :"
        )
        try:
            cancel_reservation_date_time = (
                DateTimeConverter.convert_string_to_date_time(cancel_reservation)
            )
            cancel_reservation_time = DateTimeConverter.get_string_time(
                cancel_reservation_date_time
            )
            cancel_reservation_date = DateTimeConverter.get_string_time(
                cancel_reservation_date_time
            )
            self.cancel_reservation_date_time = cancel_reservation_date_time
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
        if (
            reservation_to_cancel_index is not False
            and ReservationValidators.validate_hour_is_not_less_now(
                self.cancel_reservation_date_time
            )
            is False
        ):
            del self.schedule[self.cancel_reservation_date][reservation_to_cancel_index]
        else:
            print("There is no reservation with specified data")
            self.cancel_reservation()

        self.cancel_reservation()

    def show_schedule(self):
        try:
            range_date = self.get_all_day_user_specify_range()
            for date in range_date:
                date_str = DateTimeConverter.get_string_date(date)
                if date_str in self.schedule:
                    print(self.name_day_in_schedule(date) + ":")
                    for reservation in self.schedule[date_str]:
                        print(
                            "*",
                            reservation["name"],
                            reservation["start_time"],
                            reservation["end_time"],
                        )
                    else:
                        print("\n")
                else:
                    print(self.name_day_in_schedule(date) + ":\nNo Reservations\n")
        except ValueError:
            print("Invalid date format, Please try again")
            self.show_schedule()

    @staticmethod
    def name_day_in_schedule(date):
        day_name = DateTimeConverter.get_day_name(date)
        today = datetime.datetime.today().date()
        tomorrow = today + datetime.timedelta(days=1)
        yesterday = today - datetime.timedelta(days=1)
        if date == today:
            return "Today"
        elif date == tomorrow:
            return "Tomorrow"
        elif date == yesterday:
            return "Yesterday"
        else:
            return day_name

    @staticmethod
    def get_all_day_user_specify_range():
        start_date = input(
            "Please specify from which date you want to print/save the booking {DD.MM.YYYY}: "
        )
        end_date = input(
            "Please specify until which date you want to print/save the booking {DD.MM.YYYY}: "
        )
        start_date = DateTimeConverter.convert_string_to_date(start_date)
        end_date = DateTimeConverter.convert_string_to_date(end_date)
        all_dates = []
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date)
            current_date += datetime.timedelta(days=1)
        return all_dates

    def save_to_file(self):
        range_date = self.get_all_day_user_specify_range()
        date_reservation_specified_by_user = {}
        for date in range_date:
            date_str = DateTimeConverter.get_string_date(date)
            if date_str in self.schedule:
                for reservation in self.schedule[date_str]:
                    data = {
                        "name": reservation["name"],
                        "start_time": reservation["start_time"],
                        "end_time": reservation["end_time"],
                    }

                    if date_str in date_reservation_specified_by_user:
                        date_reservation_specified_by_user[date_str].append(data)
                    else:
                        date_reservation_specified_by_user[date_str] = [data]

        file_type = input("Specify, how would you like to save data (json/csv): ")
        filename = input("Specify, how file should be named")
        if file_type == "csv":
            self.data_handler.save_schedule_in_csv(
                filename + ".csv", date_reservation_specified_by_user
            )
        elif file_type == "json":
            self.data_handler.save_schedule_in_json(
                filename + ".json", date_reservation_specified_by_user
            )
        else:
            print("You have to choose json or csv")
            self.save_to_file()
