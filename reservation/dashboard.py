from court_reservation import MakeReservation


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
        user_choice = self.user_choices()
        if user_choice == 1:
            make_reservation = MakeReservation()
        else:
            pass


dashboard = Dashboard()
