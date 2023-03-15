import json

class DataHandler:
    def __init__(self, filename):
        self.filename = filename
        self.schedule = {}


    def save_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file)


    def load_data(self):
        with open(self.filename, 'r') as file:
            self.schedule = json.load(file)

    # def print_data(self):
    #     print(self.schedule)
    #     print(type(self.schedule))
    #     for key, value in self.schedule.items():
    #         print(value)


#
# handler = DataHandler('23.03-30.03.json')
# handler.load_data()
# handler.print_data()