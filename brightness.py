#!/usr/bin/python3

#  Control a 5V PWM fan speed with the lgpio library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import lgpio # pi gpio library vor userspace
import time
import sdnotify # systemd watchdog
import board # circuitpython base library
import adafruit_tsl2561 # sensor circuitpython librory

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Configuration
PWM = 13 # pin used to drive Display PWM 
FREQ = 100

h = lgpio.gpiochip_open(0)

# Luminosity sensor
i2c = board.I2C()
sensor = adafruit_tsl2561.TSL2561(i2c)

# Set high gain mode.
# 0 is low gain 1 is high gain
sensor.gain = 1
# Set integration time.
# A value 0 is 13.7ms, 1 is 101ms, 2 is 402ms, and 3 is manual mode.
sensor.integration_time = 2

n = sdnotify.SystemdNotifier()

try:
    while True:
        x = int(format(sensor.broadband))
        y = map_range(x,50,8000,5,100)
        #print(z)
        #print('Mapped Broadband: {}'.format(y))
        if(y >=100):
            # prevent exeption if value too hight in rare cases (direct sunlight to sensor)
            y = 100
        lgpio.tx_pwm(h, PWM, FREQ, y)
        #print(f"Brightness: {y}")
        n.notify("WATCHDOG=1") #tell the systemd watchdog that we're alive
        time.sleep(0.1)

except KeyboardInterrupt:
    lgpio.tx_pwm(h, PWM, FREQ, 100)
    print(f"Brightness: {y}")
    lgpio.gpiochip_close(h)
