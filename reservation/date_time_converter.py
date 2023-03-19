import datetime


class DateTimeConverter:
    @staticmethod
    def convert_string_to_date(string_date, year):
        date = datetime.datetime.strptime(f"{string_date}.{year}", "%d.%m.%Y").date()
        return date

    @staticmethod
    def convert_string_to_time(string_time):
        time = datetime.datetime.strptime(string_time, "%H:%M").time()
        return time

    @staticmethod
    def convert_string_to_date_time(string_date_time):
        date_time = datetime.datetime.strptime(string_date_time, "%d.%m.%Y %H:%M")
        return date_time

    @staticmethod
    def get_time(booking_date_time):
        time = booking_date_time.strftime("%H:%M")
        return time

    @staticmethod
    def convert_time_to_datetime(booking_date_time, end_time_reservation):
        end_time = datetime.datetime.combine(
            booking_date_time.date(), end_time_reservation
        )
        return end_time
