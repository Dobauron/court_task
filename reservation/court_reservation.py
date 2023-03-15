class Reservation:
    def __init__(self):
        self.set_name()
        self.set_booking_time()

    def set_name(self):
        self.name = input('What\'s your Name?')

    def set_booking_time(self):
        self.booking_time = input('When would you like to book? {DD.MM.YYYY HH:MM}')
