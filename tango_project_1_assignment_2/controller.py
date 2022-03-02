from typing import Dict

import serial


class Controller:

    def __init__(self) -> None:
        self.servo_robot_anatomy_map: Dict[str: int] = {"motors": 0x01,
                                                        "waist": 0x02,
                                                        "head_pan": 0x03,
                                                        "head_tilt": 0x04,
                                                        "r_shoulder": 0x05,
                                                        "r_bicep": 0x06,
                                                        "r_elbow": 0x07,
                                                        "r_wrist_tilt": 0x08,
                                                        "r_wrist_pan": 0x09,
                                                        "r_grip": 0x10,
                                                        "l_shoulder": 0x12,
                                                        "l_bicep": 0x13,
                                                        "l_elbow": 0x14,
                                                        "l_wrist_tilt": 0x15,
                                                        "l_wrist_pan": 0x16,
                                                        "l_grip": 0x17
                                                        }
        self.servo_robot_anatomy_map: Dict[str: int] = {"motors": 0x01, "waist": "02", "head_pan": "03",
                                                        "head_tilt": "04"}
        self.servo_controller = None
        # try:
        #     self.servo_controller = serial.Serial('/dev/ttyACM0')
        # except:
        #     try:
        #         self.servo_controller = serial.Serial('/dev/ttyACM1')
        #     except:
        #         exit(1)
        pass

    def drive_servo(self, servo: str, target: int) -> None:
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        serial_command = chr(0xaa) + chr(0xC) + chr(0x04) + chr(int(self.servo_robot_anatomy_map.get(servo))) + chr(
            lsb) + chr(msb)
        self.servo_controller.write(serial_command.encode('utf-8'))

    # TODO: make class for keyboard input
    # Keyboard input class contains arithmetic for doing and modifying each movement.
    # Add methods to this class to control specific movements (turn right, turn waist, pan_head, etc, etc)
    # Add reset method (zero all servos)
    # Add stop method (slowly, decrease the motors to 0 vel.)
    # Add E-stop method that exit's the code and releases the servo controller.
    # Add data_input method. If not a supported method print("Unsupported input data format")


if __name__ == '__main__':
    controller: Controller = Controller()
    controller.drive_servo("waist", 8000)
