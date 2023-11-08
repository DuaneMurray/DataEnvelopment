import pandas as pd
from pandas_market_calendars import get_calendar
import pandas_market_calendars as mcal
import datetime
from datetime import datetime

# Define the date range for the years 2020 through 2023
start_date = '2020-01-01'
end_date = '2020-02-01'

# Create a list of first trading days
first_trading_days = []
last_trading_days = []


# Get the US stock exchange calendar (NYSE by default)
#us_calendar = get_calendar("XNYS")
us_calendar = get_calendar("BMF")
#print(mcal.get_calendar_names())
#date_range = us_calendar.schedule(start_date=start_date, end_date=end_date)
valid_range = us_calendar.valid_days(start_date=start_date, end_date=end_date)

date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # Business day frequency

first_trading_days.append(min(valid_range))
last_trading_days.append(max(valid_range))

#for date in valid_range:
        #is_open(cal, sched, "2010-01-11 13:35:00", "2010-01-12 14:35:00", "2010-01-13 15:59:00", "2010-01-13 16:30:00")
        #if (date in valid_range) and (date.day > 0 and date.day < 6) and (date <= min(date)):
        #    first_trading_days.append(date)

#currentdatetime = first_trading_days[0].strftime("%m/%d/%Y")
first_trading_day = first_trading_days[0].strftime("%Y-%m-%d")
last_trading_day = last_trading_days[0].strftime("%Y-%m-%d")

print(first_trading_days[0])
print(last_trading_days[0])

# Print the list of first trading days
#for trading_day in first_trading_days:
#    print(trading_day)
#    print(last_trading_days)
