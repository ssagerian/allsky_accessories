import syslog
from si7020_I2C import si7020_I2C

si = si7020_I2C()
hum,temp = si.get_humidity_and_temperatureF()
print(f" humidity {hum:.2f} temperature {temp:.2f}")


 
