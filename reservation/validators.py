import datetime
from filters import search_current_week
from date_time_converter import DateTimeConverter


class ReservationValidators:
    @staticmethod
    def validate_number_of_reservation_per_week(booking_date_time, name, schedule):
        """Validate that user is not making reservation more than two time per week"""
        user_reservation_current_week = 0
        current_week = search_current_week(booking_date_time)
        for day in current_week:
            for date, users_reservation in schedule.items():
                date_obj = DateTimeConverter.convert_string_to_date(
                    date, booking_date_time.year
                )
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
        reserved_periods = ReservationValidators.create_schedule_list(
            booking_date_time, schedule
        )

        validated_booking_time = ReservationValidators.search_for_next_open_term(
            booking_date_time, reserved_periods, booking_period
        )

        if validated_booking_time[0] != booking_date_time.time():
            suggest_other_reservation = input(
                f"The time you choose is unavailable,"
                f" would you like to make a reservation for"
                f" {validated_booking_time[0]} instead (yes/no)"
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
        reserved_periods = []
        for date, user_reservation in schedule.items():

            date_obj = DateTimeConverter.convert_string_to_date(
                date, booking_date_time.year
            )
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
            return reserved_periods

    @staticmethod
    def search_for_next_open_term(booking_date_time, reserved_periods, booking_period):
        booking_start_time = booking_date_time.time()
        booking_end = booking_date_time + booking_period
        booking_end_time = booking_end.time()
        try:
            start_time_first_reservation = reserved_periods[0][0]
            end_time_first_reservation = reserved_periods[0][1]
            check_current_reservation = (
                ReservationValidators.get_next_available_reservation_time(
                    start_time_first_reservation,
                    end_time_first_reservation,
                    reserved_periods,
                    booking_period,
                    booking_date_time,
                    booking_start_time,
                    booking_end_time,
                )
            )
            return check_current_reservation
        except IndexError:
            return booking_date_time, booking_end

    @staticmethod
    def get_next_available_reservation_time(
        start_time_reserved_term,
        end_time_reserved_term,
        reserved_periods,
        booking_period,
        booking_date_time,
        booking_start_time,
        booking_end_time,
    ):
        try:

            index_current_reservation = reserved_periods.index(
                (start_time_reserved_term, end_time_reserved_term)
            )
            start_time_reserved_term = DateTimeConverter.convert_time_to_datetime(
                booking_date_time, start_time_reserved_term
            )
            end_time_reserved_term = DateTimeConverter.convert_time_to_datetime(
                booking_date_time, end_time_reserved_term
            )

            next_reservation = reserved_periods[index_current_reservation + 1]
            next_reservation_start_time = next_reservation[0]
            next_reservation_end_time = next_reservation[1]
            next_booking_start_time = start_time_reserved_term + booking_period
            next_booking_end_time = end_time_reserved_term + booking_period

            end_time_last_reservation = reserved_periods[-1][1]
            start_time_first_reservation = reserved_periods[0][0]

            if (
                booking_end_time <= start_time_first_reservation
                or booking_start_time >= end_time_last_reservation
            ):
                return booking_start_time, booking_end_time

            elif next_reservation_start_time >= booking_start_time:
                if (
                    start_time_reserved_term <= next_booking_start_time
                    and next_reservation_start_time >= next_booking_end_time.time()
                ):
                    new_booking_end_time = end_time_reserved_term + booking_period

                    return end_time_reserved_term.time(), new_booking_end_time.time()

            check_next_reservation = (
                ReservationValidators.get_next_available_reservation_time(
                    next_reservation_start_time,
                    next_reservation_end_time,
                    reserved_periods,
                    booking_period,
                    next_booking_end_time,
                    booking_start_time,
                    booking_end_time,
                )
            )
            return check_next_reservation
        except IndexError:
            if len(reserved_periods) == 0:
                return booking_start_time, booking_end_time
            else:
                start_time_reserved_term = DateTimeConverter.convert_time_to_datetime(
                    booking_date_time, reserved_periods[-1][1]
                )
                end_time_reserved_term = start_time_reserved_term + booking_period
                return start_time_reserved_term.time(), end_time_reserved_term.time()

    @staticmethod
    def validate_booking_time_is_not_forbidden(
        booking_date_time, validated_booking_time=None
    ):
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
            booking_start_time = DateTimeConverter.convert_time_to_datetime(
                booking_date_time, validated_booking_time[0]
            )
            booking_end_time = DateTimeConverter.convert_time_to_datetime(
                booking_date_time, validated_booking_time[1]
            )

        if (
            booking_start_time < date_time_too_early
            or booking_end_time > date_time_too_late
        ):
            print(
                "Tennis court is closed between 22:00 - 06:00\nPlease choose other reservation time"
            )
            return
        return False

    @staticmethod
    def validate_reservation_exist(
        name, schedule, cancel_reservation_date, cancel_reservation_time
    ):
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
