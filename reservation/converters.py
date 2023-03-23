import datetime


class DateTimeConverter:
    """A utility class for converting datetime objects and strings.

    This class provides a set of static methods for converting datetime objects to various string formats,
    and for converting string representations of dates and times to datetime objects.

    Static methods:
    - convert_string_to_date(string_date): Convert a string representation of a date to a datetime.date object.
    - convert_string_to_time(string_time): Convert a string representation of a time to a datetime.time object.
    - convert_string_to_date_time(string_date_time): Convert a string representation of a datetime to a datetime.datetime object.
    - get_string_time(date_time): Convert a datetime object to a string representation of the time in format HH:MM.
    - get_string_date(date_time): Convert a datetime object to a string representation of the date in format DD.MM.YYYY.
    - convert_time_to_datetime(date, time_to_convert): Convert a date and a time to a datetime.datetime object.
    - get_day_name(date): Get the name of the day for a given date, e.g. "Monday", "Tuesday", etc.
    """

    @staticmethod
    def convert_string_to_date(string_date):
        date = datetime.datetime.strptime(string_date, "%d.%m.%Y").date()
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
    def get_string_time(date_time):
        time = date_time.strftime("%H:%M")
        return time

    @staticmethod
    def get_string_date(date_time):
        date = date_time.strftime("%d.%m.%Y")
        return date

    @staticmethod
    def convert_time_to_datetime(date, time_to_convert):
        end_time = datetime.datetime.combine(date.date(), time_to_convert)
        return end_time

    @staticmethod
    def get_day_name(date):
        day_name = date.strftime("%A")
        return day_name
