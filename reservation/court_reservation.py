from data_handler import DataHandler
import datetime
import json
from filters import search_current_week

class Reservation:
    def __init__(self):
        self.name = None
        self.booking_time = None
        self.booking_period = None
        self.data_handler = DataHandler("23.03-30.03.json")
        self.set_name()
        self.set_booking_time()
        self.book_court_period()
        self.set_reservation()

    def set_name(self):
        self.name = input("What's your Name?")

    def set_booking_time(self):
        booking_date_time_str = input("When would you like to book? {DD.MM.YYYY HH:MM}")
        try:
            self.booking_time = datetime.datetime.strptime(
                booking_date_time_str, "%d.%m.%Y %H:%M"
            )

        except ValueError:
            print("Invalid date format, Please try again")

    def book_court_period(self):
        print("1)30 Minutes\n2)60 Minutes\n3)90Minutes")
        chosen_period = int(input("How long would you like to book court?"))
        if chosen_period == 1:
            self.booking_period = datetime.timedelta(minutes=30)
        elif chosen_period == 2:
            self.booking_period = datetime.timedelta(hours=1)
        elif chosen_period == 3:
            self.booking_period = datetime.timedelta(minutes=90)
        else:
            print("Invalid choice. Please try again.")
            self.book_court_period()

    def validate_user_rent_court(self):
        day_month_booked = self.booking_time
        self.data_handler.load_data()
        weekday = day_month_booked.weekday()
        first_weekday = day_month_booked - datetime.timedelta(days=weekday)
        last_weekday = first_weekday + datetime.timedelta(days=6)
        week_data = []
        for date in self.data_handler.schedule:
            date_obj = datetime.datetime.strptime(f"{date}.{self.booking_time.year}", "%d.%m.%Y")
            print(date)
            print(type(date))


            print(date_obj)
            print(type(date_obj))
            if first_weekday <= date_obj <= last_weekday:
                week_data.append(date)
        print(first_weekday)
        print(last_weekday)
        print(week_data)



    def set_reservation(self):
        end_time = self.booking_time + self.booking_period
        data = {
            "name": self.name,
            "start_time": self.booking_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
        }

        date_key = self.booking_time.strftime("%d.%m")
        self.data_handler.save_reservation_json(date_key, data)


R = Reservation()
