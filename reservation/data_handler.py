import json


class DataHandler:
    def __init__(self, filename):
        self.filename = filename
        self.schedule = {}

    def save_data(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def load_data(self):
        with open(self.filename, "r") as file:
            self.schedule = json.load(file)

    def print_data(self):
        print(self.schedule)

    def save_reservation_json(self, date_key, data):
        with open(self.filename, "r") as f:
            existing_reservations = json.load(f)
        if date_key in existing_reservations:
            existing_reservations[date_key].append(data)
        else:
            # Add the new reservation to the existing reservations
            existing_reservations[date_key] = [data]

        with open(self.filename, "w") as f:
            # Write the updated reservations to the JSON file
            json.dump(existing_reservations, f, indent=4)
