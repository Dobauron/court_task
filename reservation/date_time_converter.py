import datetime


class DateTimeConverter:
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
