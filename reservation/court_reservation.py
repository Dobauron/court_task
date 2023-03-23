import datetime
from validators import ReservationValidators
from converters import DateTimeConverter


class Reservation:
    """
    A class representing a reservation of a court. It allows the user to create a reservation and save it to a schedule,
        cancel a previously made reservation, print schedule, and save it to the file.

    Attributes:
    -----------
        name (str): the name of the person who made the reservation
        booking_date_time (datetime.datetime): the date and time when the reservation starts
        booking_period (datetime.timedelta): the length of the reservation
        validated_booking_time (tuple): a tuple containing the start and end time of the validated booking
        cancel_reservation_date_time (datetime.datetime): the date and time when the reservation is canceled
        schedule (dict): a dictionary containing the reservations for each day, keyed by date
        data_handler: an object responsible for loading and saving the schedule to the file

    Methods:
    ---------
        setup_reservation(): allows the user to set up a reservation
        cancel_reservation(): allows the user to cancel a reservation
        set_name(): sets the name of the person making the reservation
        set_booking_date_time(): allows the user to set the date and time of the reservation
        validate_reservation(): validates the date and time of the reservation and returns the validated booking time if
            valid
        set_book_reservation_period(): allows the user to set the length of the reservation
        set_than_save_reservation(): saves the validated reservation to the schedule
        set_cancel_reservation_date_time_then_delete(): allows the user to set the date and time of the reservation to
            cancel, and deletes the corresponding reservation from the schedule
        delete_reservation(): deletes a reservation from the schedule
        show_schedule(): shows the schedule for a specified range of dates
        save_schedule_to_file(): saves the reservation schedule for a user-specified date range to a file in either
            JSON or CSV format.
        name_day_in_schedule() : Returns the name of a day in the reservation schedule based on a given date.
            If the date is today, tomorrow or yesterday, returns the corresponding name.
        def get_all_day_user_specify_range() : Prompts the user to input a start and end date and returns
            a list of all dates within that range.
    """

    def __init__(self, data_handler):
        self.name = None
        self.booking_date_time = None
        self.booking_period = None
        self.validated_booking_time = None
        self.cancel_reservation_date_time = None
        self.schedule = {}
        self.data_handler = data_handler

    def setup_reservation(self):
        self.set_name()
        self.set_booking_date_time()
        self.set_than_save_reservation()

    def cancel_reservation(self):
        self.set_name()
        self.set_cancel_reservation_date_time_then_delete()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_date_time(self):
        try:
            while self.validated_booking_time is None:
                booking_date_time_str = input(
                    "When would you like to book? {DD.MM.YYYY HH:MM}"
                )
                booking_date_time = DateTimeConverter.convert_string_to_date_time(
                    booking_date_time_str
                )
                validation = self.validate_reservation(booking_date_time)
                if validation is not False:
                    self.validated_booking_time = validation
                    self.booking_date_time = booking_date_time
                else:
                    self.set_booking_date_time()
        except ValueError:
            print("Invalid date format, Please try again")
            self.set_booking_date_time()
        except TypeError:
            print("500", f"validated_booking_time is {self.validated_booking_time}\n")

    def validate_reservation(self, booking_date_time):
        """
        Validates the date and time of the reservation based on various criteria, such as whether the chosen time
        is not forbidden, whether the user has not exceeded the maximum number of reservations per week, and whether
        the chosen time is available for booking.

        Parameters:
        -----------
        booking_date_time: datetime.datetime
            The date and time of the reservation.

        Returns:
        --------
        validated_booking_time: tuple or None
            A tuple containing the start and end time of the validated booking if the reservation is valid,
            or None otherwise.
        """
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
                    return
                else:
                    if (
                        ReservationValidators.validate_hour_is_not_less_now(
                            booking_date_time
                        )
                        is False
                    ):
                        if (
                            ReservationValidators.validate_booking_time_is_not_forbidden(
                                booking_date_time,
                                validated_booking_time=validated_booking_time,
                            )
                            is None
                        ):
                            return

                        else:
                            return validated_booking_time

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
        try:
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
            print("Your reservation is successfully added to schedule")
        except TypeError:
            print("validated_booking_time is propably None")
        finally:
            self.validated_booking_time = None

    def set_cancel_reservation_date_time_then_delete(self):
        try:
            while self.cancel_reservation_date_time is None:
                cancel_reservation = input(
                    "Please specify date and time for cancel your reservation {DD.MM.YYYY HH:MM}: "
                )
                cancel_reservation_date_time = (
                    DateTimeConverter.convert_string_to_date_time(cancel_reservation)
                )
                cancel_reservation_time = DateTimeConverter.get_string_time(
                    cancel_reservation_date_time
                )
                cancel_reservation_date = DateTimeConverter.get_string_date(
                    cancel_reservation_date_time
                )
                self.cancel_reservation_date_time = cancel_reservation_date_time
                self.delete_reservation(
                    cancel_reservation_date, cancel_reservation_time
                )
        except ValueError:
            print("Invalid date format, Please try again")
            self.set_cancel_reservation_date_time_then_delete()
        finally:
            self.cancel_reservation_date_time = None

    def delete_reservation(self, cancel_reservation_date, cancel_reservation_time):
        reservation_to_cancel_index = ReservationValidators.validate_reservation_exist(
            self.name,
            self.schedule,
            cancel_reservation_date,
            cancel_reservation_time,
        )
        if (
            reservation_to_cancel_index is not False
            and ReservationValidators.validate_hour_is_not_less_now(
                self.cancel_reservation_date_time
            )
            is False
        ):
            del self.schedule[cancel_reservation_date][reservation_to_cancel_index]
            print("Specified reservation was deleted from schedule")
        else:
            print("There is no reservation with specified data")
            return

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

    def save_schedule_to_file(self):
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
        filename = input("Specify, how file should be named: ")
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
            self.save_schedule_to_file()

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
            "Please specify from which date you want to print/save schedule {DD.MM.YYYY}: "
        )
        end_date = input(
            "Please specify until which date you want to print/save schedule {DD.MM.YYYY}: "
        )
        start_date = DateTimeConverter.convert_string_to_date(start_date)
        end_date = DateTimeConverter.convert_string_to_date(end_date)
        all_dates = []
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date)
            current_date += datetime.timedelta(days=1)
        return all_dates
