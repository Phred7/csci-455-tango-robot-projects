import serial, time, sys

try:
    usb = serial.Serial('/dev/ttyACM0')
    print(usb.name)
    print(usb.baudrate)

except:
    try:
        usb = serial.Serial('/dev/ttyACM1')
        print(usb.name)
        print(usb.baudrate)
    except:
        print("No servo serial device found")
        sys.exit(1)

target = 6700
lsb = target & 0x7F
msb = (target >> 7) & 0x7F

# first 3 bits are just control bits
# 0x01 is saying which servo to communicate with
# 0x02 is the waist
# 0x03 is the head
cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x01) + chr(lsb) + chr(msb)
print("sending serial cmd")
usb.write(cmd.encode('utf-8'))
print("reading from serial")
