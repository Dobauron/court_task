import datetime


class DateTimeConverter:
    @staticmethod
    def convert_string_date(string_date, year):
        date = datetime.datetime.strptime(f"{string_date}.{year}", "%d.%m.%Y").date()
        return date

    @staticmethod
    def convert_string_time(string_time):
        time = datetime.datetime.strptime(string_time, "%H:%M").time()
        return time

    @staticmethod
    def convert_string_date_time(string_date_time):
        date_time = datetime.datetime.strptime(string_date_time, "%d.%m.%Y %H:%M")
        return date_time

    @staticmethod
    def get_time(booking_data):
        time = booking_data.strftime("%H:%M")
        return time
