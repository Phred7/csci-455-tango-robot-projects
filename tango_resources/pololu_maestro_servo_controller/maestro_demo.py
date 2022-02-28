"""
Demonstration program for the maestro_part library for controlling a
servo motor with the Raspberry Pi 3 and the Pololu Maestro board.
"""

import maestro_uart

# min_pos and max_pos are the minimum and maxium positions for the servos
# in quarter-microseconds. The defaults are set on the board. See the Maestro
# manual for how to change these values. The factory defaults are 992us and
# 2000us.
# Allowing quarter-microseconds gives you more resolution to work with.
# e.g. If you want a maximum of 2000us then use 8000us (4 x 2000us).

min_pos = 992*4
max_pos = 2000*4

mu = maestro_uart.MaestroUART('/dev/ttyS0', 9600)
channel = 0

error = mu.get_error()
if error:
	print(error)

accel = 5
mu.set_acceleration(channel, accel)

speed = 32
mu.set_speed(channel, speed)

position = mu.get_position(channel)

print('Position is: %d quarter-microseconds' % position)

if position < min_pos+((max_pos - min_pos)/2): # if less than halfway
	target = max_pos
else:
	target = min_pos

print('Moving to: %d quarter-microseconds' % target)

mu.set_target(channel, target)

mu.close()
