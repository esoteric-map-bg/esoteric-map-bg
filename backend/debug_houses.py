# Тест за да видим какво точно връща swe.houses()
import swisseph as swe
import datetime

# Данни за Айнщайн
date = datetime.date(1879, 3, 14)
time = datetime.time(11, 30)
lat = 48.4
lon = 10.0
tz_offset = 0.67

# JD
dt_utc = datetime.datetime.combine(date, time) - datetime.timedelta(hours=tz_offset)
jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0)

# Houses
houses_result = swe.houses(jd, lat, lon, b'P')
cusps = houses_result[0]
ascmc = houses_result[1]

print(f"Брой елементи в cusps: {len(cusps)}")
print(f"Брой елементи в ascmc: {len(ascmc)}")
print("\nCUSPS:")
for i, cusp in enumerate(cusps):
    print(f"  cusps[{i}] = {cusp:.4f}°")

print("\nASCMC:")
print(f"  ascmc[0] (ASC) = {ascmc[0]:.4f}°")
print(f"  ascmc[1] (MC)  = {ascmc[1]:.4f}°")
print(f"  ascmc[2] (ARMC)= {ascmc[2]:.4f}°")
print(f"  ascmc[3] (Vertex)= {ascmc[3]:.4f}°")
