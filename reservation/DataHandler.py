import json

class DataHandler:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}


    def save_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file)


    def load_data(self):
        with open(self.filename, 'r') as file:
            self.data = json.load(file)

    def print_data(self):
        print(self.data)