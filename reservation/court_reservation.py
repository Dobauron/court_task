from data_handler import DataHandler
import datetime

class Reservation:
    def __init__(self):
        self.load_data_handler = DataHandler('23.03-30.03.json')
        self.set_name()
        self.set_booking_time()
        self.book_court_period()
        self.validate_user_rent_court()
        self.set_reservation()

    def set_name(self):
        self.name = input('What\'s your Name?')

    def set_booking_time(self):
        booking_time_str = input('When would you like to book? {DD.MM.YYYY HH:MM}')
        try:
            self.booking_time = datetime.datetime.strptime(booking_time_str, '%d.%m.%Y %H:%M')

        except ValueError:
            print('Invalid date format, Please try again')
    def book_court_period(self):
        print('1)30 Minutes\n2)60 Minutes\n3)90Minutes')
        chosen_period = int(input('How long would you like to book court?'))
        if chosen_period == 1:
            self.booking_period = datetime.timedelta(minutes=30)
        elif chosen_period == 2:
            self.booking_period = datetime.timedelta(hours=1)
        elif chosen_period == 3:
            self.booking_period = datetime.timedelta(minutes=90)
        else:
            print('Invalid choice. Please try again.')
            self.book_court_period()


    def validate_user_rent_court(self):
        count_user_visit = 0
        self.load_data_handler.load_data()
        for data, value in self.load_data_handler.schedule.items():
            for name in value:
                if name['name'] == self.name:
                    count_user_visit += 1
        if count_user_visit > 2:
            print('Sorry but u can only visit a court two times per week')

    def set_reservation(self):
        date ={}
        end_time =self.booking_time + self.booking_period
        data ={'name': self.name,
               'start_time':self.booking_time.strftime('%H:%M'),
               'end_time': end_time.strftime('%H:%M')}

        print(data)
        date[self.booking_time.strftime('%d.%m')]=data


        print(date)

R = Reservation()
