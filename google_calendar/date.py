from datetime import date, timedelta

today = date.today()
start = today - timedelta(days=today.weekday())
end = start + timedelta(days=6)
print("Today: " + str(today))
print("Start: " + str(start))
print("End: " + str(end))
