from court_reservation import Reservation
from data_handler import DataHandler


class Dashboard:
    def __init__(self):
        self.main_loop()

    @staticmethod
    def user_choices():
        print(
            """Welcome to the most famous tennis court, what you would like to do?
        1.Make reservation
        2.Cancel reservation
        3.Print schedule
        4.Save schedule to a file
        5.Exit"""
        )
        user_choice = int(input())
        return user_choice

    def main_loop(self):

        reservation = Reservation(DataHandler("23.03-30.03.json"))
        while True:
            user_choice = self.user_choices()
            if user_choice == 1:
                reservation.setup_reservation()
            elif user_choice == 2:
                reservation.cancel_reservation()
            elif user_choice == 3:
                reservation.show_schedule()
            elif user_choice >= 5:
                break


dashboard = Dashboard()
