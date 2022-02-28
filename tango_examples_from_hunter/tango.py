import serial, time, sys

class Tango:

	def __init__(self):
		try:
			self.maestro = serial.Serial('dev/ttyACM0')
			print(self.maestro.name)
			print(self.maestro.baudrate)
		except:
			try:
				self.maestro = serial.Serial('dev/ttyACM1')
				print(self.maestro.name)
				print(self.maestro.baudrate)
			except:
				print("No servo serial device found")
				sys.exit(1)
		target = 5896
		lsb = target &0x7F
		msb = (target >> 7) & 0x7F
		cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x05) + chr(lsb) + chr(msb)
		self.maestro.write(cmd)

