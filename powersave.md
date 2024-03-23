# Powersaving feature


At first I've implemeted the backlight PWM brightness feature. This is great to reduce the brightness of the display during the night, especially because the radio is used as a bedside alarm clock.

But - it does not reduce the amount of used enery that much. 

Power usage is about 4.7 watts when the Peppy player is in screensaver mode (clock display) including the Raspi Zero 2 W.
Way too much.
The used Waveshare "5inch HDMI LCD (H)" has a power button. when switching it off with this button, it saves about 1 watt power. The idea was to steer this button with a radar sensor to only switch the display on when someone is in the room.
