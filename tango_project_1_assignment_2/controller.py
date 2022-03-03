import os
import platform
import tkinter
from typing import Dict

import serial, tkinter as tk
from serial import SerialException


class Controller:

    def __init__(self) -> None:
        self.fivestepsofPOWER: Dict[str:int] = {"rhigh": 4096,
                                                "rmid":4688,
                                                "mid":5376,
                                                "lmid":5968,
                                                "lhigh": 8192

        }
        self.servo_robot_anatomy_map: Dict[str: int] = {"motors": 0x01,
                                                        "waist": 0x00,
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
        self.servo_controller = Controller.servo_controller_via_serial()
        self.servo_min: int = 4096
        self.servo_neutral: int = 5376
        self.servo_max: int = 8192
        if self.servo_controller is None:
            print(f"No servo controller found on {platform.system()} serial port")
            exit(1)
        else:
            print(f"Servo controller found on {self.servo_controller.name}")

    @staticmethod
    def servo_controller_via_serial():
        if platform.system() == 'Linux':
            try:
                device = serial.Serial('/dev/ttyACM0')
                return device
            except SerialException:
                try:
                    device = serial.Serial('/dev/ttyACM1')
                    return device
                except SerialException:
                    return None
        elif platform.system() == 'Windows':
            try:
                device = serial.Serial('COM21')
                return device
            except SerialException:
                return None
        else:
            return None

    @staticmethod
    def print_me(key) -> None:
        print(f"Printed: {key}")

    def drive_servo(self, servo: str, target: int) -> None:
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        serial_command = chr(0xaa) + chr(0xC) + chr(0x04) + chr(int(self.servo_robot_anatomy_map.get(servo))) + chr(
            lsb) + chr(msb)
        self.servo_controller.write(serial_command.encode('utf-8'))
        print(f"moved {servo} on port 0x{int(self.servo_robot_anatomy_map.get(servo))} to {target}")

    # Keyboard input class contains arithmetic for doing and modifying each movement.
    # Add methods to this class to control specific movements (turn right, turn waist, pan_head, etc, etc)
    # Add reset method (zero all servos)
    # Add stop method (slowly, decrease the motors to 0 vel.)
    # Add E-stop method that exit's the code and releases the servo controller.
    # Add data_input method. If not a supported method print("Unsupported input data format")

    def forward(self):
        # < 6000 on channel 1
        pass

    def reverse(self):
        # > 6000 on channel 1
        pass

    def STOPDROPANDROLL(self):
        # 6000 on channel 2 and 1
        # need to slowdown first!!
        pass

    def turnwaist(self):
        # channel 0
        # from right to left 4096, 4688, 5376, 5968, 8192
        pass

    def shakehead(self):
        # channel 3
        # from right to left 4096, 4688, 5376, 5968, 8192
        pass

    def nodhead(self):
        # channel 4
        # from up to down 4096, 4688, 5376, 5968, 8192
        pass

    def right(self):
        # > 6000 on channel 2
        pass

    def left(self):
        # < 6000 on channel 2
        pass


if __name__ == '__main__':
    pass
    # controller: Controller = Controller()
    # controller.drive_servo("waist", 4000)
