import datetime


def search_current_week(booking_date):
    weekday = booking_date.weekday()
    first_weekday = booking_date - datetime.timedelta(days=weekday)

    week_data = []
    for day in range(7):
        date = first_weekday + datetime.timedelta(days=day)
        week_data.append(date)

    print(week_data)
    return week_data
