import datetime

# Create a datetime object for the specific date
date = datetime.datetime(2022, 6, 15)  # June 15, 2022

# Convert the datetime object to a timestamp (seconds since epoch)
timestamp = datetime.datetime.timestamp(date)

# Since the result is usually in float, you might want to convert it to integer
timestamp = int(timestamp)

print(timestamp)