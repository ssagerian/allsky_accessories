# allsky_accessories
dew heater and weather monitor
so the current version of allsky (mine) has the following configuration
RPi Pin is heater 11 GPIO.0 
RPi Pin is fan    12 GPIO.1

need to do the following..
Daily: move all the previous days images to the network store
 run the move_images.py python script
hourly: check the temperature and adjust the heater and fan
  run the check_temperature_status.py 
maybe send an email or text message on changes?


the home sky resides on 171
the network storage resides on 35

