# ecef_to_eci.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
#  Converts ECEF vector components to ECI using GMST angle
#  See "Fundamentals of Astrodynamics and Applications, Fourth Edition" by
#  David A. Vallado, pages 172-173
# Parameters:
# year: year
# month: month
# day: day
# hour: UTC hour
# minute: minute
# second:second
# ecef_x_km: ecef x-coord
# ecef_y_km: ecef y-coord
# ecef_z_km: ecef z-coord
#
# Output:
#  Prints the ECI x,y, and z components
#
# Written by Elise Turka
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# import Python modules
import math # math module
import sys  # argv

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456
w = 7.292115* 10**(-5)

# helper functions


# initialize script arguments
year = float('nan') # year
month = float('nan') # month
day = float('nan') # day
hour = float('nan') # hour
minute = float('nan') # minute
second = float('nan') # second
ecef_x_km = float('nan') # ECI x-component in km
ecef_y_km = float('nan') # ECI y-component in km
ecef_z_km = float('nan') # ECI z-component in km

# parse script arguments
if len(sys.argv)==10:
  year = float(sys.argv[1])
  month = float(sys.argv[2])
  day = float(sys.argv[3])
  hour = float(sys.argv[4])
  minute = float(sys.argv[5])
  second = float(sys.argv[6])
  ecef_x_km = float(sys.argv[7])
  ecef_y_km = float(sys.argv[8])
  ecef_z_km = float(sys.argv[9])
else:
  print(\
   'Usage: '\
   'python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km'\
  )
  exit()

# GETTING FRACTIONAL JULIAN DATE
if month <= 2:
  year = year - 1
  month = month+12

A = year//100
B = 2-A+(A//4)

JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

frac_of_day = hour/24+minute/1440+second/86400

jd_frac = JD+frac_of_day

JD = day - 32075 + 1461*(year+4800+(month-14)/12)/4+367*(month-2-(month-14)/12*12)/12-3*((year+4900+(month-14)/12)/100)/4

TUT1 = (JD - 2451545.0)/36525

# CALCULATING GMST ANGLE
# seconds
gmst_angle = 67310.54841+(876600*60*60+8640184.812866)*TUT1 + 0.093104*math.pow(TUT1, 2) + math.pow(-6.2,-6)*math.pow(TUT1,3)
# degrees modded
extra_rad = math.fmod(gmst_angle, 360)*w
# radians
gmst_angle = math.fmod(gmst_angle*(2*math.pi/86400), (2*math.pi))-extra_rad

# calculating rotation matrix
eci_x_km = ecef_x_km*math.cos(-gmst_angle)+ecef_y_km*math.sin(-gmst_angle)
eci_y_km = ecef_y_km*math.cos(-gmst_angle)-ecef_x_km*math.sin(-gmst_angle)
eci_z_km = ecef_z_km

print(eci_x_km)
print(eci_y_km)
print(eci_z_km)