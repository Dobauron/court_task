import datetime


def search_current_week(booking_date):
    """
    Returns a list of dates representing the current week based on a given booking date.

    Args:
    -----
        booking_date (datetime.date): A date within the week for which to generate the list of dates.

    Returns:
    --------
        list: A list of datetime.date objects representing the dates in the current week starting from Monday.
    """
    booking_date = booking_date.date()
    weekday = booking_date.weekday()
    first_weekday = booking_date - datetime.timedelta(days=weekday)
    week_data = []
    for day in range(7):
        date = first_weekday + datetime.timedelta(days=day)
        week_data.append(date)
    return week_data
