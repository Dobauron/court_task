import json


class DataHandler:
    def __init__(self, filename):
        """
        Initializes a DataHandler object with the specified filename and an empty schedule dictionary.
        """
        self.filename = filename
        self.schedule = {}

    def save_schedule(self, data):
        """
        Saves the schedule data to the JSON file specified by the filename attribute.
        """
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def load_schedule(self):
        """
        Loads the schedule data from the JSON file specified by the filename attribute and returns it.
        """
        with open(self.filename, "r") as file:
            self.schedule = json.load(file)
        return self.schedule

    def save_reservation_in_json(self, date_key, data):
        """
        Saves the reservation data to the JSON file under the specified date key.
        """

        with open(self.filename, "r") as f:
            self.schedule = json.load(f)
        if date_key in self.schedule:
            self.schedule[date_key].append(data)
        else:
            # Add the new reservation to the existing reservations
            self.schedule[date_key] = [data]

        self.sort_before_save()

        with open(self.filename, "w") as f:
            # Write the updated reservations to the JSON file
            json.dump(self.schedule, f, indent=4)

    def sort_before_save(self):
        """
        Sorts the reservations stored in the schedule attribute based on the start time.
        """
        for date, reservation_data in self.schedule.items():
            self.schedule[date] = sorted(reservation_data, key=self.get_start_time)

    def get_start_time(self, el):
        """
        Returns the start time of a reservation data element for sorting purposes.
        """
        return el["start_time"]
