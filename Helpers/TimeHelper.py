from datetime import datetime
import pytz
from Constants import TIMEZONE


def today_in_tz():
    tz = pytz.timezone(TIMEZONE)

    # Create a datetime object representing the current time in the specified timezone
    current_time = datetime.now(tz)

    # Get the date component of the datetime object
    current_date = current_time.date()

    return current_time
