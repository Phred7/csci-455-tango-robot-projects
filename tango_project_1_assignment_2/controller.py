import platform
from time import sleep
from typing import Dict, List

import serial
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
        self.motor_step_size: int = 16
        if self.servo_controller is None:
            print(f"No servo controller found on {platform.system()} serial port")
            exit(1)
        else:
            print(f"Servo controller found on {self.servo_controller.name}")
        # self.drive_servo("turn_motors", self.servo_neutral)

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
        elif platform.system() == 'Darwin':
            print("Sorry mac os is not supported yet.")
            return None
        else:
            return None

    def drive_servo(self, servo: str, target: int) -> None:
        """
        Protocol: 0xAA, device number byte, command byte with MSB cleared, any necessary data
        bytes
        :param servo:
        :param target:
        :return:
        """
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        serial_command = chr(0xaa) + chr(0xC) + chr(0x04) + chr(int(self.servo_robot_anatomy_map.get(servo))) + chr(
            lsb) + chr(msb)
        self.servo_controller.write(serial_command.encode('utf-8'))
        # print(f"moved {servo} on port 0x{int(self.servo_robot_anatomy_map.get(servo))} to {target}")

    def drive_multiple_servos(self, servos: List[str], targets: List[int]) -> None:
        """
        MultiTarget Protocol: 0xAA, device number, 0x1F, number of targets, first channel number, first target
        low bits, first target high bits, second target low bits, second target high bits, …
        :param servos:
        :param targets:
        :return:
        """
        # servo_addresses = [self.servo_robot_anatomy_map.get(servo) for servo in servos]
        # servo_addresses, targets = zip(*sorted(zip(servo_addresses, targets)))
        #
        # serial_command = chr(0xaa) + chr(0xC) + chr(0x1) + chr(0x0F) + chr(len(servos))
        # for i, servo_address in enumerate(servo_addresses):
        #     serial_command += chr(int(servo_address))
        #     serial_command += chr(targets[i] & 0x7F)
        #     serial_command += chr((targets[i] >> 7) & 0x7F)
        self.drive_servo("motors", 6000)
        sleep(0.1)
        serial_command = chr(0xaa) + chr(0xC) + chr(0x1F) + chr(len(servos)) + chr(0x01) + chr((6000 & 0x7F)) + chr((6000 >> 7) & 0x7F) + chr(0x02) + chr((8000 & 0x7F)) + chr((8000 >> 7) & 0x7F)
        self.servo_controller.write(serial_command.encode('utf-8'))
        # sleep(0.1)
        # serial_command = chr(0xaa) + chr(0xC) + chr(0x1F) + chr(len(servos)) + chr(0x01) + chr((6000 & 0x7F)) + chr((6000 >> 7) & 0x7F) + chr(0x02) + chr((7000 & 0x7F)) + chr((7000 >> 7) & 0x7F)
        # self.servo_controller.write(serial_command.encode('utf-8'))

    def __drive_left(self, target: int):
        self.drive_servo("motors", 6000)
        sleep(0.1)
        target = 6000
        turn = 6000
        serial_command = chr(0xaa) + chr(0xC) + chr(0x1F) + chr(2) + chr(0x01) + chr((target & 0x7F)) + chr((target >> 7) & 0x7F) + chr(0x02) + chr((turn & 0x7F)) + chr((turn >> 7) & 0x7F)
        self.servo_controller.write(serial_command.encode('utf-8'))
        print("turn left")

    def __drive_right(self, target: int):
        self.drive_servo("motors", 6000)
        sleep(0.1)
        target = 6000
        turn = 4000
        serial_command = chr(0xaa) + chr(0xC) + chr(0x1F) + chr(2) + chr(0x01) + chr((target & 0x7F)) + chr((target >> 7) & 0x7F) + chr(0x02) + chr((turn & 0x7F)) + chr((turn >> 7) & 0x7F)
        self.servo_controller.write(serial_command.encode('utf-8'))
        print("turn right")

    def forward(self):
        # < 6000 on channel 1
        self.motor_velocity_counter -= self.motor_step_size
        if self.motor_velocity_counter < self.servo_min:
            self.motor_velocity_counter = self.servo_min
        if self.motor_velocity_counter > self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("motors", self.motor_velocity_counter)

    def reverse(self):
        # > 6000 on channel 1
        self.motor_velocity_counter += self.motor_step_size
        if self.motor_velocity_counter > self.servo_max:
            self.motor_velocity_counter = self.servo_max
        if self.motor_velocity_counter < self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("motors", self.motor_velocity_counter)
        pass

    def STOPDROPANDROLL(self):
        # 6000 on channel 2 and 1
        # need to slowdown first!!
        while self.motor_turn_velocity_counter != self.servo_neutral:
            if self.motor_turn_velocity_counter > self.servo_neutral:
                self.motor_turn_velocity_counter -= self.motor_step_size
            else:
                self.motor_turn_velocity_counter += self.motor_step_size
            self.drive_servo("turn_motors", self.motor_velocity_counter)
        while self.motor_velocity_counter != self.servo_neutral:
            if self.motor_velocity_counter > self.servo_neutral:
                self.motor_velocity_counter -= self.motor_step_size
            else:
                self.motor_velocity_counter += self.motor_step_size
            self.drive_servo("turn_motors", self.motor_velocity_counter)
        print("stopped")
        return

    def turnwaist(self, turnright):
        # channel 0
        # from right to left 4096, 4688, 5376, 5968, 8192
        if turnright:
            self.twist_position += 1
        else:
            self.twist_position -= 1

        if self.twist_position < 0:
            self.twist_position = 0
        if self.twist_position > 4:
            self.twist_position = 4
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
        if self.twist_position > 4:
            self.twist_position = 4
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
        if self.twist_position > 4:
            self.twist_position = 4
        self.drive_servo("head_pan", self.fivestepsofPOWER[self.twist_position])

    def right(self):
        # > 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)
        #
        # self.motor_velocity_counter += 16
        # if self.motor_velocity_counter > self.servo_max:
        #     self.motor_velocity_counter = self.servo_max
        # if self.motor_velocity_counter < self.servo_neutral:
        #     self.motor_velocity_counter = self.servo_neutral
        # # self.drive_servo("turn_motors", self.motor_velocity_counter)
        self.__drive_right(self.motor_velocity_counter)
        pass

    def left(self):
        # < 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)
        #
        # self.motor_velocity_counter -= 16
        # if self.motor_velocity_counter < self.servo_min:
        #     self.motor_velocity_counter = self.servo_min
        # if self.motor_velocity_counter > self.servo_neutral:
        #     self.motor_velocity_counter = self.servo_neutral
        #self.drive_servo("turn_motors", self.motor_velocity_counter)
        self.__drive_left(self.motor_velocity_counter)
        pass


if __name__ == '__main__':
    controller: Controller = Controller()
    controller.drive_multiple_servos(["turn_motors", "motors"], [controller.servo_max, controller.servo_neutral])
    # for i in range(4000, 8000):
    #     controller.drive_multiple_servos(["turn_motors", "motors"], [controller.servo_max, controller.servo_neutral])
