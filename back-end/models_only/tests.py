from django.test import TestCase

# Create your tests here.
def dms_to_decimal(dms):
    degrees, minutes, seconds, direction = dms[:-1], 0, 0, dms[-1]
    if '-' in degrees:
        degrees, minutes = degrees.split('-', 1)
        if '-' in minutes:
            minutes, seconds = minutes.split('-', 1)
    degrees = float(degrees)
    minutes = float(minutes) / 60
    seconds = float(seconds) / 3600
    decimal = degrees + minutes + seconds
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

# Example usage
lat_dms = "34-58-59N"
lon_dms = "003-01-00W"

lat_decimal = dms_to_decimal(lat_dms)
lon_decimal = dms_to_decimal(lon_dms)

print("Latitude (Decimal):", lat_decimal)
print("Longitude (Decimal):", lon_decimal)