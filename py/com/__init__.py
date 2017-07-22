from datetime import datetime
from datetime import timedelta
week = datetime.strptime("2017-07-17","%Y-%m-%d").weekday()
print(week)
now = datetime.now()
date = now + timedelta(days = 1)
print(date)