from data_handler import DataHandler
import datetime
from filters import search_current_week
from date_time_converter import DateTimeConverter


class ReservationValidators:
    def __init__(self):
        self.data_handler = DataHandler("23.03-30.03.json")
        self.data_handler.load_data()
        # self.schedule = self.data_handler.schedule

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
            print("You are not allowed to book court more then two times per week")
            return False


    @staticmethod
    def validate_hour_is_not_less_now(booking_time):
        # check if booking time is not less than now+1 hour
        if booking_time < datetime.datetime.now() + datetime.timedelta(hours=1):
            print("Reservation time must be at least one hour ahead from now")
            return False


    @staticmethod
    def validate_hour_is_bookable_for_chosen_day(
        booking_date_time, schedule, booking_period
    ):
        reserved_periods = create_schedule_list(booking_date_time, schedule)

        next_booking_time = search_for_next_open_term(
            booking_date_time, reserved_periods, booking_period
        )
        if len(reserved_periods) >= 1:
            suggest_other_reservation = input(
                f"The time you choose is unavailable,"
                f" would you like to make a reservation for"
                f" {next_booking_time} instead (yes/no)"
            )
            if suggest_other_reservation == "yes":
                return next_booking_time
            elif suggest_other_reservation == "no":
                return False
            else:
                print("Your answer was incorrect, let's start again")
                ReservationValidators.validate_hour_is_bookable_for_chosen_day(
                    booking_date_time, schedule, booking_period
                )
        else:
            return booking_date_time



def create_schedule_list(booking_date_time, schedule):
    reserved_periods = []
    for date, user_reservation in schedule.items():

        # convert date to datetime object, add year
        date_obj = DateTimeConverter.convert_string_to_date(date, booking_date_time.year)

        # if any data object have same date, check hour reservation
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
        return reserved_periods


def search_for_next_open_term(booking_date_time, reserved_periods, booking_period):
    booking_end = booking_date_time + booking_period
    booking_end_time = booking_end.time()

    print(booking_date_time)
    for el in range(len(reserved_periods)):
        start_time_reservation = reserved_periods[el][0]
        end_time_reservation = reserved_periods[el][1]
        try:
            start_time_next_reservation = reserved_periods[el+1][0]
        except IndexError:
            print('except', end_time_reservation)
            return DateTimeConverter.convert_time_to_datetime(booking_date_time,end_time_reservation)
        if booking_end_time <= start_time_reservation:
            return booking_date_time
        elif (
            end_time_reservation >= booking_date_time.time()
            and start_time_next_reservation <= booking_end_time
        ):
            print('uha')
            continue
        else:
            continue
    else:
        print('else')
        return booking_end

