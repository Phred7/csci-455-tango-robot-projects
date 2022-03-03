import os
import platform
from typing import Dict

from serial import SerialException


class Controller:

    def __init__(self) -> None:
        self.fivestepsofPOWER: Dict[int:int] = {0: 4000, #rhigh
                                                1: 5000, #rmid
                                                2: 6000, #mid
                                                3: 7000, #lmid
                                                4: 8000} #lhigh

        self.servo_robot_anatomy_map: Dict[str: int] = {"waist": 0x00,
                                                        "motors": 0x01,
                                                        "turn_motors": 0x02,
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
        self.servo_min: int = 4000
        self.servo_neutral: int = 6000
        self.servo_max: int = 8000
        self.twist_neutral: int = 2
        self.twist_position: int = self.twist_neutral
        self.motor_velocity_counter: int = self.servo_neutral
        self.motor_turn_velocity_counter: int = self.servo_neutral
        if self.servo_controller is None:
            print(f"No servo controller found on {platform.system()} serial port")
            exit(1)
        else:
            print(f"Servo controller found on {self.servo_controller.name}")
        self.drive_servo("turn_motors", self.servo_neutral)

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
        self.motor_velocity_counter -= 16
        if self.motor_velocity_counter < self.servo_min:
            self.motor_velocity_counter = self.servo_min
        if self.motor_velocity_counter > self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("motors", self.motor_velocity_counter)

    def reverse(self):
        # > 6000 on channel 1
        self.motor_velocity_counter += 16
        if self.motor_velocity_counter > self.servo_max:
            self.motor_velocity_counter = self.servo_max
        if self.motor_velocity_counter < self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("motors", self.motor_velocity_counter)
        pass

    def STOPDROPANDROLL(self):
        # 6000 on channel 2 and 1
        # need to slowdown first!!
        pass

    def turnwaist(self, turnright):
        # channel 0
        # from right to left 4096, 4688, 5376, 5968, 8192
        if turnright:
            self.twist_position += 1
        else:
            self.twist_position -= 1

        if self.twist_position < 0:
            self.twist_position = 0
        if self.twist_position > 5:
            self.twist_position = 5
        self.drive_servo("waist", self.fivestepsofPOWER[self.twist_position])


    def headnod(self, turnup):
        # channel 3
        # from right to left 4096, 4688, 5376, 5968, 8192
        if turnup:
            self.twist_position += 1
        else:
            self.twist_position -= 1

        if self.twist_position < 0:
            self.twist_position = 0
        if self.twist_position > 5:
            self.twist_position = 5
        self.drive_servo("head_tilt", self.fivestepsofPOWER[self.twist_position])
        pass


    def headshake(self, turnright):
        # channel 4
        # from up to down 4096, 4688, 5376, 5968, 8192
        if turnright:
            self.twist_position += 1
        else:
            self.twist_position -= 1

        if self.twist_position < 0:
            self.twist_position = 0
        if self.twist_position > 5:
            self.twist_position = 5
        self.drive_servo("head_pan", self.fivestepsofPOWER[self.twist_position])

    def right(self):
        # > 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)

        self.motor_velocity_counter += 16
        if self.motor_velocity_counter > self.servo_max:
            self.motor_velocity_counter = self.servo_max
        if self.motor_velocity_counter < self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("turn_motors", self.motor_velocity_counter)
        pass

    def left(self):
        # < 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)

        self.motor_velocity_counter -= 16
        if self.motor_velocity_counter < self.servo_min:
            self.motor_velocity_counter = self.servo_min
        if self.motor_velocity_counter > self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("turn_motors", self.motor_velocity_counter)
        pass


if __name__ == '__main__':
    pass
    # controller: Controller = Controller()
    # controller.drive_servo("waist", 4000)
