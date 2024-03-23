#!/usr/bin/python3

import lgpio # pi gpio library for userspace
import time
import sdnotify # systemd watchdog
import board # circuitpython base library
import adafruit_tsl2561 # sensor circuitpython library

# mapping function to adapt sensor value range to PWM
def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Configuration
PWM = 13 # pin used to drive Display PWM 
FREQ = 100 # in Hz

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
        #print(f"Broadband: {x}",end=" ")
        y = map_range(x,50,8000,5,100) # allowed range for y is 0-100
        lgpio.tx_pwm(h, PWM, FREQ, y)
        n.notify("WATCHDOG=1") #tell the systemd watchdog that we're alive
        time.sleep(0.1)

except KeyboardInterrupt:
    lgpio.tx_pwm(h, PWM, FREQ, 100)
    print('Brightness: {}'.format(y))
    lgpio.gpiochip_close(h)
