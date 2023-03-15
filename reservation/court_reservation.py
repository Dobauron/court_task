class Reservation:
    def __init__(self):
        self.set_name()
        self.set_booking_time()
        self.book_court_period()
        self.print_data()

    def set_name(self):
        self.name = input('What\'s your Name?')

    def set_booking_time(self):
        self.booking_time = input('When would you like to book? {DD.MM.YYYY HH:MM}')

    def book_court_period(self):
        a = 1
        available_period = ['30 Minutes', '60 Minutes', '90 Minutes']
        for el in available_period:
            print(str(a)+')'+el)
            a+=1
        choosen_period = int(input('How long would you like to book court?'))
        self.choosen_period = available_period[choosen_period-1]

    def validate(self):

    def print_data(self):
        print(self.name, self.booking_time, self.choosen_period)

R = Reservation()