import os
import platform
from typing import Dict

import serial, tkinter as tk
from serial import SerialException


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
        self.servo_controller = Controller.servo_controller_via_serial()
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
                device = serial.Serial('COM7')
                return device
            except SerialException:
                return None
        else:
            return None

    def drive_servo(self, servo: str, target: int) -> None:
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        serial_command = chr(0xaa) + chr(0xC) + chr(0x04) + chr(int(self.servo_robot_anatomy_map.get(servo))) + chr(
            lsb) + chr(msb)
        self.servo_controller.write(serial_command.encode('utf-8'))

    # Keyboard input class contains arithmetic for doing and modifying each movement.
    # Add methods to this class to control specific movements (turn right, turn waist, pan_head, etc, etc)
    # Add reset method (zero all servos)
    # Add stop method (slowly, decrease the motors to 0 vel.)
    # Add E-stop method that exit's the code and releases the servo controller.
    # Add data_input method. If not a supported method print("Unsupported input data format")

    def forward(self):
        pass

    def reverse(self):
        pass

    def STOPDROPANDROLL(self):
        pass

    def turnwaist(self):
        pass

    def shakehead(self):
        pass

    def nodhead(self):
        pass

    def right(self):
        pass

    def left(self):
        pass




class KeyboardInput:
    # TODO: make class for keyboard input
    # Hunter uses a window for keyboard controlling on the video, not sure how that's supposed to work.
    # Imported tkinter for later use. Guessing we need to be active on a specific window to record key inputs w/tkinter
    # Hunter doesn't have methods, he just has an if else chain for each keycode (23:49 on week 6 friday video)

if __name__ == '__main__':
    controller: Controller = Controller()
    controller.drive_servo("waist", 8000)
