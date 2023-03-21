from court_reservation import Reservation
from data_handler import DataHandler


class Dashboard:
    def __init__(self):
        self.main_loop()

    @staticmethod
    def user_choices():
        print(
            """Welcome to the most famous tennis court!
        1.Make reservation
        2.Cancel reservation
        3.Print schedule
        4.Save schedule to a file
        5.Exit"""
        )

        user_choice = int(input("What you would like to do? "))
        return user_choice

    def main_loop(self):
        reservation = Reservation(DataHandler("23.03-30.03.json"))
        while True:
            try:
                user_choice = self.user_choices()
            except ValueError:
                print("Your choice is unavailable, please enter proper choice")
                user_choice = self.user_choices()
            if user_choice == 1:
                reservation.setup_reservation()
            elif user_choice == 2:
                reservation.cancel_reservation()
            elif user_choice == 3:
                reservation.show_schedule()
            elif user_choice == 4:
                reservation.save_to_file()
            elif user_choice == 5:
                break
            elif user_choice > 5:
                print("Please select one of the available choices")
                continue


dashboard = Dashboard()
