from typing import Dict

import serial


class Controller:

    def __init__(self) -> None:
        self.servo_robot_anatomy_map: Dict[str: int] = {"motors": 0x01, "waist": "02", "head_pan": "03", "head_tilt": "04"}
        self.servo_controller = None
        try:
            self.servo_controller = serial.Serial('/dev/ttyACM0')
        except:
            try:
                self.servo_controller = serial.Serial('/dev/ttyACM1')
            except:
                exit(1)
        pass

    def drive_servo(self, servo: str, target: int) -> None:
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        serial_command = chr(0xaa) + chr(0xC) + chr(0x04) + chr(self.servo_robot_anatomy_map.get(servo)) + chr(lsb) + chr(msb)
        self.servo_controller.write(serial_command)
