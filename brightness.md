# Backlight brightness control for the Display

I use the Waveshare 5inch HDMI LCD (H). It can be modified to enable backlight PWM brightness control.

See this document from waveshare:
https://files.waveshare.com/upload/5/56/PWM_control_backlight_manual.pdf

I've connected the Raspi GPIO13 to the PWM input of the display and wrote a Python program to run as Systemd service to control the brightness depending of the light level around. A TSL2561 I2C sensor is used, connected to the I2C pins of the Raspi.

Install Python modules:
```
sudo apt install -y python3-smbus i2c-tools python-pip3
sudo pip3 install --break-system-packages adafruit-blinka
sudo pip3 install --break-system-packages adafruit-circuitpython-tsl2561
sudo pip3 install --break-system-packages sdnotify
```

Copy ![brightness.py](brightness.py) to /opt/brightness/brightness.py


## Autostart
created a systemd service with watchdog functionality:
/lib/systemd/system/brightness.service
```
[Unit]
Description=Display Brightness Service
After=multi-user.target
[Service]
#Type=simple
WatchdogSec=30s
Restart=on-failure
StartLimitInterval=5min
StartLimitBurst=4
#StartLimitAction=reboot
WorkingDirectory=/opt/brightness
ExecStart=/usr/bin/python3 /opt/brightness/brightness.py
[Install]
WantedBy=multi-user.target

```

Enable and start:
```
sudo systemctl daemon-reload
sudo systemctl enable brightness
sudo systemctl start brightness
```
