import datetime
from calendar import monthrange


def current_date_range():
    now = datetime.datetime.now()
    week_day, last_day = monthrange(now.year, now.month)
    return (datetime.date(now.year, now.month, 1),
            datetime.date(now.year, now.month, last_day))
