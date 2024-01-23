from skyfield.api import load, Topos
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

# Function to get timezone from latitude and longitude
def get_timezone(lat, lon):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    return pytz.timezone(tz_name)

# Function to prompt user for location and return latitude, longitude, and timezone
def get_user_location():
    lat = float(input("Enter your latitude (e.g., 51.4769): "))
    lon = float(input("Enter your longitude (e.g., -0.0005): "))
    tz = get_timezone(lat, lon)
    return lat, lon, tz

# Load ephemeris data
planets = load('de421.bsp')

# Define celestial bodies
earth, venus, sun = planets['earth'], planets['venus'], planets['sun']

# Get user location and timezone
latitude, longitude, user_timezone = get_user_location()
observer = earth + Topos(latitude, longitude)

# Define a time range for the calculation
ts = load.timescale()
t1 = ts.utc(2023, 1, 1)
t2 = ts.utc(2023, 12, 31)
times = ts.utc(2023, range(1, 366))  # Every day of the year 2023

# Compute positions
astrometric_sun = observer.at(times).observe(sun).apparent()
astrometric_venus = observer.at(times).observe(venus).apparent()

# Calculate separation angle between Venus and the Sun
_, sun_alt, _ = astrometric_sun.altaz()
_, venus_alt, _ = astrometric_venus.altaz()
separation_angle = abs(sun_alt.degrees - venus_alt.degrees)

# Find instances where Venus is close to the Sun in the sky
for ti, angle in zip(times, separation_angle):
    if angle < 1:  # Threshold for "closeness", in degrees; adjust as needed
        local_time = ti.astimezone(user_timezone)
        print(local_time.strftime('%Y-%m-%d %H:%M'), 'Possible Transit')

# Note: This is a very basic approach and may not accurately predict all transits.
