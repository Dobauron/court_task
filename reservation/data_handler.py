import json, csv
from converters import DateTimeConverter


class DataHandler:
    def __init__(self):
        """
        Initializes a DataHandler object with the specified filename and an empty schedule dictionary.
        """
        self.schedule = {}

    def save_schedule_in_json(self, filename, date_reservation_specified_by_user):
        """
        Saves the reservation data to the JSON file under the specified date key.
        """
        self.sort_before_save()
        with open(filename, "w") as f:
            json.dump(date_reservation_specified_by_user, f, indent=4)

    def save_schedule_in_csv(self, filename, date_reservation_specified_by_user):
        """
        Saves the schedule data to a CSV file specified by the given filename.
        """
        self.sort_before_save()
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Name",
                    "Start Time",
                    "End Time",
                ]
            )
            for date, reservations in date_reservation_specified_by_user.items():
                for r in reservations:
                    writer.writerow(
                        [
                            r["name"],
                            date + " " + r["start_time"],
                            date + " " + r["end_time"],
                        ]
                    )

    def sort_before_save(self):
        """
        Sorts the reservations stored in the schedule attribute first based on date than on start time.
        """
        sorted_schedule_by_date = dict(
            sorted(
                self.schedule.items(),
                key=lambda x: DateTimeConverter.convert_string_to_date(x[0]),
            )
        )
        sorted_schedule_by_date_and_start_time = {}
        for date, reservation_data in sorted_schedule_by_date.items():
            sorted_schedule_by_date_and_start_time[date] = sorted(
                reservation_data, key=self.get_start_time
            )
        self.schedule = sorted_schedule_by_date_and_start_time

    @staticmethod
    def get_start_time(el):
        """
        Returns the start time of a reservation data element for sorting purposes.
        """
        return el["start_time"]
