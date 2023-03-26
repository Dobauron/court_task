import datetime
from filters import search_current_week
from converters import DateTimeConverter


class ReservationValidators:
    """class ReservationValidators:
    A collection of static methods to validate reservations made by users.

    Methods:
    ---------
    validate_number_of_reservation_per_week(booking_date_time, name, schedule)
        Validate that user is not making reservation more than two times per week.

    validate_hour_is_not_less_now(booking_time)
        Validate that reservation time is at least one hour ahead of the current time.

    validate_hour_is_bookable_for_chosen_day(booking_date_time, schedule, booking_period)
        Validate that the chosen time slot for the booking is available on the selected day.

    create_schedule_list(booking_date_time, schedule)
        Create a list of reserved periods for user chosen date.

    search_for_next_open_term(booking_date_time, reserved_periods, booking_period)
        Search for the next available reservation time slot given the current reservation period.

    get_next_available_reservation_time(start_time_reserved_term, end_time_reserved_term, reserved_periods,
        booking_period, booking_date_time, booking_start_time, booking_end_time)
        Recursively search for the next available reservation time slot given the current reservation period.

    validate_booking_time_is_not_forbidden(booking_date_time, validated_booking_time=None)
        Check if the specified booking time is between 06:00 - 22:00

    validate_reservation_exist(name, schedule, cancel_reservation_date, cancel_reservation_time)
        Check if a reservation exists

    validate_reservation_exist(name, schedule, cancel_reservation_date, cancel_reservation_time)

    All methods are static and don't require an instance of the class to be created.
    """

    @staticmethod
    def validate_number_of_reservation_per_week(booking_date_time, name, schedule):
        user_reservation_current_week = 0
        current_week = search_current_week(booking_date_time)
        for day in current_week:
            for date, users_reservation in schedule.items():
                date_obj = DateTimeConverter.convert_string_to_date(date)
                for user_data in users_reservation:
                    if day == date_obj and user_data["name"] == name:
                        user_reservation_current_week += 1
        if user_reservation_current_week >= 2:
            print(
                "You are not allowed to book court more then two times per week\tYou can make reservation next week"
            )
        else:
            return False

    @staticmethod
    def validate_hour_is_not_less_now(booking_time):
        if booking_time < datetime.datetime.now() + datetime.timedelta(hours=1):
            print("Reservation time must be at least one hour ahead from now")
        else:
            return False

    @staticmethod
    def validate_hour_is_bookable_for_chosen_day(
        booking_date_time, schedule, booking_period
    ):
        """
        Validates whether a booking time slot is available for the given `booking_date_time`
        by checking the `schedule` of existing reservations. If the requested time slot is not
        available, the method suggests the next available time slot and asks the user to confirm
        the booking.

        Args:
            booking_date_time (datetime.datetime): The desired booking date and time.
            schedule (Dict[str, List[Dict[str, str]]]): A dictionary containing the schedules
                of different users. Each key represents a date in the format "YYYY-MM-DD", and
                the corresponding value is a list of dictionaries containing information about
                the reservations made by that user on that day.
            booking_period (datetime.timedelta): The duration of the booking.

        Returns:
            Union[Tuple[datetime.time, datetime.time], bool]: If the requested time slot is
            available, the method returns a tuple containing the start and end times of the
            booking. If the requested time slot is not available and the user chooses to make
            a reservation for the suggested time slot, the method returns a tuple containing
            the start and end times of the suggested booking. If the user chooses not to make
            a reservation for the suggested time slot, the method returns False.
        """
        free_periods = ReservationValidators.create_schedule_list(
            booking_date_time, schedule
        )

        validated_booking_time = ReservationValidators.search_for_next_open_term(
            booking_date_time, free_periods, booking_period
        )
        validated_booking_start_time = validated_booking_time[0]
        if validated_booking_start_time != booking_date_time:
            suggest_other_reservation = input(
                f"The time you choose is unavailable,"
                f" would you like to make a reservation for"
                f" {validated_booking_start_time} instead (yes/no)"
            )
            if suggest_other_reservation == "yes":
                return validated_booking_time
            elif suggest_other_reservation == "no":
                return False
            else:
                print("Your answer was incorrect, let's start again")
                ReservationValidators.validate_hour_is_bookable_for_chosen_day(
                    booking_date_time, schedule, booking_period
                )

        else:
            return validated_booking_time

    @staticmethod
    def create_schedule_list(booking_date_time, schedule):
        """
        Create a list of reserved periods for a given date in the schedule.

        Args:
        - booking_date_time (datetime.datetime): The datetime for which to retrieve the reserved periods.
        - schedule (dict): A dictionary representing the schedule of reservations, where each key is a date string
                           (in the format "YYYY-MM-DD"), and each value is a list of dictionaries, where each dictionary
                           represents a reservation and contains the keys "name", "start_time", and "end_time".

        Returns:
        - A list of tuples, where each tuple represents a reserved period and contains two datetime.time objects
          representing the start and end times of the period, respectively. The list is sorted in ascending order
          of start times.
        """
        reserved_periods = []
        for date, user_reservation in schedule.items():
            date_obj = DateTimeConverter.convert_string_to_date(date)
            if date_obj == booking_date_time.date():
                for user_time_reservation in user_reservation:
                    start_time_schedule = DateTimeConverter.convert_string_to_time(
                        user_time_reservation["start_time"]
                    )
                    end_time_schedule = DateTimeConverter.convert_string_to_time(
                        user_time_reservation["end_time"]
                    )
                    reserved_periods.append((start_time_schedule, end_time_schedule))

        else:
            reserved_periods.sort()
            return ReservationValidators.reset_create_schedule_list(reserved_periods)

    @staticmethod
    def reset_create_schedule_list(reserved_periods):
        new_free_periods = []
        open_time_start = DateTimeConverter.convert_string_to_time("06:00")
        closed_time_start = DateTimeConverter.convert_string_to_time("22:00")
        try:
            new_free_periods.append((open_time_start, reserved_periods[0][0]))
            new_free_periods.append((reserved_periods[-1][1], closed_time_start))

            for reservation_index in range(len(reserved_periods)):
                new_free_periods.append(
                    (
                        reserved_periods[reservation_index][1],
                        reserved_periods[reservation_index + 1][0],
                    )
                )

        except IndexError:
            if len(new_free_periods) == 0:
                new_free_periods.append((open_time_start, closed_time_start))
            else:
                for period in new_free_periods:
                    if period[0] == period[1]:
                        new_free_periods.remove(period)
                    else:
                        continue
            sorted_new_free_periods = sorted(new_free_periods, key=lambda x: x[0])
            return sorted_new_free_periods

    @staticmethod
    def search_for_next_open_term(booking_date_time, free_periods, booking_period):
        """
        Finds the next available time slot for a booking based on the provided booking date and time,
        a list of already reserved time periods, and the duration of the booking.

        Args:
            booking_date_time (datetime.datetime): The date and time of the booking.
            free_periods (list): A list of tuples representing already reserved time periods, where each tuple contains the start and end times.
            booking_period (datetime.timedelta): The duration of the booking.

        Returns:
            tuple: A tuple containing the start and end times of the next available time slot for the booking.
        """
        booking_start_time = booking_date_time
        booking_end = booking_date_time + booking_period
        booking_end_time = booking_end
        try:
            check_current_reservation = ReservationValidators.search_next_bookable_term(
                free_periods,
                booking_period,
                booking_date_time,
                booking_start_time,
                booking_end_time,
            )
            return check_current_reservation
        except IndexError:
            return booking_date_time, booking_end

    @staticmethod
    def search_next_bookable_term(
        free_periods,
        booking_period,
        booking_date_time,
        booking_start_time,
        booking_end_time,
    ):
        for period in free_periods:
            start_time_free_period = DateTimeConverter.convert_time_to_datetime(
                booking_date_time, period[0]
            )
            end_time_free_period = DateTimeConverter.convert_time_to_datetime(
                booking_date_time, period[1]
            )
            current_checked_open_bookable_period = (
                end_time_free_period - start_time_free_period
            )
            if booking_period <= current_checked_open_bookable_period:
                if (
                    int(booking_start_time.timestamp())
                    in range(
                        int(start_time_free_period.timestamp()),
                        int(end_time_free_period.timestamp()),
                    )
                    and booking_end_time <= end_time_free_period
                ):
                    return booking_start_time, booking_end_time
                elif booking_start_time < start_time_free_period:
                    return (
                        start_time_free_period,
                        start_time_free_period + booking_period,
                    )
                elif booking_end_time > end_time_free_period:
                    return end_time_free_period - booking_period, end_time_free_period
                else:
                    continue

    @staticmethod
    def validate_booking_time_is_not_forbidden(
        booking_date_time, validated_booking_time=None
    ):
        """
        Check if the specified booking time is allowed.

        Args:
            booking_date_time (datetime.datetime): The start time of the booking.
            validated_booking_time (tuple, optional): A tuple containing the start and end time
                of the booking, if already validated. Defaults to None.

        Returns:
            bool: False if the booking time is allowed, otherwise None.

        """
        too_early = DateTimeConverter.convert_string_to_time("06:00")
        too_late = DateTimeConverter.convert_string_to_time("22:00")
        date_time_too_early = DateTimeConverter.convert_time_to_datetime(
            booking_date_time, too_early
        )
        date_time_too_late = DateTimeConverter.convert_time_to_datetime(
            booking_date_time, too_late
        )
        if validated_booking_time is None:
            booking_start_time = booking_date_time
            booking_end_time = booking_date_time
        else:
            booking_start_time = validated_booking_time[0]
            booking_end_time = validated_booking_time[1]

        if (
            booking_start_time < date_time_too_early
            or booking_end_time > date_time_too_late
        ):
            print(
                "Tennis court is closed between 22:00 - 06:00\nPlease choose other reservation time"
            )
            return
        else:
            return False

    @staticmethod
    def validate_reservation_exist(
        name, schedule, cancel_reservation_date, cancel_reservation_time
    ):
        """
        Check if a reservation exists.

        Args:
            name (str): The name associated with the reservation.
            schedule (dict): A dictionary containing reservation data.
            cancel_reservation_date (str): The date of the reservation to cancel.
            cancel_reservation_time (str): The start time of the reservation to cancel.

        Returns:
            int: The index of the reservation to cancel, if found. False otherwise.

        """
        for date, list_reservation in schedule.items():
            if date == cancel_reservation_date:
                reservation_to_cancel_index = 0
                for reservation in list_reservation:
                    if (
                        reservation["start_time"] == cancel_reservation_time
                        and reservation["name"] == name
                    ):
                        return reservation_to_cancel_index
                    else:
                        reservation_to_cancel_index += 1
                        continue
                else:
                    return False
